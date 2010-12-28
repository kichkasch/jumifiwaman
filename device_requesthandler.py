from device import *
from google.appengine.ext import webapp
from google.appengine.ext.db import stats

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
        nrDevices = int(Device.all().count())
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
        sortList = ['deviceID','name']
        device_query = Device.all().order(directionSort + sortList[indexSort])
        i=0
        devices = device_query.fetch(numberRecords,  offset = startRecords)
        txt = '{"sEcho": ' + sEcho + ', "iTotalRecords": ' + str(nrDevices) + ', "iTotalDisplayRecords": '+ str(nrDevices) + ', "aaData":  ['
        for device in devices:
            if i:
                txt += ","
            txt += '["' + device.deviceID + '","' + device.name + '","' + device.group.name + '","' + device.manufactorer.name + '"]'
            i+=1            
        txt += ']}'
        self.response.out.write(txt)
        
class DevicesForGroup(webapp.RequestHandler):
    def get(self):
        query = DeviceGroup.all().filter('name = ', self.request.get('deviceGroup'))
        devgroup = query.fetch(1)[0]
        device_query = Device.all().filter('group = ',  devgroup)
        devices = device_query.fetch(100)
        txt = ''
        for device in devices:
            txt += '<option>' + device.name + '</option>'
        self.response.out.write(txt)

class DetailsForDevice(webapp.RequestHandler):
    def get(self):
        name = self.request.get('name')
        query = Device.all().filter('name = ', name)
        dev = query.fetch(1)[0]
        txt = "%s\n%s" %(dev.group.name, dev.manufactorer.name)
        self.response.out.write(txt)
