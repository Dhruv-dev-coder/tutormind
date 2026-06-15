from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Assignment(BaseModel):
    id: Optional[str]
    student_id: Optional[str]
    subject_id: Optional[str]
    title: Optional[str]
    instructions: Optional[str]
    due_date: Optional[datetime]
    max_score: Optional[float]
    submissions: List[dict] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
