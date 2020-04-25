import asyncio
import logging

from aiohttp import web

from .utils import HTTPView, JSONRPCView, WSView, is_set


NUMBER_OF_COOLERS = 12
STATE_IS_ON = 0
STATE_IS_FAULT = 1
STATE_IS_ALARM = 2


class WSOPCView(JSONRPCView, WSView):
    async def state(self, item, temperature, set_point, state, wdt):
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
        self.request.app["watchdog_timer"] = wdt
        return "ok", None


class WSClientView(JSONRPCView, WSView):
    @JSONRPCView.login_required
    async def state(self):
        db_client = self.request.app["database"]
        redis_client = self.request.app["redis"]
        result = {"CKT":[], "plc_client_wdt": self.request.app["watchdog_timer"]}
        # result = []
        for cooler in db_client.get_coolers():
            pack = {
                "id": cooler.id,
                "description": cooler.description,
                "pv": -123, 
                "sp": -123, 
                "is_reg_on": 0, 
                "is_pv_fault": 0,
                "is_reg_alarm": 0,
            }
            data = await redis_client.get_cooler_state(cooler_id=cooler.id)
            if data:
                pack["pv"] = data["temperature"]
                pack["sp"] = data["set_point"]
                pack["is_reg_on"] = is_set(data["state"], STATE_IS_ON),
                pack["is_pv_fault"] = is_set(data["state"], STATE_IS_FAULT)
                pack["is_reg_alarm"] = is_set(data["state"], STATE_IS_ALARM)

            result["CKT"].append(pack)
        return result, None

    @JSONRPCView.login_required
    async def command(self, id, switch):
        print("command")
        ws = self.request.app["ws_opc_client"]
        pack = {"jsonrpc": "2.0", "method": "command", 
                "params": {
                    "id" : id, 
                    "switch" : switch}, 
                "id": 1}
        await ws.send_json(pack)
        
        return "ok", None

    @JSONRPCView.login_required
    async def set_point(self, id, set_point):
        print("set_point")
        ws = self.request.app["ws_opc_client"]
        pack = {"jsonrpc": "2.0", "method": "set_point", 
                "params": {
                    "id" : id, 
                    "set_point" : set_point}, 
                "id": 1}
        await ws.send_json(pack)
        
        return "ok", None

    @JSONRPCView.login_required
    async def set_description(self, id, description):
        db_client = self.request.app["database"]
        
        cooler = db_client.get_cooler(id=id)
        if cooler is None:
            return None, f"No cooler with id '{id}' in database"
        cooler.description = description
        db_client.session.commit()

        return "ok", None


class APIClientView(JSONRPCView, HTTPView):
    async def login(self, username, password):
        db_client = self.request.app["database"]
        user = db_client.get_user(username=username, password=password)
        if user is None:
            return None, "Incorrect username or password"

        session = db_client.create_session(user)

        return {"token": session.token}, None

    @JSONRPCView.login_required
    async def logout(self):
        self.session.delete()
        self.request.app["database"].commit()


class IndexView(web.View):
    async def get(self):
        return web.FileResponse("static/index.html")

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

