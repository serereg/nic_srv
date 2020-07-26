import aiohttp
from aiohttp import web
import asyncio
import json
import logging
import re

from database.client import DBClient
from database.fixtures import FIXTURES
from database.models import Base
from redis.client import RedisClient
from web.routes import ROUTES
   
from config import CONFIG

def db_connect(dsn, db):
    client = DBClient(dsn=dsn, db=db)
    client.connect()
    client.add_fixtures(FIXTURES)
    return client


async def redis_connect(host, port):
    client = None
    data = CONFIG["redis_connect"]
    client = RedisClient(host=host, port=port, simulate= not data["enable"])
    await client.connect()
    return client


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    app = web.Application()

    loop = asyncio.get_event_loop()
    redis_client = loop.run_until_complete(redis_connect("localhost", 6379))
    db_client = db_connect("sqlite:///db/db.sqlite3", Base)
    app["redis"] = redis_client
    app["database"] = db_client

    for path, method, view in ROUTES:
        app.router.add_route(method, path, view)
    app.router.add_static("/static", "static")

    web.run_app(app, port=80)
