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
from myuser_requesthandler import *
from cron_requesthandler import *

class MainPage(webapp.RequestHandler):
    
    def get(self):
        groupQuery = DeviceGroup.all().order('name')
        groups = groupQuery.fetch(100)

        manQuery = Manufactorer.all().order('name')
        mans = manQuery.fetch(100)

        fwSourceQuery = FirmwareSource.all().order('name')
        fwSources = fwSourceQuery.fetch(100)
        
        fwStatusQuery = DevelopmentStatus.all().order('name')
        fwStatus = fwStatusQuery.fetch(100)

        u = User()
        if users.get_current_user():
#            u.googleUser = users.get_current_user()
###            u.role = 'add'  # later properly
#            u.put()
            userText = users.get_current_user()
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
                                      ('/sendTestMail', TestMail),                                         
#                                      everything about devices -> check device_requesthandler for details
                                      ('/newDevice', AddDevice), 
                                      ('/newDeviceGroup', AddDeviceGroup), 
                                      ('/newManufactorer', AddManufactorer), 
                                      ('/removeManufactorer', RemoveManufactoer), 
                                      ('/getDevices', Devices), 
                                      ('/getDevicesForGroup', DevicesForGroup), 
                                      ('/details/deviceDetails', DetailsForDevice), 
#                                      everything about firmwares -> check firmware_requesthandler for details
                                      ('/newFirmwareSource', AddFirmwareSource), 
                                      ('/newFirmwareStatus', AddFirmwareStatus), 
                                      ('/newFirmwareGroup', AddFirmware), 
                                      ('/newRelease', AddRelease), 
                                      ('/details/fwGroupByName', DetailsFirmwareGroup), 
                                      ('/getFirmwareGroups', FirmwareGroups), 
                                      ('/getLatestReleaseForFirmwareGroup', LatestRelease), 
                                      ('/getAllReleasesForFirmwareGroup', AllReleases), 
                                      ('/getFWGsForDevice', FWGsForDevice), 
                                      ('/updateChecked', FWGUpdateChecked), 
                                      ('/getRelasesForFWG', ReleasesForFirmwareGroup), 
                                      ('/details/releaseDetails', DetailsForRelease), 
#                                      everything about user specific information (mydevices etc.)-> check myuser_requesthandler for details
                                      ('/getMyDevices', AllUserDevices), 
                                      ('/addToMyDevices', AddMyDevice), 
                                      ('/applyFWGToMyDevice', ApplyFWGToDevice), 
                                      ('/documentUpdateToMyDevice', UpdateMyDevice), 
                                      ('/getAllUpdatesForUserDevice', UpdatesForUserDevice),
                                      ('/profile/updateProfile', UpdateUserProfile),
                                      ('/profile/loadProfile', LoadUserProfile),
#                                      everything about scheduled jobs
                                      ('/cron/dailyUpdate', DailyCron),
                                      ],
                                     debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
