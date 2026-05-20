import socket
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.models.voter_model import VoterRequest
from app.agents.identity_agent import verify_voter
from app.agents.voting_agent import cast_vote
from app.models.vote_model import VoteRequest 
from fastapi import WebSocket, WebSocketDisconnect
from app.agents.ledger_agent import broadcast, connect_client, disconnect_client, get_tally 
from app.state import votes_ledger
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    ip = get_local_ip()
    print("\n" + "="*55)
    print("   ✅  SecureVote is running")
    print("="*55)
    print(f"   🗳️   Voting page  → http://{ip}:8000/static/index.html")
    print(f"   📊  Dashboard    → http://{ip}:8000/static/dashboard.html")
    print(f"   📡  API docs     → http://{ip}:8000/docs")
    print("="*55)
    print("   Share the voting link with voters on your network")
    print("="*55 + "\n")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home():
    return {"message": "Welcome to the Election Agent System!"}

@app.post("/verify")
def verify_voter_endpoint(voter_request: VoterRequest):
    print("Function entered")
    response = verify_voter(voter_request.voter_id, voter_request.fingerprint)
    return response

@app.post("/vote")
async def cast_vote_endpoint(vote_request: VoteRequest):
    response = cast_vote(vote_request.token, vote_request.candidate) 
    # Only broadcast if vote was accepted
    if response.status == "accepted":
        await broadcast({
            "event": "new_vote",
            "candidate": vote_request.candidate,
            "total_votes": len(votes_ledger)
        })

    return response

@app.websocket("/ws/dashboard")
async def dashboard_websocket(websocket: WebSocket):
    await connect_client(websocket)
    try:
        #Send current tally immediately on connection
        tally = await get_tally()
        await websocket.send_json(tally)
        #Keep connection alive to send future updates
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        disconnect_client(websocket)

@app.get("/results")
async def get_results():
    return await get_tally()


#run code - uvicorn app.main:app --reload --host 0.0.0.0 --port 8000