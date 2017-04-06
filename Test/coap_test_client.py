#!/usr/bin/env python3
import logging
import asyncio

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def do_get(proto,uri):
    req = Message(code=GET,uri=uri)

    try:
        res = await proto.request(req).response
    except Exception as e:
        print("Failed GET")
        print(e)
    else:
        print("GET Res: %s\n%r"%(res.code,res.payload))

async def do_put(proto,uri,payload):
    req = Message(code=PUT,uri=uri,payload=payload)

    try:
        res = await proto.request(req).response
    except Exception as e:
        print("Failed PUT")
        print(e)
    else:
        print("PUT Res: %s\n%r"%(res.code,res.payload))


async def main():
    proto = await Context.create_client_context()

    do_get(proto,'coap://localhost/var')
    do_put(proto,'coap://localhost/var',1) 
    do_get(proto,'coap://localhost/var')
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    
