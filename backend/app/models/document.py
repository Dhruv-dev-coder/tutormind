from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Document(BaseModel):
    id: Optional[str]
    student_id: Optional[str]
    filename: str
    content_type: Optional[str]
    source: Optional[str]
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = False
    metadata: dict = Field(default_factory=dict)
