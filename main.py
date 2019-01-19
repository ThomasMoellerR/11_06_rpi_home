import threading
import time
import paho.mqtt.client as mqtt
import argparse
import os

def thread2():


    while True:
        pass



def thread1():
    global client

    while True:

        client.on_connect = on_connect
        client.on_message = on_message

        try_to_connect = True

        while try_to_connect:
            try:
                client.connect(args.mqtt_server_ip, int(args.mqtt_server_port), 60)
                try_to_connect = False
                break
            except Exception as e:
                print(e)



        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):

    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensors/get_lux")



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global thermostat_obj

    print(msg.topic + " "+ msg.payload.decode("utf-8"))

    if msg.topic == "sensors/get_lux":
        lux = int(msg.payload.decode("utf-8"))
        print("Lux: " + str(lux))

        # Wordclock
        m = 0.05
        b = 0

        output = m * lux + b

        if output > 1.0: output = 1.0
        output = round(output, 2)

        print("Wordclock: " + str(output))

        client.publish("wordclock/brightness", output, qos=0, retain=False)


        # Cube

        if lux >= 1:
            binary_brightness = 1
        else:
            binary_brightness = 0


        print("Cube: " + str(binary_brightness))

        client.publish("cube/brightness", binary_brightness, qos=0, retain=False)




# Argparse
parser = argparse.ArgumentParser()
parser.add_argument("--mqtt_server_ip", help="")
parser.add_argument("--mqtt_server_port", help="")

args = parser.parse_args()

client = mqtt.Client()

t1= threading.Thread(target=thread1)
t2= threading.Thread(target=thread2)

t1.start()
time.sleep(1)
t2.start()
