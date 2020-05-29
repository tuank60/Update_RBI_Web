
import datetime
import time
import json
import paho.mqtt.client as mqtt
from cloud import models
THINGSBOARD_HOST = "demo.thingsboard.io"

class Subscribe_thingsboard:
    def __init__(self,componentID):
        self.componentID=componentID

    def SubDATA(self):
        try:
            client = mqtt.Client()
            client.username_pw_set("K6BEkJp2NbDSNjq87VVe")
            client.connect(THINGSBOARD_HOST, 1883)
            client.on_connect =self.on_connect
            client.subscribe('v1/devices/me/attributes', 0)
            client.on_message = self.on_message
            rc = 0
            while rc == 0:
                rc = client.loop()
            # print('Result code: ' + str(rc))
            time.sleep(10)
            self.SubDATA()
        except Exception as e:
            print(e)

    def PushData(self):
        try:
            data1 = {"send_data = json.dumps(data1)":12}
            # THINGSBOARD_HOST = "demo.thingsboard.io"
            client = mqtt.Client()
            client.username_pw_set("K6BEkJp2NbDSNjq87VVe")
            client.connect(THINGSBOARD_HOST, 1883)
            client.publish('v1/devices/me/attributes', json.dumps(data1))
            time.sleep(5)
        except Exception as e:
            print(e)


    def on_connect(client, userdata, flags, rc):
        print("Result code " + str(rc))
        if(rc == 0):
            print("Result code " + str(rc) + ": good connection")
        else:
            print("Result code " + str(rc) + ": authentication error")

    def SUBTHINGSBOARD(self):
        THINGSBOARD_HOST = "demo.thingsboard.io"
        ACCESS_TOKEN = models.ZSensor.objects.filter(Componentid=self.componentID)[0].Token
        print(ACCESS_TOKEN)
        client = mqtt.Client()
        client.username_pw_set(ACCESS_TOKEN)
        client.connect(THINGSBOARD_HOST, 1883)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.loop_forever(1)

    def on_connect(self,client, userdata, rc, *extra_params):
        print("Connected with result code "+str(rc))
        sensor_data = {"id": 1, "device": "Device A2", "client": 1, "key": "attribute1"}
        client.publish('v1/devices/me/attributes/request/1', json.dumps(sensor_data))

    def on_message(self,client, userdata, msg):
        payload = msg.payload.decode()
        data = json.loads(payload)
        print(data['client'])
        sensor = models.ZSensor.objects.filter(Componentid=self.componentID)[0].idsensor
        package = models.PackageSensor(idsensor_id=sensor, package=json.dumps(data['client']))
        package.save()
        client.disconnect()

if __name__=="__main__":
    a = Subscribe_thingsboard(1)
    a.SubDATA()
    # PushData()