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
# Date   : 21/07/2018
#
# Domoticz Json documentation
# https://www.domoticz.com/wiki/Domoticz_API/JSON_URL's#Custom_Sensor
#--------------------------------------

import requests
import time

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

# temp min and max value incase of a sensor error
  min = 10.0
  max = 60.0
  #id_list = ['28-0315902e73ff', '28-0315a87126ff', '28-0315a88e3bff']
  #id_name = ['Temp Aquarium : ', 'Temp Aquarium koeler warm : ', 'Temp1 :']
  #idx_list = ['333', '332', '331']
  id_list = ['28-0315902e73ff']
  id_name = ['Temp Aquarium : ']
  idx_list = ['1129']
  
  while True:
     loopcounter = 0
     for id in id_list:
	print id_name[loopcounter] + '{:.3f}'.format(gettemp(id)/float(1000))
        temp = gettemp(id)/float(1000)
        #print('temp : ', temp)
        if temp >= min and temp <= max:
	   print(DOMOTICZ_IP + "/json.htm?type=command&param=udevice&idx=" + idx_list[loopcounter] + "&nvalue=0&svalue=" + str(temp))
           r = requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=udevice&idx=" + idx_list[loopcounter] + "&nvalue=0&svalue=" + str(temp))
	   siteresponse = r.json()
           if siteresponse["status"] == 'OK':
		print('Response = OK')
	   if siteresponse["status"] == 'ERR':
		# Write to Domoticz log
		message = "ERROR writing sensor " + id_name[loopcounter]
		print(message)
		requests.get(DOMOTICZ_IP + "/json.htm?type=command&param=addlogmessage&message=" + message)
        loopcounter += 1
