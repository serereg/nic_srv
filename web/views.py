import asyncio
import logging

from aiohttp import web

from .utils import HTTPView, JSONRPCView, WSView


NUMBER_OF_COOLERS = 12
STATE_IS_ON = 0
STATE_IS_FAULT = 1
STATE_IS_ALARM = 2


class WSOPCView(JSONRPCView, WSView):
    async def state(self, item, temperature, set_point, state):
        self.request.app["ws_opc_client"] = self.ws

        db_client = self.request.app["database"]
        redis_client = self.request.app["redis"]

        cooler = db_client.get_cooler(name=item)
        if cooler is None:
            return None, f"No cooler with name '{item}' in database"

        await redis_client.set_cooler_state(
            cooler_id=int(cooler.id),
            temperature=temperature,
            set_point=set_point,
            state=state,
        )

        return "ok", None


class WSClientView(JSONRPCView, WSView):
    @JSONRPCView.login_required
    async def state(self):
        result = []
        for cooler in db_client.get_coolers():
            data = await redis_client.get_cooler_state(cooler_id=cooler.id)
            if data:
                result.append({
                    "id": cooler.id,
                    "description": cooler.description,
                    "pv": data["temperature"], 
                    "sp": data["set_point"], 
                    "is_reg_on": is_set(data["state"], STATE_IS_ON), 
                    "is_pv_fault": is_set(data["state"], STATE_IS_FAULT),
                    "is_reg_alarm": is_set(data["state"], STATE_IS_ALARM),
                })

        return result, None

    @JSONRPCView.login_required
    async def command(self, command, params):
        ws = self.request.app["ws_opc_client"]
        data = {"test_data": "post"}
        await ws.send_json({"CKT": 1, "plc_client_wdt": 123})

        return "ok", None

    @JSONRPCView.login_required
    async def set_description(self, id, description):
        db_client = self.request.app["database"]
        
        cooler = db_client.get_cooler(id=id)
        if cooler is None:
            return None, f"No cooler with name '{item}' in database"
        cooler.description = description
        db_client.session.commit()

        return "ok", None


class APIClientView(JSONRPCView, HTTPView):
    def login(self, username, password):
        db_client = self.request.app["database"]
        user = db_client.get_user(username=username, password=password)
        if user is None:
            return None, "Incorrect username or password"

        session = db_client.create_session(user)

        return {"token": session.token}, None

    @JSONRPCView.login_required
    def logout(self):
        self.session.delete()
        self.request.app["database"].commit()


class IndexView(web.View):
    async def get(self):
        return web.FileResponse("static/index.html")



class CoolerAllStatesView(web.View):
    async def get(self):
        db_client = self.request.app["database"]
        redis_client = self.request.app["redis"]

        CKT = []
        for cooler in db_client.get_coolers():
            data = await redis_client.get_cooler_state(cooler_id=cooler.id)
            if data:
                CKT.append({
                    "id": cooler.id,
                    "pv": data["temperature"], 
                    "sp": data["set_point"], 
                    "is_reg_on": is_set(data["state"], STATE_IS_ON), 
                    "is_pv_fault": is_set(data["state"], STATE_IS_FAULT),
                    "is_reg_alarm": is_set(data["state"], STATE_IS_ALARM),
                })
        all_statuses = json.dumps({"CKT": CKT, "plc_client_wdt": 123})
        return web.Response(text=all_statuses)


class CoolerCommandView(web.View):
    async def get(self):
        for i in range(12):
            cmd_key = 'cmd'+str(i + 1)
            val_key = 'val'+str(i + 1)
            if cmd_key in self.request.rel_url.query.keys():
                if self.request.rel_url.query[cmd_key] == "YOn":
                    await self._send_ws_command(
                                command="YOn",
                                target=f"CKT{i+1}",
                            )
                    #         cur_cooler.YOn()
                    return web.Response(text='YOn')
                if self.request.rel_url.query[cmd_key] == "YOff":
                    await self._send_ws_command(
                                command="YOff",
                                target=f"CKT{i+1}",
                            )
                    #         cur_cooler.YOff()
                    return web.Response(text='YOff')
            if val_key in self.request.rel_url.query.keys():
                # cur_cooler.SetSP(self.request.rel_url.query['val'+ str(i)])
                # await self._send_ws_command(
                #         command="set_sp",
                #         value=cur_cooler.sp,
                #         target=cur_cooler.name,
                #     )
                return web.Response(text='val')


    async def _send_ws_command(self, **data):
        # if not self._opc_clients:
        #     return
        # data["type"] = "command"
        # print(data)
        # coros = [ws.send_json(data) for ws in self._opc_clients]
        # await asyncio.gather(*coros, return_exceptions=True)
        ws = self.request.app["ws_opc_client"]
        if ws:
            ws.send_json(data)

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
