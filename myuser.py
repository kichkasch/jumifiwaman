#
from google.appengine.ext import db
from google.appengine.api import users 

from device import *
from firmware import FirmwareGroup, Firmware

class User(db.Model):
    googleUser = db.UserProperty()
#    role = db.StringProperty(choices=set(["read", "add", "delete"]))

    
# n-m relation
class UserDevices(db.Model):
    user = db.ReferenceProperty(User)
    device = db.ReferenceProperty(Device)
    firmwareGroup = db.ReferenceProperty(FirmwareGroup)
    
class UserDeviceUpdates(db.Model):
    user = db.ReferenceProperty(User)
    device = db.ReferenceProperty(Device)
    release = db.ReferenceProperty(Firmware)
    updateDatetime = db.DateTimeProperty(auto_now_add=True)

class UserProfile(db.Model):
    user = db.ReferenceProperty(User)
    emailUpdateEach = db.BooleanProperty()
    emailUpdateBulk = db.BooleanProperty()
    emailRegularInterval = db.StringProperty(choices=set(["daily", "weekly", "monthly"]))
    emailUserLoginAddress = db.BooleanProperty()
    emailSpecifiedAddress = db.StringProperty()

    def getEmailAdress(self):
        if self.emailUserLoginAddress:
            return self.user.googleUser.email()
        else:
            return self.emailSpecifiedAddress
