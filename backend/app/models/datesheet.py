from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Datesheet(BaseModel):
    id: Optional[str]
    student_id: Optional[str]
    exams: List[dict] = Field(default_factory=list)  # list of {subject, date, duration, weight}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
