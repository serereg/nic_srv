import asyncio
import functools
import collections

#for import Cooler
import json

from aiohttp import ClientSession

# for working with telegram
# import traceback
import time
# import sys

# import requests


class WS:

    def timer(interval):
        def decorator(f):
            @functools.wraps(f)
            async def wrapper(*args, **kwargs):
                while True:
                    try:
                        await f(*args, **kwargs)
                    except asyncio.CancelledError:
                        raise
                    except Exception:
                        print("smolov")
                    await asyncio.sleep(interval)
            return wrapper
        return decorator

    def __init__(self, url):
        self.url = url
        self.ws = None
        self._ws_connected = asyncio.Event()
 

    @timer(10)
    async def _send_temperature_to_web_srv_task(self):
        for c_item in range(8):
            data = {
            "item": "CKT1",
            "temperature": c_item,
            "set_point": 16,
            "state": 11,
            "timestamp": 2020,
        }
        await self.ws.send_json(data)

    @timer(0)
    async def _ensure_web_socket(self):
        async with ClientSession() as session:
            async with session.ws_connect(self.url) as self.ws:
                self._ws_connected.set()
                # logger.info("web socket ready")
                while True:
                    await asyncio.sleep(0.1)
                    if self.ws.closed:
                        return

    async def run(self):
        self.tasks = [
            asyncio.create_task(self._ensure_web_socket()),
        ]
        await self._ws_connected.wait()
        self.tasks.extend([
            asyncio.create_task(self._send_temperature_to_web_srv_task()),
        ])

        await asyncio.wait(self.tasks)
        for t in self.tasks:
            t.cancel()
        await asyncio.wait(self.tasks)


async def main():
    ws = WS("http://localhost:8080/ws/opc")
    await ws.run()

if __name__ == "__main__":
    asyncio.run(main())
