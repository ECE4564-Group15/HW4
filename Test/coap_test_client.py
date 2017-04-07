#!/usr/bin/env python3
import logging
import asyncio
import pickle

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def do_get(proto,uri):
    request = Message(code=GET,uri=uri)

    try:
        res = await proto.request(request).response
    except TypeError as e:
        pass
    except Exception as e:
        print("Failed GET")
        print(e)
    finally:
        p = pickle.loads(res.payload)
        print("GET Res: %s\n%s"%(str(res.code),str(p)))
        return p

async def do_put(proto,uri,payload):
    p = pickle.dumps(payload)
    req = Message(code=PUT,uri=uri,payload=p)

    try:
        res = await proto.request(req).response
    except TypeError as e:
        pass
    except Exception as e:
        print("Failed PUT")
        print(e)
    finally:
        p = pickle.loads(res.payload)
        print("PUT Res: %s\n%s"%(str(res.code),str(p)))


async def main():
    proto = await Context.create_client_context()

    t = await do_get(proto,'coap://localhost/var')
    t = (t[0]+1,)
    await do_put(proto,'coap://localhost/var',t) 
    await do_get(proto,'coap://localhost/var')
if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        print("Exiting...")
