from device import *
from google.appengine.ext import webapp

class AddDevice(webapp.RequestHandler):
    def post(self):
        device = Device()
        device.name = self.request.get('deviceName')
        device.deviceID = self.request.get('deviceID')
        query = DeviceGroup.all().filter('name = ', self.request.get('deviceGroup'))
        device.group = query.fetch(1)[0]
        query = Manufactorer.all().filter('name = ', self.request.get('manufactorer'))
        device.manufactorer = query.fetch(1)[0]
        device.put()

class AddDeviceGroup(webapp.RequestHandler):
    def post(self):
        group = DeviceGroup()
        group.name = self.request.get('groupName')
        group.put()        

class AddManufactorer(webapp.RequestHandler):
    def post(self):
        man = Manufactorer()
        man.name = self.request.get('manName')
        man.website = self.request.get('manWebsite')
        man.put()

class RemoveManufactoer(webapp.RequestHandler):
    def post(self):
        query = Manufactorer.all().filter('name = ', self.request.get('manufactorer'))
        manufactorer = query.fetch(1)[0]
        manufactorer.delete()


class Devices(webapp.RequestHandler):
    def get(self):
        sEcho = self.request.get('sEcho')
        numberRecords = self.request.get('iDisplayLength')
        startRecords = self.request.get('iDisplayStart')
        try:
            indexSort = int(self.request.get('iSortCol_0'))
        except:
            indexSort = 0
        directionSort = self.request.get('sSortDir_0')
        if directionSort.strip().lower() == "desc":
            directionSort = "-"
        else:
            directionSort = ""
        sortList = ['deviceID','name']        
        device_query = Device.all().order(directionSort + sortList[indexSort])
        i=0
        devices = device_query.fetch(100)
        txt = '{"sEcho": ' + sEcho + ', "iTotalRecords": ' + str(len(devices)) + ', "iTotalDisplayRecords": '+ str(len(devices)) + ', "aaData":  ['
        for device in devices:
            if i:
                txt += ","
            txt += '["' + device.deviceID + '","' + device.name + '","' + device.group.name + '","' + device.manufactorer.name + '"]'
            i+=1            
        txt += ']}'
        self.response.out.write(txt)
