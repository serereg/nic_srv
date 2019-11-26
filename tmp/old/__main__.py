# import asyncio

from aiohttp import web
from loguru import logger


routes = web.RouteTableDef()


class Server:

    def __init__(self, app):
        self._opc_clients = set()
        self._browser_clients = set()
        app.router.add_get("/", self.root_handler)
        app.router.add_get("/ws/opc", self.ws_opc_handler)

    # async def _simulate_commands(self):
    #     import random
    #     while True:
    #         await asyncio.sleep(5)
    #         if not self._opc_clients:
    #             continue
    #         cmd = dict(type="command", action=random.choice(["on", "off", "set"]),
    #                    item="node1", value=random.randint(-20, 20))
    #         logger.info("sending command {} to {} clients", cmd, len(self._opc_clients))
    #         await asyncio.gather(*[ws.send_json(cmd) for ws in self._opc_clients])

    async def ws_browser_handler(self, request):
        pass

    async def ws_opc_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self._opc_clients.add(ws)
        async for msg in ws:
            logger.info("opc msg {}", msg.data)
        self._opc_clients.discard(ws)

    async def root_handler(self, request):
        return web.FileResponse("static/index.html")


def main():
    app = web.Application()
    Server(app)
    app.add_routes(routes)
    web.run_app(app)


if __name__ == "__main__":
    main()
