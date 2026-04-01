from typing import Annotated
from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    Depends,
    Query,
    WebSocketException,
    status,
)
import json
app = FastAPI()


@app.get("/")
def hello():
    return {"message": "hello"}


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: int):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"Client {client_id} connected")
        print("Active users:", list(self.active_connections.keys()))

    def disconnect(self, client_id: int):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            print(f"Client {client_id} disconnected")

    async def send_personal_message(self, message: str, client_id: int):
        websocket = self.active_connections.get(client_id)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            try:
                await connection.send_text(message)
            except:
                pass


manager = ConnectionManager()


# 🔐 Dependency (auth simulation)
# async def get_token(
#     token: Annotated[str | None, Query()] = None,
# ):
#     if token is None:
#         raise WebSocketException(
#             code=status.WS_1008_POLICY_VIOLATION
#         )
#     return token


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: int,
    # token: Annotated[str, Depends(get_token)],
):
    print(f"New connection attempt from {client_id}")

    await manager.connect(websocket, client_id)

    try:
        while True:
            data = await websocket.receive_text()
            parsed = json.loads(data)

            to = parsed["to"]
            msg = parsed["message"]

            print(f"{client_id} → {to}: {msg}")

            # send to receiver
            await manager.send_personal_message(
                f"From {client_id}: {msg}", to
            )

            # optional: send back to sender
            await manager.send_personal_message(
                f"You → {to}: {msg}", client_id
            )
            print("Received:", data)

            # broadcast
            await manager.broadcast(
                f"Client #{client_id} says: {data}"
            )

    except WebSocketDisconnect:
        print("disconnecting")
        manager.disconnect(client_id)
        await manager.broadcast(f"Client #{client_id} left the chat")

    except Exception as e:
        print("Error:", e)