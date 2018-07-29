# ds18b20
Domoticz update script for DS18B20 sensors

Three sensors:
These value's are different for all sensors.
# list of sensors to process, loopcounter gives position value
id_list = ['28-0315902e73ff', '28-0315a87126ff', '28-0315a88e3bff']
id_name = ['Temp Aquarium : ', 'Temp Aquarium koeler warm : ', 'Temp1 :']
idx_list = ['333', '332', '331']

# temp min and max value incase of a sensor error
min = 10.0
max = 60.0

Add script to crontap -e
@reboot python /<path>/ds18b20_domoticz.py
