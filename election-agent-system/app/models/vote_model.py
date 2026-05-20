from pydantic import BaseModel

class VoteRequest(BaseModel):
    token: str
    candidate: str

    class Config:
        extra = "forbid"

class VoteResponse(BaseModel):
    status: str
    reason: str