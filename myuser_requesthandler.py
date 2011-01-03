from myuser import *
from device import Device
from firmware import FirmwareGroup, Firmware
from google.appengine.ext import webapp
from google.appengine.api import users
from datetime import datetime
from google.appengine.api import mail

class AllUserDevices(webapp.RequestHandler):
    def get(self):
        gUser = users.get_current_user()
        query = User.all().filter('googleUser = ', gUser)
        res = query.fetch(1)
        if res:
            myUser = res[0]
        else:
            myUser = User()
            myUser.googleUser = gUser
            myUser.put()
        device_query = UserDevices.all().filter('user = ', myUser)
        
        nrDevices = int(device_query.count())
        sEcho = self.request.get('sEcho')
        numberRecords = int(self.request.get('iDisplayLength'))
        startRecords = int(self.request.get('iDisplayStart'))
        try:
            indexSort = int(self.request.get('iSortCol_0'))
        except:
            indexSort = 0
        directionSort = self.request.get('sSortDir_0')
        if directionSort.strip().lower() == "desc":
            directionSort = "-"
        else:
            directionSort = ""
#        sortList = ['device.name','device.manufactorer']
#        device_query = device_query.order(directionSort + sortList[indexSort])
        i=0
        devices = device_query.fetch(numberRecords,  offset = startRecords)
        txt = '{"sEcho": ' + sEcho + ', "iTotalRecords": ' + str(nrDevices) + ', "iTotalDisplayRecords": '+ str(nrDevices) + ', "aaData":  ['
        for device in devices:
            fws = 0
            if i:
                txt += ","
            if device.firmwareGroup:
                fwgName = device.firmwareGroup.name
                fwQuery = Firmware.all().filter("group =", device.firmwareGroup).order("-releaseDate")
                fws = fwQuery.fetch(1)
                if fws:
                    fws = fws[0]
                    fwgLatest = str(fws.version) + ' ('+ str(fws.releaseDate) + ')'
                else:
                    fwgLatest = "n.a."
            else:
                fwgName = "n.a."
                fwgLatest = "n.a."
            releaseQuery = UserDeviceUpdates.all().filter('user = ', myUser).filter('device = ', device.device).order('-updateDatetime')
            releases = releaseQuery.fetch(1)
            if releases:
                relName = releases[0].release.version
                relDate = str(releases[0].updateDatetime)
            else:
                relName = "n.a."
                relDate = "n.a."
            txt += '["' + device.device.name + '","' + device.device.manufactorer.name + '","' + fwgName+ '","' + relName+  '","' + relDate +  '","' + fwgLatest+ '"'

            # newer firmware available?
            if fws:
                if not releases:
                    txt += ', "1"]'
                elif releases[0].release.version != fws.version:
                    txt += ', "1"]'
                else:
                    txt += ', "0"]'
            else:
                txt += ', "0"]'

            i+=1
        txt += ']}'
        self.response.out.write(txt)

class AddMyDevice(webapp.RequestHandler):
    def post(self):
        userDevice = UserDevices()
        
        devName = self.request.get('deviceName')
        device_query = Device.all().filter('name = ', devName)
        devItem = device_query.fetch(1)[0]

        fwgName = self.request.get('fwgName')   # firmware group name
        if fwgName.strip().lower() == "--none--":
            fwgItem = None
        else:
            fw_query = FirmwareGroup.all().filter('name = ', fwgName)
            fwgItem = fw_query.fetch(1)[0]
        
        gUser = users.get_current_user()
        query = User.all().filter('googleUser = ', gUser)
        res = query.fetch(1)
        if res:
            myUser = res[0]
        else:
            myUser = User()
            myUser.googleUser = gUser
            myUser.put()

        userDevice.user = myUser
        userDevice.device = devItem
        userDevice.firmwareGroup = fwgItem
        
        userDevice.put()
        
class ApplyFWGToDevice(webapp.RequestHandler):
    def post(self):
        devName = self.request.get('deviceName')
        device_query = Device.all().filter('name = ', devName)
        devItem = device_query.fetch(1)[0]        
        
        gUser = users.get_current_user()
        query = User.all().filter('googleUser = ', gUser)
        res = query.fetch(1)
        myUser = res[0]
        
        query = UserDevices.all().filter('user = ', myUser).filter('device = ', devItem)
        item = query.fetch(1)[0]
        
        fwgName = self.request.get('fwgName')   # firmware group name
        if fwgName.strip().lower() == "--none--":
            fwgItem = None
        else:
            fw_query = FirmwareGroup.all().filter('name = ', fwgName)
            fwgItem = fw_query.fetch(1)[0]
            
        item.firmwareGroup = fwgItem
        item.put()
        
