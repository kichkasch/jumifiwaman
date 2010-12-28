from myuser import *
from device import Device
from firmware import FirmwareGroup, Firmware
from google.appengine.ext import webapp
from google.appengine.api import users

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
            txt += '["' + device.device.name + '","' + device.device.manufactorer.name + '","' + fwgName+ '","' + 'n.a.'+  '","' +'n.a.' +  '","' + fwgLatest+ '"]'
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
