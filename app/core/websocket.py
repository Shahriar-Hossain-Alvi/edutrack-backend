from fastapi import WebSocket
from typing import Dict


class ConnectionManager:
    def __init__(self):
        # use user_id as key to store websocket connection
        self.active_connections: Dict[int, WebSocket] = {}

    # connect user to websocket
    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    # disconnect user from websocket
    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    # send message to user
    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_json(message)


manager = ConnectionManager()
