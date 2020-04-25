from aiohttp import web
import asyncio
import json
import logging
import os
import re

from database.client import DBClient
from database.fixtures import FIXTURES
from database.models import Base
from redis.client import RedisClient
from web.routes import ROUTES
   

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
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = int(os.environ["DB_PORT"])
    DB_NAME = os.environ["DB_NAME"]
    DB_USER = os.environ["DB_USER"]
    DB_PASSWORD = os.environ["DB_PASSWORD"]

    REDIS_HOST = os.environ["REDIS_HOST"]
    REDIS_PORT = int(os.environ["REDIS_PORT"])

    logger = logging.getLogger(__name__)
    app = web.Application()

    loop = asyncio.get_event_loop()
    redis_client = loop.run_until_complete(redis_connect(REDIS_HOST, REDIS_PORT))
    db_client = db_connect(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        Base,
    )
    app["redis"] = redis_client
    app["database"] = db_client

    for path, method, view in ROUTES:
        app.router.add_route(method, path, view)
    app.router.add_static("/static", "static")

    web.run_app(app, port=80)
