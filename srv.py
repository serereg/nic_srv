from aiohttp import web
from loguru import logger
from Cooler import Cooler

print(Cooler)
import asyncio

import json

import re

#regexp = re.compile(r'\.js|\.png|\.jpg|index\.html')
logger.info("test")

class Server:

    def __init__(self, app):
        self._opc_clients = set()
        self.list_Cooler = []
        self.num_ckt = 12
        for i in range(1, self.num_ckt + 1 + 1):
            self.list_Cooler.append(Cooler(i))
        app.add_routes([web.get('/', self.handle),
                        web.get('/{name}', self.handle)])
        app.router.add_get("/ws/opc", self.ws_opc_handler)  # for client opc exchange
        app.router.add_static("/static", "static")

    # Exchange with opc client
    async def ws_opc_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self._opc_clients.add(ws)
        try:
            async for msg in ws:
                #logger.info("opc msg {}", msg.data)
                print(msg.data)
                ckt_data = json.loads(msg.data)
                for k in range(1, self.num_ckt+1):
                    if (ckt_data['item']) == 'CKT'+str(k):
                        self.list_Cooler[k].pv.Value = ckt_data['temperature']
        finally:
            self._opc_clients.discard(ws)

    async def _send_ws_command(self, **data):
        if not self._opc_clients:
            return
        data["type"] = "command"
        coros = [ws.send_json(data) for ws in self._opc_clients]
        await asyncio.gather(*coros, return_exceptions=True)

    # async def _simulate_commands(self):
    #     import random
    #     while True:
    #         await asyncio.sleep(5)
    #         if not _opc_clients:
    #             continue
    #         cmd = dict(type="command", action=random.choice(["on", "off", "set"]),
    #                    item="node1", value=random.randint(-20, 20))
    #         logger.info("sending command {} to {} clients", cmd, len(_opc_clients))
    #         await asyncio.gather(*[ws.send_json(cmd) for ws in _opc_clients])


    async def handle(self, request):
        name = request.match_info.get('name')
        print(name)
        # for k in request.rel_url.query.keys():
        #     print(k+"="+request.rel_url.query[k])
        if name is None:
            return web.FileResponse('static/index.html')
        else:
            for t in range(1, self.num_ckt+1):
                print(t)
                cur_cooler = self.list_Cooler[t]
                if ('val'+str(t)) in request.rel_url.query.keys():
                    cur_cooler.SetSP(request.rel_url.query['val'+ str(t)])
                    print(str(t)+"/"+cur_cooler.sp)
                    await self._send_ws_command(
                        command="set_sp",
                        value=cur_cooler.sp,
                        target=cur_cooler.name,
                    )
                    return web.Response(text='OK')
                elif ('cmd'+str(t)) in request.rel_url.query.keys():
                    if request.rel_url.query['cmd' + str(t)] == 'YOn':
                        await self._send_ws_command(
                            command="YOn",
                            target=cur_cooler.name,
                        )
                        cur_cooler.YOn()
                        return web.Response(text='OK')
                    if request.rel_url.query['cmd' + str(t)] == 'YOff':
                        await self._send_ws_command(
                            command="YOff",
                            target=cur_cooler.name,
                        )
                        cur_cooler.YOff()
                        return web.Response(text='OK')
                elif len(request.rel_url.query.keys())==0:
                    strpv = ""
                    strsp = ""
                    strstate = ""
                    for k in range(1, self.num_ckt+1):
                        strpv = strpv+str(self.list_Cooler[k].GetPV())+";"
                        strsp = strsp+str(self.list_Cooler[k].sp)+";"
                        strstate = strstate+str(self.list_Cooler[k].isOn())+";"
                    return web.Response(text=strpv+strsp+strstate)


if __name__ == '__main__':
    app = web.Application()
    server = Server(app)
    web.run_app(app)

