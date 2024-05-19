import asyncio
import json
import websockets
from websockets import WebSocketClientProtocol
from textual import log

class WebSocketClient:
    def __init__(self, token, message_handler):
        self.token = token
        self.message_handler = message_handler
        self.ws_url = "wss://gateway.discord.gg/?v=9&encoding=json"
        self.heartbeat_interval = None

    async def connect(self):
        async with websockets.connect(self.ws_url) as websocket:
            await self.identify(websocket)
            await self.listen(websocket)

    async def identify(self, websocket: WebSocketClientProtocol):
        identify_payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "os": "windows",
                    "browser": "textual",
                    "device": "textual"
                }
            }
        }
        await websocket.send(json.dumps(identify_payload))

    async def listen(self, websocket: WebSocketClientProtocol):
        async for message in websocket:
            await self.handle_message(message, websocket)

    async def handle_message(self, message, websocket: WebSocketClientProtocol):
        data = json.loads(message)
        if data.get("op") == 10:  # Hello message with heartbeat interval
            self.heartbeat_interval = data["d"]["heartbeat_interval"] / 1000
            asyncio.create_task(self.heartbeat(websocket))

        log.info(f"Type: {data.get("t")}")
        if data.get("t") == "MESSAGE_CREATE" or data.get("t") == "MESSAGE_DELETE":
            log.info(f"Received message: {data}")
            await self.message_handler(data)

        

    async def heartbeat(self, websocket: WebSocketClientProtocol):
        while True:
            await asyncio.sleep(self.heartbeat_interval)
            await websocket.send(json.dumps({"op": 1, "d": None}))

    def run(self):
        asyncio.run(self.connect())
