import logging
log = logging.getLogger(__name__)
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as MQTTsubscribe
import time
import asyncio

class Sensor():
    _on_rising_edge_flag = False
    _on_falling_edge_flag = False
    
    _on_rising_edge_cb = None
    _on_falling_edge_cb = None
    _on_state_change_cb = None
    
    def getState(self):
        return self.state
        
    async def __onConnect(self, client, userData, flags, rc):
        if rc == 0:
            topic = 'devices/io-expander/'+ str(self.networkId) +'/digital-input/'+ str(self.pin)
            self.sensorClient.subscribe(topic)
            self.connected=True
            log.info(self.name + " connected to pin " + str(self.pin))
        

    def __onMessage(self, client, userData, msg):
        
        value = msg.payload
        self.state = int(value)
        ret = ""
        
        if self.state == 1:
            self._on_rising_edge_flag = True
            if self._on_rising_edge_cb is not None:
                ret = self._on_rising_edge_cb()
        elif self.state ==0:
            self._on_falling_edge_flag = True
            if self._on_falling_edge_cb is not None:
                ret = self._on_faling_edge_cb()
        elif self._on_state_change_cb is not None:
            ret = self._on_state_change_cb()
        return ret
        
        

    def __init__(self, name, ipAddress, networkId, pin):
        self.connected=False
        self.networkId = networkId
        self.pin = pin
        self.name = name
        self.sensorClient = None
        self.sensorClient = mqtt.Client()
        self.sensorClient.on_connect = self.__onConnect
        self.sensorClient.on_message = self.__onMessage
        self.sensorClient.connect(ipAddress)
        self.sensorClient.loop_start()
        
        t0 = time.time()
        connection_timeout = 5 #timeout after 5 seconds
        while self.connected==False:
            if time.time()-t0 > 5:
                raise Exception("system timeout during connection to to {}".format(self.name))
                
            time.sleep(0.2)
    
    def register_on_rising_edge(self, cb):
        self._on_rising_edge_cb = cb
    def register_on_falling_edge(self, cb):
        self._on_falling_edge_cb = cb
    def register_on_value_change(self, cb):
        self._on_state_change_cb = cb
        
    #TODO: Add timeout or disconnect?
    def wait_for_rising_edge(self):
        #Wait for the rising edge flag to trigger True. 
        while self._on_rising_edge_flag == False:
            time.sleep(0.5)
        self._on_rising_edge_flag = False
        return
    
    def wait_for_falling_edge(self):
        #Wait for the rising edge flag to trigger True. 
        while self.wait_for_falling_edge == False:
            time.sleep(0.5)
        self.wait_for_falling_edge = False
        return