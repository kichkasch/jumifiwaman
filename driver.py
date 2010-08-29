#
import os
from google.appengine.ext.webapp import template
import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

from device import Device

class MainPage(webapp.RequestHandler):
    def get(self):
        device_query = Device.all().order('-name')
        devices= device_query.fetch(10)

        template_values = {
            'devices': devices,
            }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


class AddDevice(webapp.RequestHandler):
    def post(self):
        device = Device()
        device.name = self.request.get('deviceName')
        device.deviceID = self.request.get('deviceID')
        device.put()
        self.redirect('/')

def main():
    application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/newDevice', AddDevice)],
                                     debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
