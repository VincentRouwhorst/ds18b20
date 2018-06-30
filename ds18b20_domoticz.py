#!/usr/bin/python
#--------------------------------------
#
#              ds18b20.py
#  Read DS18B20 1-wire temperature sensor
#
# Author : Matt Hawkins
# Date   : 10/02/2015
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------
#
# Addition for updating to Domoticz
#
# Author : Vincent Rouwhorst
# Date   : 30/06/2018
#
# Domoticz Json documentation
# https://www.domoticz.com/wiki/Domoticz_API/JSON_URL's#Custom_Sensor
#--------------------------------------

import requests

DOMOTICZ_IP = 'http://127.0.0.1:8080'

def gettemp(id):
  try:
    mytemp = ''
    filename = 'w1_slave'
    f = open('/sys/bus/w1/devices/' + id + '/' + filename, 'r')
    line = f.readline() # read 1st line
    crc = line.rsplit(' ',1)
    crc = crc[1].replace('\n', '')
    if crc=='YES':
      line = f.readline() # read 2nd line
      mytemp = line.rsplit('t=',1)
    else:
      mytemp = 99999
    f.close()

    return int(mytemp[1])

  except:
    return 99999

if __name__ == '__main__':
  # Script has been called directly

  while True:
     id = '28-0315902e73ff'
     idx = str(333)
     #print "Temp Aquarium : " + '{:.3f}'.format(gettemp(id)/float(1000))
     temp = str((gettemp(id)/float(1000)))
     #print(DOMOTICZ_IP + "/json.htm?type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue=" + temp)
     requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue=" + temp)

     id = '28-0315a87126ff'
     idx = str(332)
     #print "Temp Aquarium koeler warm : " + '{:.3f}'.format(gettemp(id)/float(1000))
     temp = str((gettemp(id)/float(1000)))
     #print(DOMOTICZ_IP + "/json.htm?type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue=" + temp)
     requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue=" + temp)

     id = '28-0315a88e3bff'
     idx = str(331)
     #print "Temp1 : " + '{:.3f}'.format(gettemp(id)/float(1000))
     temp = str((gettemp(id)/float(1000)))
     #print(DOMOTICZ_IP + "/json.htm?type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue=" + temp)
     requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue=" + temp)
