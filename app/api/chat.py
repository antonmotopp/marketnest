from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websockets.connection_manager import manager
import json

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    print(f"WebSocket connection attempt for user {user_id}")

    try:
        await manager.connect(websocket, user_id)
        print(f"User {user_id} successfully connected to WebSocket")

        while True:
            data = await websocket.receive_text()
            print(f"Received data from user {user_id}: {data}")

            try:
                message_data = json.loads(data)

                if message_data.get("type") == "new_message":
                    print(f"Processing new_message from user {user_id}")
                    await manager.send_to_conversation(
                        message_data,
                        user_id,
                        message_data.get("receiver_id")
                    )
            except json.JSONDecodeError as e:
                print(f"Invalid JSON from user {user_id}: {e}")
            except Exception as e:
                print(f"Error processing message from user {user_id}: {e}")

    except WebSocketDisconnect:
        print(f"User {user_id} disconnected from WebSocket")
        manager.disconnect(user_id)
    except Exception as e:
        print(f"Unexpected error for user {user_id}: {e}")
        manager.disconnect(user_id)