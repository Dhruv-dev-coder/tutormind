from fastapi import APIRouter, Body, File, UploadFile, HTTPException
from typing import Dict, Any
from app.database import db
from app.agents.langgraph_workflow import LangGraphWorkflow
from datetime import datetime

router = APIRouter()
workflow = LangGraphWorkflow()


@router.post('/initialize')
async def initialize_student(payload: Dict[str, Any] = Body(...)):
    """Initialize student with syllabus and datesheet to generate roadmap"""
    student_id = payload.get('student_id')
    syllabus_text = payload.get('syllabus_text', '')
    datesheet_text = payload.get('datesheet_text', '')
    
    if not student_id:
        raise HTTPException(status_code=400, detail='student_id required')
    
    # Generate roadmap using planner agent
    try:
        roadmap = await workflow.run_planner_flow(student_id, syllabus_text.encode('utf-8'), 'text/plain', datesheet_text)
    except Exception as e:
        roadmap = {
            "error": "Failed to generate roadmap",
            "message": str(e),
            "student_id": student_id
        }
    
    # Store roadmap in database
    students = db['students']
    await students.update_one(
        {"_id": student_id} if not student_id.startswith('_') else {"firebase_uid": student_id},
        {
            "$set": {
                "roadmap": roadmap,
                "onboarded": True,
                "onboarded_at": datetime.utcnow().isoformat(),
                "syllabus_text": syllabus_text,
                "datesheet_text": datesheet_text
            }
        },
        upsert=True
    )
    
    return {
        "status": "ok",
        "message": "Student initialized with roadmap",
        "roadmap": roadmap
    }


@router.get('/status/{student_id}')
async def onboarding_status(student_id: str):
    """Check onboarding status of a student"""
    students = db['students']
    student = await students.find_one(
        {"_id": student_id} if not student_id.startswith('_') else {"firebase_uid": student_id}
    )
    
    if not student:
        return {"status": "not_found"}
    
    return {
        "status": "ok",
        "onboarded": student.get("onboarded", False),
        "onboarded_at": student.get("onboarded_at"),
        "has_roadmap": "roadmap" in student,
        "roadmap_summary": {
            "total_chapters": student.get("roadmap", {}).get("total_chapters"),
            "exam_date": student.get("roadmap", {}).get("exam_date"),
            "days_remaining": student.get("roadmap", {}).get("days_remaining")
        } if "roadmap" in student else None
    }


@router.get('/roadmap/{student_id}')
async def get_student_roadmap(student_id: str):
    """Retrieve student's personalized roadmap"""
    students = db['students']
    student = await students.find_one(
        {"_id": student_id} if not student_id.startswith('_') else {"firebase_uid": student_id}
    )
    
    if not student or "roadmap" not in student:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    
    return {
        "status": "ok",
        "roadmap": student["roadmap"]
    }
