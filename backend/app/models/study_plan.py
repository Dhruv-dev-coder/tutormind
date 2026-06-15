from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class StudyPlan(BaseModel):
    id: Optional[str]
    student_id: str
    plan_type: str  # semester/monthly/weekly/daily
    title: Optional[str]
    tasks: List[dict] = Field(default_factory=list)  # tasks with status, due date, topic refs
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
