from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websockets.connection_manager import manager
import json

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            if message_data.get("type") == "new_message":
                await manager.send_to_conversation(
                    message_data,
                    user_id,
                    message_data.get("receiver_id")
                )

    except WebSocketDisconnect:
        manager.disconnect(user_id)