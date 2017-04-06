#!/usr/bin/env python3

import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap

class VariableResource(resource.Resource):
    def __init__(self):
        super(VariableResource, self).__init__()
        self.content = 0

    async def render_get(self, req):
        return aiocoap.Message(payload=self.content)

    async def render_put(self, req):
        print('PUT Payload: %s' % req.payload)
        temp = int(req.payload)
        if temp is None:
            e = "Expecting integer. Did not modify resource."
            return aiocoap.Message(payload=e)
        else:
            self.content = temp
            return aiocoap.Message(payload=self.content)

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-test-server").setLevel(logging.DEBUG)

def main():
        root = resource.Site()

        root.add_resource(('.well-known', 'core'), resource.WKCResource(root.get_resources_as_linkheader))

        root.add_resource(('var',), VariableResource())

        asyncio.Task(aiocoap.Context.create_server_context(root))

        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")