class UpdateMyDevice(webapp.RequestHandler):
    def post(self):
        devName = self.request.get('deviceName')
        device_query = Device.all().filter('name = ', devName)
        devItem = device_query.fetch(1)[0]        
        
        fwgName = self.request.get('fwgName')
        fw_query = FirmwareGroup.all().filter('name = ', fwgName)
        fwgItem = fw_query.fetch(1)[0]
        
        releaseNumber = self.request.get('releaseName')
        relQuery = Firmware.all().filter('group = ', fwgItem).filter('version = ', releaseNumber)
        relItem = relQuery.fetch(1)[0]
        
        installationTime = self.request.get('releaseDate')
        if installationTime.strip().lower() == "now":
            installationTime = None
        else:
            installationTime = datetime.strptime(installationTime, "%Y-%m-%d")
        
        gUser = users.get_current_user()
        query = User.all().filter('googleUser = ', gUser)
        res = query.fetch(1)
        myUser = res[0]
        
        udu = UserDeviceUpdates()
        udu.user = myUser
        udu.device = devItem
        udu.release = relItem
        if installationTime:
            udu.updateDatetime = installationTime
        udu.put()
        
class UpdatesForUserDevice (webapp.RequestHandler):
    def get(self):
        devName = self.request.get('devName')
        device_query = Device.all().filter('name = ', devName)
        devItem = device_query.fetch(1)[0]           
        
        gUser = users.get_current_user()
        query = User.all().filter('googleUser = ', gUser)
        res = query.fetch(1)
        myUser = res[0]        
        
        query = UserDeviceUpdates.all().filter('user = ', myUser).filter('device = ', devItem).order('-updateDatetime')
        releases = query.fetch(20)
        txt = ""
        for release in releases:
            txt += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n" %(str(release.updateDatetime.date()), release.release.group.name, release.release.version)
        self.response.out.write(txt)            

class TestMail(webapp.RequestHandler):
    def post(self):
        gUser = users.get_current_user()
        query = User.all().filter('googleUser = ', gUser)
        res = query.fetch(1)
        myUser = res[0]        

        query = UserProfile().all().filter('user = ', myUser)
        res = query.fetch(1)
        if res:
            myProfile = res[0]
            if myProfile.emailUserLoginAddress:
                receiver_address = gUser.email()
            else:
                receiver_address = myProfile.emailSpecifiedAddress
            sender_address = "Jumi Firmware Manager Admin <jumifiwaman10@googlemail.com>"
            subject = "TestEmail"
            body = """This is a test email from JuMiFiWaMan"""
            mail.send_mail(sender_address, receiver_address, subject, body)        

class UpdateUserProfile(webapp.RequestHandler):
    def post(self):
        updateEach = self.request.get('updateEach')
        updateRegular = self.request.get('updateRegular')
        updateRegularInterval = self.request.get('updateRegularInterval')
        updateEmailType = self.request.get('updateEmailType')
        updateEmailAddress = self.request.get('updateEmailAddress')

        gUser = users.get_current_user()
        query = User.all().filter('googleUser = ', gUser)
        res = query.fetch(1)
        myUser = res[0]        

        query = UserProfile().all().filter('user = ', myUser)
        res = query.fetch(1)
        if res:
            myProfile = res[0]
        else:
            myProfile = UserProfile()
            myProfile.user = myUser

        myProfile.emailUpdateEach = (updateEach.strip().lower() == "true")
        myProfile.emailUpdateBulk = (updateRegular.strip().lower() == "true")
        myProfile.emailRegularInterval = updateRegularInterval
        myProfile.emailUserLoginAddress = (updateEmailType.strip().lower() == "true")
        myProfile.emailSpecifiedAddress = updateEmailAddress 
	myProfile.put()

class LoadUserProfile(webapp.RequestHandler):
    def get(self):
        txt = ""

        gUser = users.get_current_user()
        query = User.all().filter('googleUser = ', gUser)
        res = query.fetch(1)
        myUser = res[0]        

        query = UserProfile().all().filter('user = ', myUser)
        res = query.fetch(1)
        if res:
            myProfile = res[0]
            txt += str(myProfile.emailUpdateEach).lower() + "\n"
            txt += str(myProfile.emailUpdateBulk).lower() + "\n"
            txt += myProfile.emailRegularInterval + "\n"
            txt += str(myProfile.emailUserLoginAddress).lower() + "\n"
            txt += myProfile.emailSpecifiedAddress + "\n"
        else:
            txt = "None"  + "\n"
        self.response.out.write(txt)            

def informUsersOnUpdate(fwg, release):
    query = UserDevices.all().filter('firmwareGroup = ', fwg)
    res = query.fetch(1000)
    for ud in res:
        myUser = ud.user
        query = UserProfile().all().filter('user = ', myUser)
        res = query.fetch(1)
        if res:
            myProfile = res[0]
            if not myProfile.emailUpdateEach:
                continue
            if myProfile.emailUserLoginAddress:
                receiver_address = myUser.googleUser.email()
            else:
                receiver_address = myProfile.emailSpecifiedAddress
            sender_address = "Jumi Firmware Manager Admin <jumifiwaman10@googlemail.com>"
            subject = "New release available"
            body = """A new firmware has been released\n\tfor %s\n\tRelease number: %s\n\tFirmware Group: %s\n\nVisit http://jumifiwaman.appspot.com/ for updating.""" %(ud.device.name, release.version, fwg.name)
            mail.send_mail(sender_address, receiver_address, subject, body)   

