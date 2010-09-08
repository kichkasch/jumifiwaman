from firmware import *
from google.appengine.ext import webapp

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
        
class DetailsFirmwareGroup(webapp.RequestHandler):
    def get(self):
        name = self.request.get('name')
        query = FirmwareGroup.all().filter('name = ', name)
        fwg = query.fetch(1)[0]
        txt = "%s\n%s\n%s\n%s\n%s" %(fwg.name, fwg.homepage, fwg.notes, fwg.developmentStatus.name, fwg.origin.name)
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
                txt += '"'+ fws.version + '", "'+ fws.releaseDate + '", ""'
            else:
                txt += '"", "", ""'
            txt += ']'
            i+=1            
        txt += ']}'
        self.response.out.write(txt)
