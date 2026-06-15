from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Quiz(BaseModel):
    id: Optional[str]
    student_id: Optional[str]
    subject_id: Optional[str]
    title: Optional[str]
    questions: List[dict] = Field(default_factory=list)  # question blocks with type, choices, answer
    duration_minutes: Optional[int]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
