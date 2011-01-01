from firmware import *
from myuser import User
from myuser_requesthandler import informUsersOnUpdate
from google.appengine.ext import webapp
from google.appengine.api import users
from datetime import datetime, date

class AddFirmwareSource(webapp.RequestHandler):
    def post(self):
        fwSource = FirmwareSource()
        fwSource.name = self.request.get('fwSourceName')
        fwSource.put()

class AddFirmwareStatus(webapp.RequestHandler):
    def post(self):
        fwStatus = DevelopmentStatus()
        fwStatus.name = self.request.get('fwStatusName')
        fwStatus.put()

class AddFirmware(webapp.RequestHandler):
    def post(self):
        fwGroup = FirmwareGroup()
        fwGroup.name = self.request.get('fwGroupName')
        fwGroup.homepage = self.request.get('fwGroupHomepage')
        fwGroup.notes = self.request.get('fwGroupNotes')
        status = self.request.get('fwGroupStatus')
        source = self.request.get('fwGroupSource')
        query = DevelopmentStatus.all().filter('name = ', status)
        fwGroup.developmentStatus = query.fetch(1)[0]
        query = FirmwareSource.all().filter('name = ', source)
        fwGroup.origin = query.fetch(1)[0]
        fwGroup.put()

class AddRelease(webapp.RequestHandler):
    def post(self):
        release = Firmware()
        release.version = self.request.get('fwReleaseNumber')
        release.releaseDate = datetime.strptime(self.request.get("fwReleaseDate"), "%Y-%m-%d").date()
        name = self.request.get('fwGroupForRelease')
        query = FirmwareGroup.all().filter('name = ', name)
        fwg = query.fetch(1)[0]
        release.group = fwg
        release.downloadLink = self.request.get('fwReleaseDirectLink')
        googleUser = users.get_current_user()
#        query = User.all().filter('googleUser = ', googleUser)
#        release.insertMaintainer = query.fetch(1)[0]
        release.insertMaintainer = None
        release.put()
        fwg.lastCheck = datetime.today().date()
        fwg.put() 
        informUsersOnUpdate(fwg, release)       

class FWGUpdateChecked(webapp.RequestHandler):
    def post(self):
        name = self.request.get('fwGroup')
        query = FirmwareGroup.all().filter('name = ', name)
        fwg = query.fetch(1)[0]
        fwg.lastCheck = datetime.today().date()
        fwg.put()

class DetailsFirmwareGroup(webapp.RequestHandler):
    def get(self):
        name = self.request.get('name')
        query = FirmwareGroup.all().filter('name = ', name)
        fwg = query.fetch(1)[0]
        txt = "%s\n%s\n%s\n%s\n%s" %(fwg.name, fwg.homepage, fwg.notes, fwg.developmentStatus.name, fwg.origin.name)
        self.response.out.write(txt)
        
class LatestRelease(webapp.RequestHandler):
    def get(self):
        name = self.request.get('groupName')
        query = FirmwareGroup.all().filter('name = ', name)
        fwg = query.fetch(1)[0]
        fwQuery = Firmware.all().filter("group =", fwg).order("-releaseDate")
        fws = fwQuery.fetch(1)
        if fws:
            release = fws[0]
            txt = "%s\n%s\n%s" %(release.version, release.releaseDate, release.downloadLink)
        else:
            txt = 'n.a.\nn.a.\nn.a.\n'
        self.response.out.write(txt)
        
class AllReleases(webapp.RequestHandler):
    def get(self):
        name = self.request.get('groupName')
        query = FirmwareGroup.all().filter('name = ', name)
        fwg = query.fetch(1)[0]
        fwQuery = Firmware.all().filter("group =", fwg).order("-releaseDate")
        fws = fwQuery.fetch(20)
        txt = ""
        for release in fws:
            txt += "<tr><td>%s</td><td>%s</td></tr>\n" %(str(release.releaseDate), release.version)
        self.response.out.write(txt)        
        
class ReleasesForFirmwareGroup(webapp.RequestHandler):
    def get(self):
        name = self.request.get('groupName')
        query = FirmwareGroup.all().filter('name = ', name)
        fwg = query.fetch(1)[0]
        fwQuery = Firmware.all().filter("group =", fwg).order("-releaseDate")
        fws = fwQuery.fetch(20)
        txt = ""
        for release in fws:
            txt += "<option>%s</option>" %(release.version)
        self.response.out.write(txt)    
        
class FirmwareGroups(webapp.RequestHandler):
    def get(self):
        sEcho = self.request.get('sEcho')
        query = FirmwareGroup.all().order('-name')
        i=0
        fwgs = query.fetch(100)
        txt = '{"sEcho": ' + sEcho + ', "iTotalRecords": ' + str(len(fwgs)) + ', "iTotalDisplayRecords": '+ str(len(fwgs)) + ', "aaData":  ['
        for fwg in fwgs:
            if i:
                txt += ","
            txt += '["' + fwg.name + '","' + fwg.origin.name + '","' + fwg.developmentStatus.name + '",'
            fwQuery = Firmware.all().filter("group =", fwg).order("-releaseDate")
            fws = fwQuery.fetch(1)
            if fws:
                fws = fws[0]
                txt += '"'+ str(fws.version) + '", "'+ str(fws.releaseDate) + '",'
            else:
                txt += '"", "",'
                
            if fwg.lastCheck:
                txt += '"' + str(fwg.lastCheck) + '", '
            else:
                txt +=  '"", '

            # long time no check for new firmware?
            if not fwg.lastCheck:
                txt += '"1"'
            elif (date.today() - fwg.lastCheck).days > 30:    # check form firmware suggested after 30 days
                txt += '"1"'
            else:
                txt += '"0"'

            txt += ']'
            i+=1            
        txt += ']}'
        self.response.out.write(txt)

class FWGsForDevice(webapp.RequestHandler):
    def get(self):
        query = FirmwareGroup.all().order('name')
        fwgs = query.fetch(100)
        txt = '<option>--none--</option>'
        for fwg in fwgs:
            txt += '<option>' + fwg.name + '</option>'
        self.response.out.write(txt)

class DetailsForRelease(webapp.RequestHandler):
    def get(self):
        name = self.request.get('groupName')
        query = FirmwareGroup.all().filter('name = ', name)
        fwg = query.fetch(1)[0]
        version = self.request.get('version')
        fwQuery = Firmware.all().filter("group =", fwg).filter("version =", version)
        fws = fwQuery.fetch(1)
        if fws:
            release = fws[0]
            txt = "%s\n%s\n%s" %(release.version, release.releaseDate, release.downloadLink)
        else:
            txt = 'n.a.\nn.a.\n#\n'
        self.response.out.write(txt)
