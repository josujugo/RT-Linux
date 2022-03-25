import pyqtgraph as pqt
import numpy as np
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt

topics = ['#']
broker="raspberrypi.local"
#mqttc = mqtt.Client()
#mqttc.connect(broker, 1883, 60)
ii=0


class MyMQTTClass(mqtt.Client):

    def __init__(self, broker="localhost", topics="#"):
        mqtt.Client.__init__(self)
        self.connect(broker, 1883, 60)
        self.subscribe(topics, 0)

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))

    def on_connect_fail(self, mqttc, obj):
        print("Connect failed")

    def on_message(self, mqttc, obj, msg):
        g.insert(eval(msg.payload))
        #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    #def on_log(self, mqttc, obj, level, string):
        #pass
        #print(string)

    def run(self):


        rc = self.loop()
        return rc


# If you want to use a specific client id, use
# mqttc = MyMQTTClass("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = MyMQTTClass(broker)


class Gdata:

     def __init__(self, plot, N=200):
             self.ii=0
             self.data=np.zeros((1,N))
             self.plot=plot
             self.N=N
     def insert(self,value):
             self.data= np.append(self.data, value)
             self.data= np.delete(self.data, 0)
             self.ii = np.mod(self.ii+1,self.N)
     def update(self):
             if self.ii==0:
                     self.plot.clear()
                     self.plot.plot(self.data[0])
g=Gdata(pqt.plot(), N=1800)



def graph():
     global ii
     ii+=1
     g.plot.clear()
     a=g.plot.plot(g.data.reshape(1800,))
     if ii%20==0:
         pqt.QtGui.QApplication.processEvents()

def on_message(mqttc, obj, msg):
    #print(eval(msg.payload))
    g.insert(eval(msg.payload))
    #graph()
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


mqttc.on_message = on_message
#mqttc.subscribe("sea/test",1)
#mqtt0c.loop_forever()


#while True:
     #rc = mqttc.run()
     #print(g.data)
#     graph()
#     mqttc.run()

     #¡¡graph()
     #m=mqttc.subscribe("sea/test",0)
     #print(m)
     #m = subscribe.simple(topics, hostname="raspberrypi.local", retained=False)
     #g.insert(eval(m.payload))
