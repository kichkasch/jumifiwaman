#
#
from google.appengine.ext import db

class Device(db.Model):
    name = db.StringProperty()
    deviceID = db.StringProperty()
