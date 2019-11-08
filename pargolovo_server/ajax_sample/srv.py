from aiohttp import web
from loguru import logger
from Cooler import Cooler

import asyncio

import re

regexp = re.compile(r'\.js|\.png|\.jpg|index\.html')

_opc_clients = set()

# Exschange with opc client
async def ws_opc_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    _opc_clients.add(ws)
    async for msg in ws:
        logger.info("opc msg {}", msg.data)
    _opc_clients.discard(ws)


async def _simulate_commands(self):
    import random
    while True:
        await asyncio.sleep(5)
        if not _opc_clients:
            continue
        cmd = dict(type="command", action=random.choice(["on", "off", "set"]),
                   item="node1", value=random.randint(-20, 20))
        logger.info("sending command {} to {} clients", cmd, len(_opc_clients))
        await asyncio.gather(*[ws.send_json(cmd) for ws in _opc_clients])

list_Cooler = []

async def handle(request):
    name = request.match_info.get('name')
    print(name)
    #text = "Hello, " + name
    for k in request.rel_url.query.keys():
        print(k+"="+request.rel_url.query[k])
    if name == None:
        return web.FileResponse('index.html')
    elif (regexp.search(name)): # == 'main.js' or name == 'CKT.png'
        return web.FileResponse(name)
    else:
        for t in range(1,13):
            print(t)
            cur_cooler = list_Cooler[t]
            if ('val'+str(t)) in request.rel_url.query.keys():
                cur_cooler.SetSP(request.rel_url.query['val'+ str(t)])
                print(str(t)+"/"+cur_cooler.sp)
                return web.Response(text='OK')
            elif ('cmd'+str(t)) in request.rel_url.query.keys():
                if request.rel_url.query['cmd' + str(t)] == 'YOn':
                    cur_cooler.YOn()
                    return web.Response(text='OK')
                if request.rel_url.query['cmd' + str(t)] == 'YOff':
                    cur_cooler.YOff()
                    return web.Response(text='OK')
            elif len(request.rel_url.query.keys())==0:
                strpv = ""
                strsp = ""
                strstate = ""
                for k in range(1,13):
                    strpv = strpv+str(list_Cooler[k].GetPV())+";"
                    strsp = strsp+str(list_Cooler[k].sp)+";"
                    strstate = strstate+str(list_Cooler[k].isOn())+";"
                return web.Response(text=strpv+strsp+strstate)
async def ws_browser_handler(self, request):
        pass

    
app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}',handle)])
app.router.add_get("/ws/opc", ws_opc_handler) # for client opc exchange

if __name__ == '__main__':
    for i in range(1,16):
        list_Cooler.append(Cooler(i))


    web.run_app(app)

