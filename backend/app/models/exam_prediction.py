from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class ExamPrediction(BaseModel):
    id: Optional[str]
    student_id: str
    exam_id: Optional[str]
    predicted_score: Optional[float]
    readiness_score: Optional[float]
    factors: Dict[str, float] = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.utcnow)
