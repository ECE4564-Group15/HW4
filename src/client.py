#!/usr/bin/env python3

from MineCoapClient import CoapClient
import asyncio

def main():
    run = asyncio.get_event_loop().run_until_complete
    client = CoapClient()
    #must run
    run(client.connect())
    #id
    id_uri = 'coap://localhost/id'
    m_uri = 'coap://localhost/mine'
    #get the id
    my_id = run(client.get(id_uri))
    colors = ['','blue','red','yellow']
    while True:
        #get current id
        pos = run(client.get(m_uri))
        if pos['id'] == 0:
            break
        elif pos['id'] != my_id:
            continue
        else:
            pos.pop('id')
            pos['type'] = colors[my_id]
            res = run(client.put(m_uri,pos))
            print(res)
main()
