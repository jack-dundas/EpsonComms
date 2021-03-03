import logging
import asyncio

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2

async def get_request(client):
    async with client.subscribe(topic) as msg:
        try:
            resp = await msg
            text = resp.publish_packet.payload.data
            print(text)
        except Exception as e:
            return e
        else:
            return url, resp

class Sensor():
    
    def __init__(self, pin, ipAddress, networkId, asyncio_loop):
        self.loop = asyncio_loop
        self.pin = pin
        self.networkId = networkId
        self.ipAddress = ipAddress
        self.topic = 'devices/io-expander/{id}/digital-input/{pin}'.format(id=self.networkId, pin=self.pin)
        self.client = MQTTClient()

    async def run():
        self.initialized = self.loop.call_soon(self.initialize)
    
    async def initialize(self):
        await self.client.connect(self.ipAddress)
        await self.client.subscribe(self.topic)
        
    def get_state(self):
        msg = self.client.deliver_message()
        
        return msg
        
        

# async def uptime_coro():
#     C = MQTTClient()
#     await C.connect('192.168.7.2')
#     await C.subscribe([
#             ('$SYS/broker/uptime', QOS_1),
#             ('$SYS/broker/load/#', QOS_2),
#          ])
#     try:
#         for i in range(1, 100):
#             message = await C.deliver_message()
#             packet = message.publish_packet
#             print("%d:  %s => %s" % (i, packet.variable_header.topic_name, str(packet.payload.data)))
#         await C.unsubscribe(['$SYS/broker/uptime', '$SYS/broker/load/#'])
#         await C.disconnect()
#     except ClientException as ce:
#         logger.error("Client exception: %s" % ce)

# def test():
#     print("hello")

# async def printSensor():
#     loop = asyncio.get_event_loop()
#     await box_sensor.initialize()
#     future = loop.run_in_executor(None, box_sensor.get_state)
#     # future = loop.run_in_executor(None, test)
#     response = await future
#     print(response)

async def print_sensor():
    loop = asyncio.new_event_loop()
    try:
        client = MQTTClient()
        topic = 'devices/io-expander/{id}/digital-input/{pin}'.format(id=1, pin=0)
        
        await client.connect("192.168.7.2")
        await client.subscribe(self.topic)
        msg = await get_request(client)
        print(msg)
    finally:
        loop.close()
        
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_sensor())
    
    
