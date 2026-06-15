from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AIMemory(BaseModel):
    id: Optional[str]
    student_id: str
    completed_chapters: List[dict] = Field(default_factory=list)
    current_topic: Optional[dict] = None
    weak_topics: List[str] = Field(default_factory=list)
    strong_topics: List[str] = Field(default_factory=list)
    quiz_history: List[dict] = Field(default_factory=list)
    assignment_history: List[dict] = Field(default_factory=list)
    revision_history: List[dict] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
