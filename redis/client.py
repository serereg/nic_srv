import asyncio_redis
import logging
import datetime


class RedisClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None

    async def connect(self, poolsize=1):
        self.data = {}
        # self.connection = await asyncio_redis.Pool.create(
        #     host=self.host,
        #     port=self.port,
        #     poolsize=poolsize,
        # )

    async def close(self):
        pass
        # await self.connection.close()

    async def set_cooler_state(self, cooler_id, temperature, set_point, state):
        timestamp = datetime.datetime.now().timestamp        
        
        # transaction = await self.connection.multi()

        # await transaction.set(f"cooler:{cooler_id}:{timestamp}:temperature", temperature)
        # await transaction.set(f"cooler:{cooler_id}:{timestamp}:set_point", set_point)
        # await transaction.set(f"cooler:{cooler_id}:{timestamp}:state", state)

        # await transaction.exec()

        data = {
            "data": {
                "temperature": temperature,
                "set_point": set_point,
                "state": state,
            },
            "timestamp": timestamp,
        }
        if cooler_id in self.data:
            self.data[cooler_id].append(data)
        else:
            self.data[cooler_id] = [data] 
        logging.info(self.data[cooler_id][-1]["data"])

    async def get_cooler_state(self, cooler_id):
        if cooler_id in self.data:
            pass
        else:
            self.set_cooler_state(cooler_id, 0.0, 0.0, 0)
        return self.data[cooler_id][-1]["data"]
