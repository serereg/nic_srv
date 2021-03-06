import asyncio_redis
import logging
import datetime

STATE_IS_ON = 0
STATE_IS_FAULT = 1
STATE_IS_ALARM = 2


class RedisClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None

    async def connect(self, poolsize=10): # poolsize ?
        self.connection = await asyncio_redis.Pool.create(
            host=self.host,
            port=self.port,
            poolsize=poolsize,
        )

    async def close(self):
        await self.connection.close()

    async def set_cooler_state(self, cooler_id, temperature, set_point, state):
        timestamp = datetime.datetime.now().timestamp()

        transaction = await self.connection.multi()

        await transaction.rpush(f"cooler:{cooler_id}:temperature", [str(temperature)])
        await transaction.rpush(f"cooler:{cooler_id}:set_point", [str(set_point)])
        await transaction.rpush(f"cooler:{cooler_id}:state", [str(state)])
        await transaction.rpush(f"cooler:{cooler_id}:timestamp", [str(timestamp)])

        await transaction.set(f"cooler:{cooler_id}:last:temperature", str(temperature))
        await transaction.set(f"cooler:{cooler_id}:last:set_point", str(set_point))
        await transaction.set(f"cooler:{cooler_id}:last:state", str(state))

        await transaction.exec()

    async def get_cooler_state(self, cooler_id):
        data = {}
        try:
            temperature = await self.connection.get(f"cooler:{cooler_id}:last:temperature")
            if temperature:
                data["temperature"] = float(temperature)
            set_point = await self.connection.get(f"cooler:{cooler_id}:last:set_point")
            if set_point:
                data["set_point"] = float(set_point)
            state = await self.connection.get(f"cooler:{cooler_id}:last:state")
            if state:
                data["state"] = int(state)
        except Exception as e:
            print(e)
            data["temperature"] = -121.1
            data["set_point"] = -131.1
            data["state"] = STATE_IS_FAULT

        return data
