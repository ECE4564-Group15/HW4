#!/usr/bin/env python3

from MineCoapClient import CoapClient
import sys
import asyncio

def main():
    client = CoapClient()
    #must run
    client.connect()
    #id
    if len(sys.argv) < 2:
        print('No host specified. Assuming localhost')
        base_uri = 'coap://localhost/'
    else:
        base_uri = 'coap://' + sys.argv[1] + '/'
    id_uri = base_uri + 'id'
    m_uri = base_uri + 'mine'
    #id_uri = 'coap://localhost/id'
    #m_uri = 'coap://localhost/mine'
    
    #get the id
    my_id = client.get(id_uri)
    colors = ['','blue','red','yellow']
    while True:
        #get current id
        pos = client.get(m_uri)
        if pos['id'] == 0:
            break
        elif pos['id'] != my_id:
            continue
        else:
            pos.pop('id')
            pos['type'] = colors[my_id]
            res = client.put(m_uri,pos)
            print(res)
main()
