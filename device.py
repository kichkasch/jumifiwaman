#
#
from google.appengine.ext import db

class DeviceGroup(db.Model):
    name = db.StringProperty()
    
class Manufactorer(db.Model):
    name = db.StringProperty()
    website = db.StringProperty()
    
class Device(db.Model):
    name = db.StringProperty()
    deviceID = db.StringProperty()
    group = db.ReferenceProperty(DeviceGroup)
    manufactorer = db.ReferenceProperty(Manufactorer)
    
