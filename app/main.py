# import asyncio
import random
from typing import List, Optional

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://github.com/tiangolo/fastapi/issues/258
class Notifier:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            await self._notify(message)

    async def push(self, msg: str):
        await self.generator.asend(msg)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def _notify(self, message: str):
        living_connections = []
        while len(self.connections) > 0:
            # Looping like this is necessary in case a disconnection is handled
            # during await websocket.send_text(message)
            websocket = self.connections.pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections = living_connections


notifier = Notifier()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        notifier.remove(websocket)


@app.get("/push/{message}")
async def push_to_connected_websockets(message: str):
    await notifier.push(f"! Push notification: {message} !")


@app.on_event("startup")
async def startup():
    # Prime the push notification generator
    await notifier.generator.asend(None)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     print("Accepting client connection...")
#     await websocket.accept()
#     while True:
#         try:
#             # Wait for any message from the client
#             ws_text = await websocket.receive_text()
#             if ws_text == "ping":
#                 await websocket.send_json({"ping": "pong"})
#             else:
#                 # Send message to the client
#                 resp = {"value": random.uniform(0, 1)}
#                 # await asyncio.sleep(0.1)
#                 await websocket.send_json(resp)
#         except Exception as e:
#             print("error:", e)
#             break
#     print("Bye..")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


# if __name__ == "__main__":
# if settings.ENV != "production":
# uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True, debug=True)
# else:
#     uvicorn.run("main:app")
