import hashlib
import uuid
from datetime import timezone, datetime
from app.models.voter_model import Voter, AuthResponse
from app.state import voters_db, token_store

def hash_fingerprint(fingerprint: str) -> str:
    return hashlib.sha256(fingerprint.encode()).hexdigest()


def generate_token() -> str:
    return str(uuid.uuid4())


def verify_voter(voter_id: str, fingerprint: str) -> AuthResponse:
    hashed_input = hash_fingerprint(fingerprint)

    # 🔍 Find voter
    voter = next((v for v in voters_db if v.voter_id == voter_id), None)

    if not voter:
        return AuthResponse(
            status="rejected",
            reason="Voter not found",
            token=None
        )

    # 🔐 Check fingerprint
    if voter.fingerprint_hash != hashed_input:
        return AuthResponse(
            status="rejected",
            reason="Fingerprint mismatch",
            token=None
        )

    # 🚫 Check if already voted
    if voter.has_voted:
        return AuthResponse(
            status="rejected",
            reason="Voter has already voted",
            token=None
        )

    # ✅ Generate token
    token = generate_token()
    token_store[token] = {
        "voter_id": voter.voter_id,
        "issued_at": datetime.now(timezone.utc)
    }

    return AuthResponse(
        status="verified",
        reason="Voter verified successfully",
        token=token
    )