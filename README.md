# ds18b20
Domoticz update script for DS18B20 sensors

Three sensors:
These value's are different for all sensors.
idx = 333 temp aq = 28-0315902e73ff  
idx = 332 temp aq koeler = 28-0315a87126ff  
idx = 331 temp 1 = 28-0315a88e3bff

Add script to crontap -e
@reboot python /<path>/ds18b20_domoticz.py
