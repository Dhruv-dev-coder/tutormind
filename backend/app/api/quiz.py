from fastapi import APIRouter, Body
from typing import Dict, Any
from app.agents.assessment_agent import AssessmentAgent
from app.database import db

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

    # Retrieve student's roadmap for context
    students = db['students']
    student = await students.find_one({"firebase_uid": student_id}) if not student_id.startswith('_') else await students.find_one({"_id": student_id})
    roadmap = student.get("roadmap") if student else None

    quiz = await assessment.generate_quiz(student_id, subject_id, difficulty, roadmap)
    return {"status": "ok", "quiz": quiz}


@router.post('/submit')
async def submit_quiz(payload: Dict[str, Any] = Body(...)):
    """Submit quiz answers and get evaluation"""
    quiz_id = payload.get('quiz_id')
    answers = payload.get('answers', [])
    questions = payload.get('questions', [])
    
    result = await assessment.evaluate_answers(quiz_id, answers, questions)
    return {"status": "ok", "evaluation": result}
