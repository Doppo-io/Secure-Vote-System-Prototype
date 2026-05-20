from datetime import datetime, timezone
from fastapi import WebSocket, WebSocketDisconnect
from app.agents.voting_agent import votes_ledger

# Connected dashboard clients
active_connections: list[WebSocket] = []


async def connect_client(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)


def disconnect_client(websocket: WebSocket):
    active_connections.remove(websocket)


async def broadcast(message: dict):
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception:
            pass


async def get_tally() -> dict:
    tally = {}
    for vote in votes_ledger:
        candidate = vote["candidate"]
        tally[candidate] = tally.get(candidate, 0) + 1
    return {
        "total_votes": len(votes_ledger),
        "tally": tally,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }