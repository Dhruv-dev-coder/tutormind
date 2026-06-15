from pydantic import BaseModel
from typing import Optional


class TokenVerifyRequest(BaseModel):
    id_token: str


class TokenVerifyResponse(BaseModel):
    uid: str
    email: Optional[str]
    name: Optional[str]
    firebase_claims: Optional[dict]
