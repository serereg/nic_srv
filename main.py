from aiohttp import web
import asyncio
import json
import logging
import re

from database.client import DBClient
from database.fixtures import FIXTURES
from database.models import db
from redis.client import RedisClient
from web.routes import ROUTES

#regexp = re.compile(r'\.js|\.png|\.jpg|index\.html')

class Server:

    def __init__(self, app):
        self._opc_clients = set()
        self.list_cooler = []
        self.num_ckt = 12
        for i in range(0, self.num_ckt + 1 + 1):
            self.list_cooler.append(cooler(i))
        app.add_routes([web.get('/', self.handle),
                        web.get('/{name}', self.handle)])
        app.router.add_get("/ws/opc", self.ws_opc_handler)  # for client opc exchange
        app.router.add_static("/static", "static")

        self.plc_link_wdt = 0
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
                self.plc_link_wdt = ckt_data['wdt']
                for k in range(1, self.num_ckt+1):
                    if (ckt_data['item']) == 'CKT'+str(k):
                        self.list_cooler[k].pv.Value = ckt_data['temperature']
                        self.list_cooler[k].sp = ckt_data['sp']
                        self.list_cooler[k].State = ckt_data['state']
                        self.list_cooler[k].update_state_on()
                        #self.list_cooler[k].StateOn = ckt_data['is_on']
        finally:
            self._opc_clients.discard(ws)

    async def _send_ws_command(self, **data):
        if not self._opc_clients:
            return
        data["type"] = "command"
        print(data)
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
                cur_cooler = self.list_cooler[t]
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
                    stron = ""
                    strflt = ""
                    stralarm = ""
                    for k in range(1, self.num_ckt+1):
                        strpv = strpv+str(self.list_cooler[k].GetPV())+";"
                        strsp = strsp+str(self.list_cooler[k].sp)+";"
                        stron = stron+str(self.list_cooler[k].isOn())+";"
                        strflt = strflt+str(self.list_cooler[k].isFault())+";"
                        stralarm = stralarm+str(self.list_cooler[k].isAlarm())+";"
                    strwdt = str(self.plc_link_wdt)+";"
                    return web.Response(text=strpv+strsp+stron+strflt+stralarm+strwdt)


async def db_connect(dsn, db):
    client = DBClient(dsn=dsn, db=db)
    await client.connect()
    await client.add_fixtures(FIXTURES)
    return client


async def redis_connect(host, port):
    client = RedisClient(hots=host, port=port)
    await client.connect()
    return client


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    app = web.Application()

    loop = asyncio.get_event_loop()
    db_client = loop.run_until_complete(db_connect("sqlite:///db.sqlite3", db))
    redis_client = loop.run_until_complete(redis_connect("localhost", 5679))

    app["redis"] = redis_client
    app["database"] = db_client

    for path, method, view in ROUTES:
        app.router.add_route(method, path, view)
    app.router.add_static("/static", "static")

    web.run_app(app)
