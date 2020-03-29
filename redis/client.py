import asyncio_redis
import logging
import datetime


class RedisClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None

    async def connect(self, poolsize=1):
        # self.data = {}
        self.connection = await asyncio_redis.Pool.create(
            host=self.host,
            port=self.port,
            poolsize=poolsize,
        )

    async def close(self):
        # pass
        await self.connection.close()

    async def set_cooler_state(self, cooler_id, temperature, set_point, state):
        timestamp = datetime.datetime.now().timestamp()      
        print("TSS:", timestamp)

        transaction = await self.connection.multi()

        await transaction.set(f"cooler:{cooler_id}:{timestamp}:temperature", str(temperature))
        await transaction.set(f"cooler:{cooler_id}:{timestamp}:set_point", str(set_point))
        await transaction.set(f"cooler:{cooler_id}:{timestamp}:state", str(state))

        await transaction.exec()

        # data = {
        #     "data": {
        #         "temperature": temperature,
        #         "set_point": set_point,
        #         "state": state,
        #     },
        #     "timestamp": timestamp,
        # }
        # if cooler_id in self.data:
        #     self.data[cooler_id].append(data)
        # else:
        #     self.data[cooler_id] = [data] 
        # logging.info(self.data[cooler_id][-1]["data"])

    async def get_cooler_state(self, cooler_id):
        cursor = await self.connection.scan(match=f"cooler:{cooler_id}:*")
        cooler_data = await cursor.fetchall()
        cooler_data.sort()
        data = {}
        for key in cooler_data[-3:]:
            _, __, timestamp, k = key.split(":")
            data[k] = float(await self.connection.get(key))
        
        return data

        # if cooler_id in self.data:
        #     pass
        # else:
        #     await self.set_cooler_state(cooler_id, 0.0, 0.0, 0)
        # return self.data[cooler_id][-1]["data"]
