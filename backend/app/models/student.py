from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Student(BaseModel):
    id: Optional[str]
    name: str
    email: str
    class_name: Optional[str] = None
    board: Optional[str] = None
    subjects: List[str] = Field(default_factory=list)
    study_hours: Optional[int] = None
    learning_profile_id: Optional[str] = None
    last_activity: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
