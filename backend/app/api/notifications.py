from fastapi import APIRouter, Body
from typing import Dict, Any
from app.services.notification_service import NotificationService
from app.services.email_service import EmailService

router = APIRouter()
notif = NotificationService()
email_svc = EmailService()


@router.post('/send')
async def send_notification(payload: Dict[str, Any] = Body(...)):
    student_id = payload.get('student_id')
    title = payload.get('title')
    message = payload.get('message')
    return await notif.send_push(student_id, title, message, metadata=payload.get('metadata'))


@router.post('/schedule')
async def schedule_notification(payload: Dict[str, Any] = Body(...)):
    student_id = payload.get('student_id')
    when = payload.get('when')
    payload_data = payload.get('payload', {})
    return await notif.schedule(student_id, when, payload_data)


@router.post('/send_email')
async def send_email(payload: Dict[str, Any] = Body(...)):
    student_id = payload.get('student_id')
    subject = payload.get('subject')
    body = payload.get('body')
    return await email_svc.send_generic(student_id, subject, body, metadata=payload.get('metadata'))
