from google.appengine.ext import db

class FirmwareGroup(db.Model):
    name = db.StringProperty()
    developmentStatus =  db.StringProperty(choices=set(["production", "beta", "under development"]))
    origin =  db.StringProperty(choices=set(["vendor", "third party"]))    
    
class Firmware(db.Model):
    version = db.StringProperty()
    releaseDate = db.DateTimeProperty()
    developmentStatus =  db.StringProperty(choices=set(["production", "beta", "under development"]))
    origin =  db.StringProperty(choices=set(["vendor", "third party"]))
    group = db.ReferenceProperty(FirmwareGroup)
    downloadLink = db.LinkProperty()
