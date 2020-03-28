from aiohttp import web
import asyncio
import json
import logging


NUMBER_OF_COOLERS = 12


class OPCView(web.View):
    async def get(self):
        db_client = self.request.app["database"]
        redis_client = self.request.app["redis"]
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        async for message in ws:
            data = json.loads(message.data)
            cooler = db_client.get_cooler(name=data["item"])

            await redis_client.set_cooler_state(
                cooler_id=int(cooler.id),
                temperature=data["temperature"],
                set_point=data["set_point"],
                state=data["state"],
            )


class IndexView(web.View):
    async def get(self):
        return web.FileResponse("static/index.html")


class CoolerStateView(web.View):
    async def get(self):
        try:
            db_client = self.request.app["database"]
            redis_client = self.request.app["redis"]

            name = self.request.match_info["name"]
            if name != "":
                cooler = db_client.get_cooler(name=name)
                data = await redis_client.get_cooler_state(cooler_id=cooler.id)
                logging.debug(cooler.name)
                return web.json_response(data)
        except:
            pass
        

class CoolerAllStatusesView(web.View):
    async def get(self):
        db_client = self.request.app["database"]
        redis_client = self.request.app["redis"]
        CKT = []
        for i in range(NUMBER_OF_COOLERS):
            cooler = db_client.get_cooler(name = f"CKT{i+1}")
            data = await redis_client.get_cooler_state(cooler_id=cooler.id)
            CKT.append({
                            "pv": data.temperature, 
                            "sp": data.set_point, 
                            "is_reg_on": is_set(data.state, 0), 
                            "is_pv_fault": is_set(data.state, 1),
                            "is_reg_alarm": is_set(data.state, 2)
                        })
        all_statuses = json.dumps({"CKT":CKT, "plc_client_wdt" : 123})
        logging.info("----------" + all_statuses)
        return web.Response(text=all_statuses)


class CoolerCommandView(web.View):
    async def get(self):
        # for i in range(NUMBER_OF_COOLERS):
            # k = i + 1
            k = 1

            if self.request.rel_url.query['cmd'+str(k)]=="YOn":
                # await self._send_ws_command(
                #             command="YOn",
                #             target=cur_cooler.name,
                #         )
                #         cur_cooler.YOn()
                return web.Response(text='YOn')
            if self.request.rel_url.query['cmd'+str(k)]=="YOff":
                # await self._send_ws_command(
                #             command="YOff",
                #             target=cur_cooler.name,
                #         )
                #         cur_cooler.YOff()
                return web.Response(text='YOff')
            if ('val'+str(k)) in self.request.rel_url.query.keys():
                # cur_cooler.SetSP(self.request.rel_url.query['val'+ str(i)])
                # await self._send_ws_command(
                #         command="set_sp",
                #         value=cur_cooler.sp,
                #         target=cur_cooler.name,
                #     )
                return web.Response(text='val')


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
                # if ('val'+str(t)) in request.rel_url.query.keys():
                #     cur_cooler.SetSP(request.rel_url.query['val'+ str(t)])
                #     print(str(t)+"/"+cur_cooler.sp)
                #     await self._send_ws_command(
                #         command="set_sp",
                #         value=cur_cooler.sp,
                #         target=cur_cooler.name,
                #     )
                #     return web.Response(text='OK')
                # elif ('cmd'+str(t)) in request.rel_url.query.keys():
                #     if request.rel_url.query['cmd' + str(t)] == 'YOn':
                #         await self._send_ws_command(
                #             command="YOn",
                #             target=cur_cooler.name,
                #         )
                #         cur_cooler.YOn()
                #         return web.Response(text='OK')
                #     if request.rel_url.query['cmd' + str(t)] == 'YOff':
                #         await self._send_ws_command(
                #             command="YOff",
                #             target=cur_cooler.name,
                #         )
                #         cur_cooler.YOff()
                #         return web.Response(text='OK')
                # elif len(request.rel_url.query.keys())==0:
                #     strpv = ""
                #     strsp = ""
                #     stron = ""
                #     strflt = ""
                #     stralarm = ""
                #     for k in range(1, self.num_ckt+1):
                #         strpv = strpv+str(self.list_cooler[k].GetPV())+";"
                #         strsp = strsp+str(self.list_cooler[k].sp)+";"
                #         stron = stron+str(self.list_cooler[k].isOn())+";"
                #         strflt = strflt+str(self.list_cooler[k].isFault())+";"
                #         stralarm = stralarm+str(self.list_cooler[k].isAlarm())+";"
                #     strwdt = str(self.plc_link_wdt)+";"
                #     return web.Response(text=strpv+strsp+stron+strflt+stralarm+strwdt)


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


def is_set(x, n):
        try:
            r = (int(x) & 1 << int(n)) != 0
        except Exception:
            r = True
        return r