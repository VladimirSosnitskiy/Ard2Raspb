#!/usr/bin/env python
import asyncio
import json
import serial

import websockets
import random

async def hello():
    sdata = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1.0)
    await asyncio.sleep(2)
    sdata.reset_input_buffer()
    print("Arduino is Connected")
    async with websockets.connect('ws://localhost:8480/ws') as websocket:
        while True:
            if sdata.in_waiting > 0:
                mydata = sdata.readline().decode("utf-8").rstrip()
                print(mydata)
                name = json.dumps({"action": "data", "data": mydata})
                await websocket.send(name)
            await asyncio.sleep(0.1)

asyncio.get_event_loop().run_until_complete(hello())