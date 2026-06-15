from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class RevisionSchedule(BaseModel):
    id: Optional[str]
    student_id: str
    entries: List[dict] = Field(default_factory=list)  # {topic, scheduled_at, status}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
