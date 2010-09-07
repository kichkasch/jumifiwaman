# JuMiFiWaMan
# by Michael Pilgermann (kichkasch@gmx.de)
# GPLv3
import os
from google.appengine.ext.webapp import template
import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from device import Device, DeviceGroup, Manufactorer
from firmware import *
from myuser import User

class MainPage(webapp.RequestHandler):
    
    def get(self):
        device_query = Device.all().order('-name')
        devices = device_query.fetch(100)
        
        groupQuery = DeviceGroup.all().order('-name')
        groups = groupQuery.fetch(100)

        manQuery = Manufactorer.all().order('-name')
        mans = manQuery.fetch(100)

        fwSourceQuery = FirmwareSource.all().order('-name')
        fwSources = fwSourceQuery.fetch(100)
        
        fwStatusQuery = DevelopmentStatus.all().order('-name')
        fwStatus = fwStatusQuery.fetch(100)
        
        fwGroupsQuery = FirmwareGroup.all().order('-name')
        fwGroups = fwGroupsQuery.fetch(100)
        for g in fwGroups:
            fwQuery = Firmware.all().filter("group =", g).order("-releaseDate")
            fws = fwGroupsQuery.fetch(1)
            if fws:
                g.latestFirmware = fws[0]
            else:
                g.latestFirmware = None

        u = User()
        if users.get_current_user():
            u.googleUser = users.get_current_user()
            userText = u.googleUser
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            profText = 'Profile Settings'
        else:
            userText = "<none>"
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'          
            profText = None

        template_values = {
            'groups': groups, 
            'devices': devices,
            'manufactorers': mans, 
            'userText': userText, 
            'url': url, 
            'urlText': url_linktext, 
            'profileText': profText, 
            'firmwareSources': fwSources, 
            'firmwareStatus': fwStatus, 
            'firmwareGroups': fwGroups
            }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class TestPage(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'test.html')
        self.response.out.write(template.render(path, template_values))        

class AddDevice(webapp.RequestHandler):
    def post(self):
        device = Device()
        device.name = self.request.get('deviceName')
        device.deviceID = self.request.get('deviceID')
        query = DeviceGroup.all().filter('name = ', self.request.get('deviceGroup'))
        device.group = query.fetch(1)[0]
        query = Manufactorer.all().filter('name = ', self.request.get('manufactorer'))
        device.manufactorer = query.fetch(1)[0]
        device.put()

class AddDeviceGroup(webapp.RequestHandler):
    def post(self):
        group = DeviceGroup()
        group.name = self.request.get('groupName')
        group.put()        

class AddManufactorer(webapp.RequestHandler):
    def post(self):
        man = Manufactorer()
        man.name = self.request.get('manName')
        man.website = self.request.get('manWebsite')
        man.put()

class RemoveManufactoer(webapp.RequestHandler):
    def post(self):
        query = Manufactorer.all().filter('name = ', self.request.get('manufactorer'))
        manufactorer = query.fetch(1)[0]
        manufactorer.delete()

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

def main():
    application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/test', TestPage), 
                                      ('/newDevice', AddDevice), 
                                      ('/newDeviceGroup', AddDeviceGroup), 
                                      ('/newManufactorer', AddManufactorer), 
                                      ('/removeManufactorer', RemoveManufactoer), 
                                      ('/newFirmwareSource', AddFirmwareSource), 
                                      ('/newFirmwareStatus', AddFirmwareStatus), 
                                      ('/newFirmwareGroup', AddFirmware), 
                                      ('/details/fwGroupByName', DetailsFirmwareGroup)
                                      ],
                                     debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
