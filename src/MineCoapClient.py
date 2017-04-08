#!/usr/bin/env python3
# This will be the RESTful coap connection to the minecrat server
# This module will export a class that creates a coap context when created,
# then is able to handle requests for the user.
# Request 1: Get an id from the server
# Request 2: Get the current position and turn id from the server
# Request 3: Post a new block to the server

#imports
from aiocoap import *
import pickle
import logging
import asyncio

#must await...
class CoapClient():
    #ctor
    def __init__(self):
        pass
    
    async def connect(self):
        self.proto = await Context.create_client_context()
        print('Connected')
        
    async def do_get(self,uri):
        req = Message(code=GET,uri=uri)

        try:
            res = await self.proto.request(req).response
        except TypeError as e:
            pass
        except Exception as e:
            print("Failed GET")
            print(e)
            return None
        finally:
            p = pickle.loads(res.payload)
            return p

    async def do_put(self,uri,data):
        p = pickle.dumps(data)
        req = Message(code=PUT,uri=uri,payload=p)

        try:
            res = await self.proto.request(req).response
        except TypeError as e:
            pass
        except Exception as e:
            print("Failed PUT")
            print(e)
            return None
        finally:
            p = pickle.loads(res.payload)
            return p

    async def get(self,uri):
        return await self.do_get(uri)

    async def put(self,uri,data):
        return await self.do_put(uri,data)

if __name__ == '__main__':
    run = asyncio.get_event_loop().run_until_complete
    
    c = CoapClient()
    run(c.connect())
    uri = 'coap://localhost/id'
    t = run(c.get(uri))
    print('Got %s'%t)
    uri = 'coap://localhost/mine'
    t = run(c.get(uri))
    print('Got %s'%t)
    t.pop('id')
    t['type'] = 'yellow'
    t = run(c.put(uri,t))
    print(t)
