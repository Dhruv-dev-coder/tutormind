from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Syllabus(BaseModel):
    id: Optional[str]
    student_id: Optional[str]
    subject_id: Optional[str]
    title: Optional[str]
    chapters: List[dict] = Field(default_factory=list)  # list of {title, topics, estimated_hours}
    source_document_id: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
