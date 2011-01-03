from myuser import *
import serversettings
from google.appengine.ext import webapp
from google.appengine.api import users
from datetime import datetime
from google.appengine.api import mail


class DailyCron(webapp.RequestHandler):
    def _assembleMyDevSection(self, myUser):
        txt = "=" * 80 + "\n"
        summary = "=" * 80 + "\nAction summary: \n\n"
        device_query = UserDevices.all().filter('user = ', myUser)
        uds = device_query.fetch(100)
        for ud in uds:
            device = ud.device
            txt += device.name + "\n"
            if ud.firmwareGroup:
                fwgName = ud.firmwareGroup.name
                fwQuery = Firmware.all().filter("group =", ud.firmwareGroup).order("-releaseDate")
                fwLatest = fwQuery.fetch(1)
            else:
                fwLatest = None

            txt += """Latest firmware available: """
            if fwLatest:
                txt += fwLatest[0].version + "\n"
            else:
                txt += "None\n"   

            releaseQuery = UserDeviceUpdates.all().filter('user = ', myUser).filter('device = ', device).order('-updateDatetime')
            releases = releaseQuery.fetch(1)
            txt += """Firmware installed: """
            if releases:
                txt += releases[0].release.version + "\n"
            else:
                txt += "None\n"

            txt += """\nRequired action: """
            if fwLatest:
                if not releases:
                    txt += 'Install Release Number %s\n' %(fwLatest[0].version)
                    summary += """%s: Install release %s\n""" %(device.name, fwLatest[0].version) 
                elif releases[0].release.version != fwLatest[0].version:
                    txt += 'Install Release Number %s\n' %(fwLatest[0].version)
                else:
                    txt += 'None\n'
            else:
                txt += 'None\n'

            txt += "\n" + "-" * 60 + "\n"

        txt += "=" * 80
        txt = summary + txt
        return txt

    def _assembleStatusUpdate(self, myUser, stFrequency):
        body = """%s JuMiFiWaMan Status Update\n""" %(stFrequency)
        myDevs = self._assembleMyDevSection(myUser)
        body += myDevs
	return body

    def get(self):
        query = UserProfile.all().filter("emailUpdateBulk =", True)
        res = query.fetch(1000)
        for myProfile in res:
            myUser = myProfile.user
            interval = myProfile.emailRegularInterval
            receiver_address = myProfile.getEmailAdress()
            subject = "Status Update" 
            if interval == "daily":
                body = self._assembleStatusUpdate(myUser, "Daily")
            elif interval == "weekly":
                if datetime.today().isoweekday() == serversettings.DAY_OF_WEEK:
                    body = self._assembleStatusUpdate(myUser, "Weekly")
                else:
                    body = None
            elif interval == "monthly":
                if datetime.today().day == serversettings.DAY_OF_MONTH:
                    body = self._assembleStatusUpdate(myUser, "Monthly")
                else:
                    body = None
            else:
                body = None

            if body:
                body += """\nVisit %s for updating and subscription settings.""" %(serversettings.APP_URL)
                mail.send_mail(serversettings.SENDER_ADDRESS, receiver_address, subject, body)   

