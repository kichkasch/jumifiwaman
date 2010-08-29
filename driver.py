#
import os
from google.appengine.ext.webapp import template
import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from device import Device, DeviceGroup, Manufactorer

class MainPage(webapp.RequestHandler):
    def get(self):
        device_query = Device.all().order('-name')
        devices = device_query.fetch(10)
        
        groupQuery = DeviceGroup.all().order('-name')
        groups = groupQuery.fetch(10)

        manQuery = Manufactorer.all().order('-name')
        mans = manQuery.fetch(10)

        template_values = {
            'groups': groups, 
            'devices': devices,
            'manufactorers': mans, 
            }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
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
        self.redirect('/')

class AddDeviceGroup(webapp.RequestHandler):
    def post(self):
        group = DeviceGroup()
        group.name = self.request.get('groupName')
        group.put()        
        self.redirect('/')

class AddManufactorer(webapp.RequestHandler):
    def post(self):
        man = Manufactorer()
        man.name = self.request.get('manName')
        man.website = self.request.get('manWebsite')
        man.put()        
        self.redirect('/')

def main():
    application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/newDevice', AddDevice), 
                                      ('/newDeviceGroup', AddDeviceGroup), 
                                      ('/newManufactorer', AddManufactorer)],
                                     debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
