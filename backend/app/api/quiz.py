from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, Query
from typing import Dict, Any
from app.agents.assessment_agent import AssessmentAgent
from app.api.utils import student_selector
from app.database import db

router = APIRouter()
assessment = AssessmentAgent()


@router.post('/generate')
async def generate_quiz(payload: Dict[str, Any] = Body(...)):
    """Generate a quiz for a student.

    Expected payload: { student_id, subject_id, difficulty }
    """
    student_id = payload.get('student_id')
    subject_id = payload.get('subject_id') or payload.get('topic')
    difficulty = payload.get('difficulty', 'medium')

    if not student_id:
        raise HTTPException(status_code=400, detail='student_id required')
    if not subject_id:
        raise HTTPException(status_code=400, detail='topic required')

    # Retrieve student's roadmap for context
    students = db['students']
    student = await students.find_one(student_selector(student_id))
    roadmap = student.get("roadmap") if student else None

    quiz = await assessment.generate_quiz(student_id, subject_id, difficulty, roadmap)
    await db["quiz_attempts"].insert_one({
        "student_id": student_id,
        "topic": subject_id,
        "quiz_id": quiz.get("quiz_id"),
        "difficulty": difficulty,
        "quiz": quiz,
        "status": "generated",
        "created_at": datetime.utcnow().isoformat(),
    })
    return {"status": "ok", "quiz": quiz}


@router.post('/submit')
async def submit_quiz(payload: Dict[str, Any] = Body(...)):
    """Submit quiz answers and get evaluation"""
    quiz_id = payload.get('quiz_id')
    student_id = payload.get('student_id')
    topic = payload.get('topic') or payload.get('subject_id')
    answers = payload.get('answers', [])
    questions = payload.get('questions', [])
    
    result = await assessment.evaluate_answers(quiz_id, answers, questions)
    weak_areas = [
        topic_name
        for topic_name, data in result.get("analysis", {}).get("topic_breakdown", {}).items()
        if data.get("accuracy", 0) < 60
    ]
    result["weak_areas"] = weak_areas

    if student_id:
        await db["quiz_attempts"].insert_one({
            "student_id": student_id,
            "topic": topic,
            "quiz_id": quiz_id,
            "answers": answers,
            "questions": questions,
            "evaluation": result,
            "status": "submitted",
            "created_at": datetime.utcnow().isoformat(),
        })
    return {"status": "ok", "evaluation": result}


@router.get('/history')
async def quiz_history(
    student_id: str = Query(...),
    topic: str = Query(default=None),
):
    query = {"student_id": student_id}
    if topic:
        query["topic"] = {"$regex": f"^{topic}$", "$options": "i"}

    attempts = []
    cursor = db["quiz_attempts"].find(query).sort("created_at", -1)
    async for attempt in cursor:
        attempt["_id"] = str(attempt["_id"])
        attempts.append(attempt)

    return {"status": "ok", "attempts": attempts}
