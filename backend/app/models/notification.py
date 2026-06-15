from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Notification(BaseModel):
    id: Optional[str]
    student_id: Optional[str]
    type: str
    title: Optional[str]
    message: Optional[str]
    scheduled_at: Optional[datetime]
    delivered: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
