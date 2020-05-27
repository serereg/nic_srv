import asyncio_redis
import logging
import datetime

STATE_IS_ON = 0
STATE_IS_FAULT = 1
STATE_IS_ALARM = 2


class RedisClient:
    def __init__(self, host, port, simulate):
        self.host = host
        self.port = port
        self.connection = None
        self.simulate = simulate
        self.coolers_data = dict()

    async def connect(self, poolsize=10): # poolsize ?
        if self.simulate:
            return
        self.connection = await asyncio_redis.Pool.create(
            host=self.host,
            port=self.port,
            poolsize=poolsize,
        )

    async def close(self):
        if self.simulate:
            return
        await self.connection.close()

    async def set_cooler_state(self, cooler_id, temperature, set_point, state):
        if self.simulate:
            self.coolers_data["cooler_id"] = {"temperature":temperature,
                "set_point":set_point,
                "state":state}
            return

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
            if self.simulate:
                data["temperature"] = float(self.coolers_data[cooler_id]["temperature"])
                data["set_point"] = float(self.coolers_data[cooler_id]["set_point"])
                data["state"] = int(self.coolers_data[cooler_id]["state"])
            else:
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
