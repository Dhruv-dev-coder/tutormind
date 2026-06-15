from pydantic import BaseModel
from typing import List, Optional

class StudentCreate(BaseModel):
    name: str
    email: str
    class_name: Optional[str]
    board: Optional[str]
    subjects: List[str] = []
    study_hours: Optional[int]

class StudentOut(StudentCreate):
    id: str
