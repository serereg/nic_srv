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

logging.basicConfig(level=logging.DEBUG)
logging.debug("Informational message")
#regexp = re.compile(r'\.js|\.png|\.jpg|index\.html')

class Server:

    def __init__(self, app):
        self._opc_clients = set()
        self.list_cooler = []
        self.num_ckt = 12
        for i in range(0, self.num_ckt + 1 + 1):
            self.list_cooler.append(Cooler(i))
        # app.add_routes([web.get('/', self.handle),
        #                 web.get('/{name}', self.handle)])
        # app.router.add_get("/ws/opc", self.ws_opc_handler)  # for client opc exchange
        # app.router.add_static("/static", "static")

        # self.plc_link_wdt = 0
   

def db_connect(dsn, db):
    client = DBClient(dsn=dsn, db=db)
    client.connect()
    client.add_fixtures(FIXTURES)
    return client


async def redis_connect(host, port):
    client = RedisClient(host=host, port=port)
    await client.connect()
    return client


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    app = web.Application()

    loop = asyncio.get_event_loop()
    # db_client = loop.run_until_complete(db_connect("sqlite:///db.sqlite3", db))
    redis_client = loop.run_until_complete(redis_connect("localhost", 5679))
    db_client = db_connect("sqlite:///db.sqlite3", db)
    app["redis"] = redis_client
    app["database"] = db_client

    for path, method, view in ROUTES:
        app.router.add_route(method, path, view)
    app.router.add_static("/static", "static")

    web.run_app(app)
