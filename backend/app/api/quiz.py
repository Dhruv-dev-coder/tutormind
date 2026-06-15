from fastapi import APIRouter, Body
from typing import Dict, Any
from app.agents.assessment_agent import AssessmentAgent

router = APIRouter()
assessment = AssessmentAgent()


@router.post('/generate')
async def generate_quiz(payload: Dict[str, Any] = Body(...)):
    """Generate a quiz for a student.

    Expected payload: { student_id, subject_id, difficulty }
    """
    student_id = payload.get('student_id')
    subject_id = payload.get('subject_id')
    difficulty = payload.get('difficulty', 'medium')

    quiz = await assessment.generate_quiz(student_id, subject_id, difficulty)
    return {"status": "ok", "quiz": quiz}
