import hashlib
from datetime import datetime, timezone
from app.models.vote_model import VoteResponse
from app.state import voters_db, token_store, votes_ledger

def encrypt_vote(candidate: str, voter_id: str) -> str:
    payload = f"{voter_id}:{candidate}:{datetime.now(timezone.utc).isoformat()}"
    return hashlib.sha256(payload.encode()).hexdigest()

def cast_vote(token: str, candidate: str) -> VoteResponse:

    # Validate token exists
    token_data = token_store.get(token)
    if not token_data:
        return VoteResponse(status="rejected", reason="Invalid or expired token")

    # Check session timeout (token older than 5 minutes is dead)
    elapsed = (datetime.now(timezone.utc) - token_data["issued_at"]).seconds
    if elapsed > 300:
        token_store.pop(token)
        return VoteResponse(status="rejected", reason="Session timed out")

    voter_id = token_data["voter_id"]

    # Find voter and guard against double voting
    voter = next((v for v in voters_db if v.voter_id == voter_id), None)
    if not voter:
        return VoteResponse(status="rejected", reason="Voter not found")

    if voter.has_voted:
        return VoteResponse(status="rejected", reason="Voter has already voted")

    # Encrypt and record vote
    encrypted = encrypt_vote(candidate, voter_id)
    vote_record = {
        "voter_id": voter_id,
        "candidate": candidate,
        "encrypted_vote": encrypted,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    votes_ledger.append(vote_record)


    # Mark voter and consume token
    voter.has_voted = True
    token_store.pop(token)

    return VoteResponse(status="accepted", reason="Vote cast successfully")