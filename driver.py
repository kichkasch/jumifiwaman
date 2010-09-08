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
from firmware_requesthandler import *
from device_requesthandler import *

class MainPage(webapp.RequestHandler):
    
    def get(self):
#        device_query = Device.all().order('-name')
#        devices = device_query.fetch(100)
        
        groupQuery = DeviceGroup.all().order('-name')
        groups = groupQuery.fetch(100)

        manQuery = Manufactorer.all().order('-name')
        mans = manQuery.fetch(100)

        fwSourceQuery = FirmwareSource.all().order('-name')
        fwSources = fwSourceQuery.fetch(100)
        
        fwStatusQuery = DevelopmentStatus.all().order('-name')
        fwStatus = fwStatusQuery.fetch(100)

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
#            'devices': devices,
            'manufactorers': mans, 
            'userText': userText, 
            'url': url, 
            'urlText': url_linktext, 
            'profileText': profText, 
            'firmwareSources': fwSources, 
            'firmwareStatus': fwStatus
            }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
    


def main():
    application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/newDevice', AddDevice), 
                                      ('/newDeviceGroup', AddDeviceGroup), 
                                      ('/newManufactorer', AddManufactorer), 
                                      ('/removeManufactorer', RemoveManufactoer), 
                                      ('/newFirmwareSource', AddFirmwareSource), 
                                      ('/newFirmwareStatus', AddFirmwareStatus), 
                                      ('/newFirmwareGroup', AddFirmware), 
                                      ('/details/fwGroupByName', DetailsFirmwareGroup), 
                                      ('/getFirmwareGroups', FirmwareGroups), 
                                      ('/getDevices', Devices)
                                      ],
                                     debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
