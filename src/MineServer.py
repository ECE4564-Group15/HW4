#!/usr/bin/env python3
# This will be the RESTful COAP interface into the
# Minecraft API. Here, requests will be handled from the three clients and processed.
# Request 1: Get an id (Returns id)
# Request 2: Get current posision of cursor (Returns {x,y,z,id})
# Request 3: Place Block (PUT {x,y,z,'type'})

#imports
from aiocoap import *
import aiocoap.resource as resource
import pickle
import logging
import asyncio
from MinecraftAPI import MinecraftAPI

#HERE WE WILL INCLUDE SimpleMineApi.py (needs to be able to place block and get location) (maybe move cursor to new location)

######

class IdResource(resource.Resource):
    #ctor
    def __init__(self):
        super(IdResource, self).__init__()
        self.currentId = 1

    #handler
    async def render_get(self, req):
        #response
        if self.currentId >= 4:
            self.currentId = int(-1)
            p = pickle.dumps(self.currentId)
            print('GET: Reply with %s'%self.currentId)
        elif self.currentId < 0:
            p = pickle.dumps(self.currentId)
            print('GET: Reply with %s'%self.currentId)
        else:
            p = pickle.dumps(self.currentId)
            print('GET: Reply with %s'%self.currentId)
            self.currentId = self.currentId + 1
        return Message(payload=p)

#handler class
class MinecraftResource(resource.Resource):
    #ctor
    def __init__(self):
        super(MinecraftResource, self).__init__()
        #data
        self.numblocks = 0
        self.position = {'x':0,'y':0,'z':0,'id':1}
        self.mc = MinecraftAPI()
        x, y, z = self.mc.getPlayerPosition()
        self.playerPosition = {'x':x, 'y':y ,'z':z}

    async def render_get(self, req):
        #response
        p = pickle.dumps(self.position)
        #print('GET: Reply with %s'%self.position)
        return Message(payload=p)

    async def render_put(self, req):
        #message
        message = pickle.loads(req.payload)
        if all(k in message for k in ('x','y','z','type')):
            #build stuff
            x = message['x'] + self.playerPosition['x']
            y = message['y'] + self.playerPosition['y']
            z = message['z'] + self.playerPosition['z']
            if message['type'] == 'yellow':
                stone = 1
                self.mc.setBlock(x, y, z, stone)
            elif message['type'] == 'blue':
                grass = 2
                self.mc.setBlock(x, y, z, grass)
            elif message['type'] == 'red':
                tnt = 46
                self.mc.setBlock(x, y, z, tnt)
            
            #then good
            #put_block(message)
            print('Placed: %s'%message)
            #put block down... increment by one, set positiono
            self.numblocks = self.numblocks + 1
            #next client
            if self.position['id'] < 3:
                self.position['id'] = self.position['id'] + 1
            else:
                self.position['id'] = 1
            #next pos
            if self.numblocks >= 20:
                self.position['id'] = 0
            elif self.position['x'] < 9:
                self.position['x'] = self.position['x'] + 1
            elif self.position['y'] < 1:
                self.position['x'] = 0
                self.position['y'] = self.position['y'] + 1
            p = pickle.dumps(True)
            return Message(payload=p)
        else:
            p = pickle.dumps(False)
            return Message(payload=p)

logging.basicConfig(level=logging.INFO)
logging.getLogger('mine-server').setLevel(logging.DEBUG)

def main():
        root = resource.Site()

        root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))

        root.add_resource(('mine',), MinecraftResource())

        root.add_resource(('id',), IdResource())

        asyncio.Task(Context.create_server_context(root))

        asyncio.get_event_loop().run_forever()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting...')
