from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MockTest(BaseModel):
    id: Optional[str]
    student_id: str
    subject_id: Optional[str]
    name: Optional[str]
    questions: List[dict] = Field(default_factory=list)
    scheduled_for: Optional[datetime]
    duration_minutes: Optional[int]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
