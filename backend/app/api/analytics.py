from fastapi import APIRouter, Body
from typing import Dict, Any
from app.services.analytics_service import AnalyticsService

router = APIRouter()
analytics = AnalyticsService()


@router.get('/weekly_report/{student_id}')
async def weekly_report(student_id: str):
    return await analytics.generate_weekly_report(student_id)


@router.get('/weak_topics/{student_id}')
async def weak_topics(student_id: str):
    return await analytics.detect_weak_topics(student_id)
