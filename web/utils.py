import json

from aiohttp import web
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import jwt


class HTTPView(web.View):
    async def get(self):
        pass

    async def post(self):
        status_code, headers, body = await self.handler(request.body, request.headers)

        return web.Response(body)


class WSView(web.View):
    async def get(self):
        self.ws = web.WebSocketResponse()
        await self.ws.prepare(self.request)

        async for message in self.ws:
            await self.ws.send_json(await self.handle(message.data, message.headers))

    async def handle(self, data, headers):
        raise NotImplementedError


class JSONRPCView(web.View):
    SCHEMA = {
        "additionalProperties": False,
        "properties": {
            "jsonrpc": {
                "enum": ["2.0"],
            },
            "id": {
                "type": "integer",
                "minimum": 1,
            },
            "method": {
                "type": "string",
            },
            "params": {
                "type": "object",
            },
        },
        "required": ["jsonrpc", "id", "method"],
    }

    def auth(coroutine):
        async def wrapper(self, **params):
            pass

        return wrapper

    # jsonschema validator for json-rpc 2.0
    async def handle(self, data, headers):
        response = {"jsonrpc": "2.0", "error": None, "result": None, "id": None}
        try:
            data = json.loads(message.data)
            validate(data, schema=self.SCHEMA)
            if hasattr(self, data["method"]):
                method = getattr(self, data["method"])
                response["result"], response["error"] = method(**data.get("params", {}))
            else:
                response["error"] = f"Have no method '{data['method']}'"
            response["id"] = data["id"]
        except json.decoder.JSONDecodeError:
            response["error"] = "Incorrect format"
        except ValidationError as e:
            response["error"] = e.args[0]
            response["id"] = data.get("id")
        except:
            response["error"] = "Server error"
        finally:
            return response
