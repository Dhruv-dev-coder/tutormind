from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class StudySession(BaseModel):
    id: Optional[str]
    student_id: str
    subject_id: Optional[str]
    topic: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    activity_log: List[dict] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
