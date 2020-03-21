from aiohttp import web


class OPCView(web.View):
    async def get(self):
        db_client = self.request.app["database"]
        redis_client = self.request.app["redis"]
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        async for message in ws:
            data = json.loads(message.data)
            cooler = db_client.get_cooler(name=data["item"])

            redis_client.set_cooler_state(
                cooler_id=cooler.id,
                temperature=data["temperature"],
                set_point=data["sp"],
                state=data["state"],
            )


class IndexView(web.View):
    async def get(self):
        return web.FileResponse("static/index.html")


class CoolerStateView(web.View):
    async def get(self):
        db_client = self.request.app["database"]
        redis_client = self.request.app["redis"]

        name = self.request.match_info["name"]
        
        cooler = await db_client.get_cooler(name=name)
        data = await redis_client.get_cooler(cooler_id=cooler.id)

        return web.json_response(data)
