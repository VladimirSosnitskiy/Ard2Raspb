#!/usr/bin/env python

# WS client example

import asyncio
import json

import websockets
import random

async def hello():
    async with websockets.connect('ws://localhost:8480/ws') as websocket:
        while True:
            name = random.randrange(1,1000, 4)
            name = json.dumps({"action": "data", "data": name})
            await websocket.send(name)
            print(f"> {name}")
            await asyncio.sleep(2)

        #greeting = await websocket.recv()
        #print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())