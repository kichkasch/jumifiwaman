from google.appengine.ext import db

class FirmwareSource(db.Model):
    name = db.StringProperty() # vendor, third party ...
    
class DevelopmentStatus(db.Model):
    name = db.StringProperty() #"production", "beta", "under development"

class FirmwareGroup(db.Model):
    name = db.StringProperty()
    developmentStatus =  db.ReferenceProperty(DevelopmentStatus)
    origin =  db.ReferenceProperty(FirmwareSource)
    latestFirmware = None
    lastCheck = db.DateTimeProperty()
    
class Firmware(db.Model):
    version = db.StringProperty()
    releaseDate = db.DateTimeProperty()
    group = db.ReferenceProperty(FirmwareGroup)
    downloadLink = db.LinkProperty()
