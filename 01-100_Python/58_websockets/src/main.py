#!/usr/bin/env python3
"""
Program 58: WebSockets
Demonstrates WebSocket connections and real-time communication.

Topics covered:
- WebSocket basics
- WebSocket with FastAPI
- Broadcasting messages
- Room/channel management
- Connection management
- Error handling
- Real-time applications
"""

from typing import Dict, Any, List, Optional, Set
from datetime import datetime


class WebSocketsDemo:
    """Demonstration of WebSocket patterns."""

    def demonstrate_websocket_basics(self) -> None:
        """Demonstrate WebSocket basics."""
        print("WEBSOCKET BASICS")
        print("=" * 60)

        explanation = """
WebSocket vs HTTP:
------------------
HTTP (Request-Response):
- Client sends request
- Server sends response
- Connection closes
- Overhead for each request
- Half-duplex (one direction at a time)

WebSocket (Full-Duplex):
- Client initiates handshake (HTTP Upgrade)
- Connection stays open
- Bidirectional communication
- Low latency
- Full-duplex (both directions simultaneously)

WebSocket Flow:
1. Client sends HTTP Upgrade request
2. Server responds with 101 Switching Protocols
3. Connection upgraded to WebSocket
4. Messages flow bidirectionally
5. Either party can close connection

Use Cases:
- Chat applications
- Live updates (stock prices, sports scores)
- Collaborative editing
- Gaming
- Notifications
- Real-time dashboards
- Live streaming data
"""
        print(explanation)

    def demonstrate_fastapi_websocket(self) -> None:
        """Demonstrate WebSocket with FastAPI."""
        print("\nWEBSOCKET WITH FASTAPI")
        print("=" * 60)

        code = """
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import json

app = FastAPI()

# 1. Simple WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    '''Simple echo WebSocket.'''
    await websocket.accept()

    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            print(f"Received: {data}")

            # Send response to client
            await websocket.send_text(f"Echo: {data}")

    except WebSocketDisconnect:
        print("Client disconnected")

# 2. JSON messages
@app.websocket("/ws/json")
async def websocket_json(websocket: WebSocket):
    '''WebSocket with JSON messages.'''
    await websocket.accept()

    try:
        while True:
            # Receive JSON
            data = await websocket.receive_json()
            message_type = data.get("type")
            payload = data.get("payload")

            # Process message
            response = {
                "type": "response",
                "payload": f"Received {message_type}",
                "timestamp": datetime.now().isoformat()
            }

            # Send JSON
            await websocket.send_json(response)

    except WebSocketDisconnect:
        print("Disconnected")

# 3. Binary messages
@app.websocket("/ws/binary")
async def websocket_binary(websocket: WebSocket):
    '''WebSocket with binary data.'''
    await websocket.accept()

    try:
        while True:
            # Receive binary data
            data = await websocket.receive_bytes()

            # Process binary data
            # ...

            # Send binary data
            await websocket.send_bytes(data)

    except WebSocketDisconnect:
        print("Disconnected")

# Client-side JavaScript:
'''
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8000/ws');

// Connection opened
ws.onopen = () => {
    console.log('Connected');
    ws.send('Hello Server!');
};

// Receive message
ws.onmessage = (event) => {
    console.log('Received:', event.data);
};

// Connection closed
ws.onclose = () => {
    console.log('Disconnected');
};

// Error occurred
ws.onerror = (error) => {
    console.error('Error:', error);
};

// Send message
ws.send('Hello!');

// Send JSON
ws.send(JSON.stringify({
    type: 'message',
    payload: 'Hello'
}));

// Close connection
ws.close();
'''
"""
        print(code)

    def demonstrate_connection_manager(self) -> None:
        """Demonstrate WebSocket connection management."""
        print("\nCONNECTION MANAGEMENT")
        print("=" * 60)

        code = """
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict, Set
import json

class ConnectionManager:
    '''Manage WebSocket connections.'''

    def __init__(self):
        # Active connections
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        '''Accept and store connection.'''
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        '''Remove connection.'''
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        '''Send message to specific client.'''
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        '''Send message to all connected clients.'''
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_json(self, data: dict):
        '''Broadcast JSON to all clients.'''
        for connection in self.active_connections:
            await connection.send_json(data)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    '''WebSocket with connection management.'''
    await manager.connect(websocket)

    try:
        # Send connection confirmation
        await manager.send_personal_message(
            f"Welcome {client_id}!",
            websocket
        )

        # Notify others
        await manager.broadcast(f"{client_id} joined the chat")

        while True:
            # Receive message
            data = await websocket.receive_text()

            # Broadcast to all
            await manager.broadcast(f"{client_id}: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{client_id} left the chat")

# Advanced: Connection manager with user tracking
class AdvancedConnectionManager:
    def __init__(self):
        # Map user_id to websocket
        self.connections: Dict[str, WebSocket] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[user_id] = websocket

    def disconnect(self, user_id: str):
        if user_id in self.connections:
            del self.connections[user_id]

    async def send_to_user(self, user_id: str, message: str):
        '''Send message to specific user.'''
        if user_id in self.connections:
            await self.connections[user_id].send_text(message)

    async def send_to_users(self, user_ids: List[str], message: str):
        '''Send message to specific users.'''
        for user_id in user_ids:
            await self.send_to_user(user_id, message)

    async def broadcast(self, message: str, exclude: List[str] = None):
        '''Broadcast to all except excluded users.'''
        exclude = exclude or []
        for user_id, websocket in self.connections.items():
            if user_id not in exclude:
                await websocket.send_text(message)

    def get_connected_users(self) -> List[str]:
        '''Get list of connected user IDs.'''
        return list(self.connections.keys())
"""
        print(code)

    def demonstrate_chat_application(self) -> None:
        """Demonstrate a chat application with rooms."""
        print("\nCHAT APPLICATION WITH ROOMS")
        print("=" * 60)

        code = """
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Set
from datetime import datetime
import json

app = FastAPI()

class ChatRoom:
    '''Represents a chat room.'''

    def __init__(self, room_id: str):
        self.room_id = room_id
        self.connections: Dict[str, WebSocket] = {}

    async def add_user(self, user_id: str, websocket: WebSocket):
        '''Add user to room.'''
        await websocket.accept()
        self.connections[user_id] = websocket

        # Notify room
        await self.broadcast({
            "type": "user_joined",
            "user_id": user_id,
            "room_id": self.room_id,
            "timestamp": datetime.now().isoformat()
        }, exclude=[user_id])

    async def remove_user(self, user_id: str):
        '''Remove user from room.'''
        if user_id in self.connections:
            del self.connections[user_id]

            # Notify room
            await self.broadcast({
                "type": "user_left",
                "user_id": user_id,
                "room_id": self.room_id,
                "timestamp": datetime.now().isoformat()
            })

    async def send_message(self, user_id: str, message: str):
        '''Send message to room.'''
        await self.broadcast({
            "type": "message",
            "user_id": user_id,
            "room_id": self.room_id,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

    async def broadcast(self, data: dict, exclude: List[str] = None):
        '''Broadcast to all users in room.'''
        exclude = exclude or []
        for user_id, websocket in self.connections.items():
            if user_id not in exclude:
                try:
                    await websocket.send_json(data)
                except:
                    # Connection failed, remove user
                    await self.remove_user(user_id)

    def get_users(self) -> List[str]:
        '''Get list of users in room.'''
        return list(self.connections.keys())

class ChatManager:
    '''Manage multiple chat rooms.'''

    def __init__(self):
        self.rooms: Dict[str, ChatRoom] = {}

    def get_or_create_room(self, room_id: str) -> ChatRoom:
        '''Get existing room or create new one.'''
        if room_id not in self.rooms:
            self.rooms[room_id] = ChatRoom(room_id)
        return self.rooms[room_id]

    def get_room(self, room_id: str) -> ChatRoom:
        '''Get room by ID.'''
        return self.rooms.get(room_id)

    def delete_room(self, room_id: str):
        '''Delete room if empty.'''
        room = self.rooms.get(room_id)
        if room and len(room.connections) == 0:
            del self.rooms[room_id]

    def get_all_rooms(self) -> List[str]:
        '''Get list of all room IDs.'''
        return list(self.rooms.keys())

chat_manager = ChatManager()

@app.websocket("/ws/chat/{room_id}/{user_id}")
async def chat_websocket(
    websocket: WebSocket,
    room_id: str,
    user_id: str
):
    '''WebSocket endpoint for chat.'''
    room = chat_manager.get_or_create_room(room_id)
    await room.add_user(user_id, websocket)

    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            message_type = data.get("type")

            if message_type == "message":
                # Send message to room
                message = data.get("message")
                await room.send_message(user_id, message)

            elif message_type == "typing":
                # Broadcast typing indicator
                await room.broadcast({
                    "type": "typing",
                    "user_id": user_id,
                    "room_id": room_id
                }, exclude=[user_id])

            elif message_type == "get_users":
                # Send list of users
                users = room.get_users()
                await websocket.send_json({
                    "type": "users_list",
                    "users": users
                })

    except WebSocketDisconnect:
        await room.remove_user(user_id)
        chat_manager.delete_room(room_id)

# REST endpoints for chat
@app.get("/chat/rooms")
def get_rooms():
    '''Get list of all chat rooms.'''
    return {"rooms": chat_manager.get_all_rooms()}

@app.get("/chat/rooms/{room_id}/users")
def get_room_users(room_id: str):
    '''Get users in a room.'''
    room = chat_manager.get_room(room_id)
    if not room:
        return {"users": []}
    return {"users": room.get_users()}

# Client-side usage:
'''
const ws = new WebSocket('ws://localhost:8000/ws/chat/room1/user123');

ws.onopen = () => {
    // Send message
    ws.send(JSON.stringify({
        type: 'message',
        message: 'Hello everyone!'
    }));

    // Send typing indicator
    ws.send(JSON.stringify({
        type: 'typing'
    }));

    // Get users list
    ws.send(JSON.stringify({
        type: 'get_users'
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    switch(data.type) {
        case 'message':
            console.log(`${data.user_id}: ${data.message}`);
            break;
        case 'user_joined':
            console.log(`${data.user_id} joined`);
            break;
        case 'user_left':
            console.log(`${data.user_id} left`);
            break;
        case 'typing':
            console.log(`${data.user_id} is typing...`);
            break;
        case 'users_list':
            console.log('Users:', data.users);
            break;
    }
};
'''
"""
        print(code)

    def demonstrate_error_handling(self) -> None:
        """Demonstrate WebSocket error handling."""
        print("\nWEBSOCKET ERROR HANDLING")
        print("=" * 60)

        code = """
from fastapi import WebSocket, WebSocketDisconnect, status
import asyncio
import logging

logger = logging.getLogger(__name__)

@app.websocket("/ws/secure")
async def secure_websocket(websocket: WebSocket):
    '''WebSocket with error handling and timeouts.'''

    try:
        # Accept with timeout
        await asyncio.wait_for(websocket.accept(), timeout=5.0)

    except asyncio.TimeoutError:
        logger.error("Connection timeout")
        return

    try:
        while True:
            # Receive with timeout
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=60.0  # 60 second timeout
                )

            except asyncio.TimeoutError:
                # Send ping to check if connection alive
                try:
                    await websocket.send_json({
                        "type": "ping",
                        "timestamp": datetime.now().isoformat()
                    })
                except:
                    # Connection dead, exit
                    break

            # Validate message
            try:
                message = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON"
                })
                continue

            # Process message with error handling
            try:
                # Your message processing logic
                result = await process_message(message)
                await websocket.send_json({
                    "type": "success",
                    "data": result
                })

            except ValueError as e:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })

            except Exception as e:
                logger.exception("Error processing message")
                await websocket.send_json({
                    "type": "error",
                    "message": "Internal server error"
                })

    except WebSocketDisconnect as e:
        logger.info(f"Client disconnected: {e.code}")

    except Exception as e:
        logger.exception("WebSocket error")

    finally:
        # Cleanup
        try:
            await websocket.close()
        except:
            pass

# Rate limiting for WebSocket
from collections import defaultdict
from time import time

message_counts = defaultdict(list)

async def rate_limit_check(user_id: str, max_messages: int = 10, window: int = 60):
    '''Check if user exceeded rate limit.'''
    now = time()
    # Remove old timestamps
    message_counts[user_id] = [
        t for t in message_counts[user_id]
        if now - t < window
    ]

    # Check limit
    if len(message_counts[user_id]) >= max_messages:
        return False

    # Add current timestamp
    message_counts[user_id].append(now)
    return True

@app.websocket("/ws/ratelimited/{user_id}")
async def ratelimited_websocket(websocket: WebSocket, user_id: str):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()

            # Check rate limit
            if not await rate_limit_check(user_id):
                await websocket.send_json({
                    "type": "error",
                    "message": "Rate limit exceeded"
                })
                continue

            # Process message
            # ...

    except WebSocketDisconnect:
        pass
"""
        print(code)


def main() -> None:
    """Main entry point demonstrating WebSockets."""
    print("\n" + "=" * 60)
    print("PROGRAM 58: WEBSOCKETS")
    print("=" * 60 + "\n")

    demo = WebSocketsDemo()

    demo.demonstrate_websocket_basics()
    demo.demonstrate_fastapi_websocket()
    demo.demonstrate_connection_manager()
    demo.demonstrate_chat_application()
    demo.demonstrate_error_handling()

    print("\n" + "=" * 60)
    print("WEBSOCKET BEST PRACTICES")
    print("=" * 60)
    print("1. Implement proper connection management")
    print("2. Handle disconnections gracefully")
    print("3. Use heartbeat/ping-pong for connection health")
    print("4. Implement rate limiting")
    print("5. Validate all incoming messages")
    print("6. Use timeouts for operations")
    print("7. Clean up resources on disconnect")
    print("8. Consider using Redis for scaling")
    print("9. Implement authentication/authorization")
    print("10. Log errors and monitor connections")
    print("=" * 60)


if __name__ == "__main__":
    main()
