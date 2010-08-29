#
from google.appengine.ext import db
from google.appengine.api import users 

from device import *
from firmware import *

class User(db.Model):
    googleUser = users.User
    
class Update(db.Model):
    date = db.DateTimeProperty(auto_now_add=True)
    device = db.ReferenceProperty(Device)
    firmware = db.ReferenceProperty(Firmware)
    user = db.ReferenceProperty(User)
    
# n-m relation
class UserDevices(db.Model):
    user = db.ReferenceProperty(User)
    device = db.ReferenceProperty(Device)
