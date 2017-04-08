#!/usr/bin/env python3
# This will be the RESTful COAP interface into the
# Minecraft API. Here, requests will be handled from the three clients and processed.
# Request 1: Get an id (Returns id)
# Request 2: Get current posision of cursor (Returns {x,y,z,id})
# Request 3: Place Block (PUT {x,y,z,'type'})

#imports
from aiocoap import *
import pickle
import logging
import asyncio

#HERE WE WILL INCLUDE SimpleMineApi.py (needs to be able to place block and get location) (maybe move cursor to new location)

######

class IdResource(resource.Resource):
    #ctor
    def __init__(self):
        super(IdResource, self).__init__()
        self.currentId = 0

    #handler
    async def render_get(self, req):
        #response
        if self.currentId >= 3:
            p = pickle.dumps(int(-1))
        else:
            p = pickle.dumps(self.currentId)
            self.currentId = self.currentId + 1
        return Message(payload=p)

#handler class
class MinecraftResource(resource.Resource):
    #ctor
    def __init__(self):
        super(MinecraftResource, self).__init__()
        #data
        self.numblocks = 0
        self.position = {'x':0,'y':0,'z':0,'id':0}
        
    async def render_get(self, req):
        #response
        p = pickle.dumps(self.position)
        print('GET: Reply with %s'%self.position)
        return Message(payload=p)

logging.basicConfig(level=logging.INFO)
logging.getLogger('mine-server').setLevel(logging.DEBUG)

def main():
        root = resource.Site()

        root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))

        root.add_resource(('minecraft',), MinecraftResource())

        root.add_resource(('id',), IdResource())

        asyncio.Task(aiocoap.Context.create_server_context(root))

        asyncio.get_event_loop().run_forever()
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting...')
