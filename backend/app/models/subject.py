from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Subject(BaseModel):
    id: Optional[str]
    name: str
    syllabus_id: Optional[str]
    teacher_notes: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
