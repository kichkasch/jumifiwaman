from google.appengine.ext import db
#from myuser import User

class FirmwareSource(db.Model):
    name = db.StringProperty() # vendor, third party ...

class DevelopmentStatus(db.Model):
    name = db.StringProperty() #"production", "beta", "under development"

class FirmwareGroup(db.Model):
    name = db.StringProperty()
    developmentStatus =  db.ReferenceProperty(DevelopmentStatus)
    origin =  db.ReferenceProperty(FirmwareSource)
    latestFirmware = None
    lastCheck = db.DateProperty()
    homepage = db.StringProperty()
    notes = db.StringProperty()

class Firmware(db.Model):
    version = db.StringProperty()
    releaseDate = db.DateProperty()
    group = db.ReferenceProperty(FirmwareGroup)
    downloadLink = db.LinkProperty()
#    insertMaintainer = db.ReferenceProperty(User) # who provided this information
