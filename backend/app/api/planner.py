from fastapi import APIRouter, Body
from typing import Dict, Any
from app.agents.langgraph_workflow import LangGraphWorkflow

router = APIRouter()
workflow = LangGraphWorkflow()


@router.post('/generate_roadmap')
async def generate_roadmap(payload: Dict[str, Any] = Body(...)):
    """Generate study roadmap using PlannerAgent via LangGraphWorkflow.

    Expected payload: { student_id, syllabus_text, datesheet_text }
    """
    student_id = payload.get('student_id')
    syllabus_text = payload.get('syllabus_text', '')
    datesheet_text = payload.get('datesheet_text', '')

    # For now pass syllabus bytes as utf-8 bytes to the planner stub
    syllabus_bytes = syllabus_text.encode('utf-8') if isinstance(syllabus_text, str) else b''
    roadmap = await workflow.run_planner_flow(student_id, syllabus_bytes, 'text/plain', datesheet_text)
    return {"status": "ok", "roadmap": roadmap}
