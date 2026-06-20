from fastapi import APIRouter, HTTPException

from app.api.utils import student_selector
from app.database import db

router = APIRouter()


@router.get("/{student_id}")
async def get_roadmap(student_id: str):
    student = await db["students"].find_one(student_selector(student_id))
    if not student or "roadmap" not in student:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    return {"status": "ok", "roadmap": student["roadmap"]}

