from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ChatHistory(BaseModel):
    id: Optional[str]
    student_id: str
    messages: List[dict] = Field(default_factory=list)  # {role, text, timestamp}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
