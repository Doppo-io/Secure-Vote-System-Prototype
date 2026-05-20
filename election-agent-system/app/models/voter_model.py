from pydantic import BaseModel

class Voter(BaseModel):
    voter_id: str
    fingerprint_hash: str
    has_voted: bool = False


class VoterRequest(BaseModel):
    voter_id: str
    fingerprint: str  # raw input (we will hash this)
    class Config:
        extra = "forbid"  # Forbid extra fields in the request

class AuthResponse(BaseModel):
    status: str
    reason: str
    token: str | None = None