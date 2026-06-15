from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime

class Progress(BaseModel):
    id: Optional[str]
    student_id: str
    subject_progress: Dict[str, dict] = Field(default_factory=dict)  # subject -> {mastery_score, completed_chapters}
    overall_mastery: Optional[float] = 0.0
    quiz_history: List[dict] = Field(default_factory=list)
    time_spent_minutes: int = 0
    last_updated: datetime = Field(default_factory=datetime.utcnow)
