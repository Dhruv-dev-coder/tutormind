from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Achievement(BaseModel):
    id: Optional[str]
    student_id: str
    key: str
    title: Optional[str]
    description: Optional[str]
    awarded_at: datetime = Field(default_factory=datetime.utcnow)
