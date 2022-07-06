import asyncio
import os
import aiohttp.web
import json
import time
import aiohttp_debugtoolbar
from aiohttp_debugtoolbar import toolbar_middleware_factory

from datetime import datetime

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8480))
USERS = set()
VALUE = 0
DATA = set()

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})


def value_event():
    return json.dumps({"type": "value", "value": VALUE})


def data_event(data):
    dt = datetime.now()
    str_date_time = dt.strftime("%d-%m-%Y, %H:%M:%S")
    mess = "       [{0}]: {1}".format(str_date_time, data)
    return json.dumps({"type": "data", "value": mess})


async def testhandle(request):
    s = open('index.html', "r")
    return aiohttp.web.Response(text=s.read(), content_type='text/html')


async def broadcast(mess):
    global  USERS
    for user_ws in USERS:
        await user_ws.send_str(mess)


async def websocket_handler(request, *args, **kwargs):
    global VALUE, USERS
    print('Websocket connection starting')
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)
    if ws not in USERS:
        USERS.add(ws)
        await broadcast(value_event())
        await broadcast(users_event())

    print('Websocket connection ready')

    async for msg in ws:

        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                USERS.remove(ws)
                await ws.close()
            else:
                command = json.loads(msg.data)
                print(command)
                if command["action"] == "minus":
                    VALUE -= 1
                    await broadcast(value_event())
                if command["action"] == "plus":
                    VALUE += 1
                    await broadcast(value_event())
                if command["action"] == "data":
                    VALUE += 1
                    ss = command["data"]
                    await broadcast(data_event(command["data"]))
    USERS.remove(ws)
    await broadcast(users_event())
    print('Websocket connection closed')
    return ws

async def readed_data(app):
    while True:
        print("ssss")
        await asyncio.sleep(2)

async def start_background_tasks(app):
    app['redis_listener'] = app.loop.create_task(readed_data(app))

def main():
    queue = asyncio.Queue()
    app = aiohttp.web.Application(middlewares=[toolbar_middleware_factory])
    app['static_root_url'] = '/static'
    app["arduino_queue"] = asyncio.Queue()
    STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")
    app.router.add_static('/static/', path=STATIC_PATH, name='static')
    app.router.add_route('GET', '/', testhandle)
    app.router.add_route('GET', '/ws', websocket_handler)
    aiohttp_debugtoolbar.setup(app)
    aiohttp.web.run_app(app, host=HOST, port=PORT)

if __name__ == '__main__':
    main()