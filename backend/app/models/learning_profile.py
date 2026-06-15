from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LearningProfile(BaseModel):
    id: Optional[str]
    student_id: str
    learning_level: Optional[str]
    mastery_scores: dict = Field(default_factory=dict)
    weak_topics: List[str] = Field(default_factory=list)
    strong_topics: List[str] = Field(default_factory=list)
    preferred_study_hours: Optional[int] = None
    study_pattern: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
