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
        self.run = asyncio.get_event_loop().run_until_complete
    
    #this must be run immediatly after init in order to operate
    async def do_connect(self):
        self.proto = await Context.create_client_context()

    def connect(self):
        self.run(self.do_connect())        
        print('Connected')

    #perform a get
    async def do_get(self,uri):
        #message object
        req = Message(code=GET,uri=uri)
        #perform request
        try:
            res = await self.proto.request(req).response
        except TypeError as e:
            pass
        except Exception as e:
            print("Failed GET")
            print(e)
            return None
        finally:
            #get the result
            p = pickle.loads(res.payload)
            return p

    #perfor a put
    async def do_put(self,uri,data):
        #encode the data
        p = pickle.dumps(data)
        #create message
        req = Message(code=PUT,uri=uri,payload=p)
        #perform the request
        try:
            res = await self.proto.request(req).response
        except TypeError as e:
            pass
        except Exception as e:
            print("Failed PUT")
            print(e)
            return None
        finally:
            #return data
            p = pickle.loads(res.payload)
            return p
    #public wrappers
    def get(self,uri):
        return self.run(self.do_get(uri))

    def put(self,uri,data):
        return self.run(self.do_put(uri,data))

#test program if this is run standalone
if __name__ == '__main__':
    c = CoapClient()
    c.connect()
    uri = 'coap://localhost/id'
    t = c.get(uri)
    print('Got %s'%t)
    uri = 'coap://localhost/mine'
    t = c.get(uri)
    print('Got %s'%t)
    t.pop('id')
    t['type'] = 'yellow'
    t = c.put(uri,t)
    print(t)
