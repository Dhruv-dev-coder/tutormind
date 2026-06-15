"""MCP health and test endpoints."""
from fastapi import APIRouter, Body, HTTPException
from typing import Dict, Any
from app.mcp import get_email_mcp

router = APIRouter()


@router.get('/mcp/health/email')
async def email_mcp_health():
    """Check Email MCP health status."""
    try:
        mcp = get_email_mcp()
        health = await mcp.health_check()
        return health
    except Exception as e:
        return {"status": "error", "reason": str(e)}


@router.post('/mcp/test/email')
async def test_email_mcp(payload: Dict[str, Any] = Body(...)):
    """Test Email MCP by sending a test email.
    
    Request body:
    {
        "to": "test@example.com",
        "subject": "Test Email",
        "body": "This is a test email from TutorMind EmailMCP"
    }
    """
    try:
        to = payload.get('to')
        subject = payload.get('subject', 'Test Email from TutorMind')
        body = payload.get('body', 'This is a test email.')
        
        if not to:
            raise HTTPException(status_code=400, detail="'to' email address is required")
        
        mcp = get_email_mcp()
        result = mcp.send_email(to=to, subject=subject, body=body)
        return {"status": "success", "message": "Test email sent", "result": result}
    except Exception as e:
        return {"status": "error", "reason": str(e)}


@router.post('/mcp/test/reminder_email')
async def test_reminder_email(payload: Dict[str, Any] = Body(...)):
    """Test Email MCP reminder email async method.
    
    Request body:
    {
        "student_id": "123",
        "subject": "Reminder",
        "body": "Don't forget to study",
        "metadata": {"email": "student@example.com"}
    }
    """
    try:
        student_id = payload.get('student_id')
        subject = payload.get('subject', 'Reminder')
        body = payload.get('body', 'This is a reminder.')
        metadata = payload.get('metadata', {})
        
        mcp = get_email_mcp()
        result = await mcp.send_reminder_email(student_id, subject, body, metadata)
        return result
    except Exception as e:
        return {"status": "error", "reason": str(e)}
