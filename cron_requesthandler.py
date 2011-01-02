from myuser import *
from google.appengine.ext import webapp
from google.appengine.api import users
from datetime import datetime
from google.appengine.api import mail


class DailyCron(webapp.RequestHandler):
    def get(self):
        query = UserProfile.all().filter("emailUpdateBulk =", True)
        res = query.fetch(1000)
        for myProfile in res:
            myUser = myProfile.user
            interval = myProfile.emailRegularInterval
            if myProfile.emailUserLoginAddress:
                receiver_address = myUser.googleUser.email()
            else:
                receiver_address = myProfile.emailSpecifiedAddress
            sender_address = "Jumi Firmware Manager Admin <jumifiwaman10@googlemail.com>"
            subject = "Status Update" 
            body = """Daily JuMiFiWaMan Status Update\n\nVisit http://jumifiwaman.appspot.com/ for updating and settings.""" 
            mail.send_mail(sender_address, receiver_address, subject, body)   

