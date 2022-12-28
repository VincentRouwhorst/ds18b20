#!/usr/bin/python3
# python 3.6

import random
import time
import statistics

from paho.mqtt import client as mqtt_client

# def average var
LoopCounter = -1
Numbers = [[],[],[],[]]

# MQTT settings
broker = '127.0.0.1'
port = 1883
#topic = "python/mqtt"
topic = "domoticz/in"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'your-username'
password = 'your-password'

# Sensors settings
# temp min and max value incase of a sensor error
min = 10.0
max = 60.0
# list of sensors to process, loopcounter gives position value
# old id_list = ['28-0315902e73ff', '28-0315a87126ff', '28-0315a88e3bff']
id_list = ['28-0317303a5bff', '28-0315a87126ff', '28-0315a88e3bff', '28-0517608afdff']
id_name = ['Temp Aquarium : ', 'Temp Aquarium koeler warm : ', 'Temp1 : ', 'Temp-licht : ']
idx_list = ['333', '332', '331', '7391']

def average(x, i):
    global LoopCounter
    # max memory positions
    max = 4
    # number of digits to return
    digits = 2
    if LoopCounter >= 0 and LoopCounter < max-1:
        LoopCounter +=1
    elif LoopCounter >= max-1 or LoopCounter == -1:
        LoopCounter = 0
    #fill list
    if len(Numbers[i]) < max:
        Numbers[i].insert(LoopCounter, x)
    elif len(Numbers[i]) == max:
        Numbers[i][LoopCounter] = x
    result = round(statistics.mean(Numbers[i]), digits)
    #print(i)
    #print(Numbers[i])
    #print(result)
    return result

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


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


def publish(client):
    while True:
        loopcounter = 0
        for id in id_list:
            #print id_name[loopcounter] + '{:.3f}'.format(gettemp(id)/float(1000))
            temp = gettemp(id)/float(1000)
            print('temp : ', temp)
            # filter temp min and max value incase of a sensor error
            if temp >= min and temp <= max:
                #msg = f"messages: {msg_count}"
                begin_sl_char = "{"
                end_sl_char = "}"
                msg = f"{begin_sl_char}\"idx\" : {idx_list[loopcounter]}, \"nvalue\" : 0,  \"svalue\" : \"{str(average(temp, loopcounter))}\"{end_sl_char}"
                result = client.publish(topic, msg)
                # result: [0, 1]
                status = result[0]
                if status == 0:
                    print(f"Send `{msg}` to topic `{topic}`")
                else:
                    print(f"Failed to send message to topic {topic}")
            loopcounter += 1
        time.sleep(1)


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
