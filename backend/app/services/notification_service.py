"""Notification service that wraps Notification MCP client.

Provides helpers for sending and scheduling in-app/push notifications.
"""
from typing import Dict, Any
from app.mcp import get_notification_mcp


class NotificationService:
    def __init__(self, notification_mcp=None):
        self.notification_mcp = notification_mcp or get_notification_mcp()

    async def send_push(self, student_id: str, title: str, message: str, metadata: Dict[str, Any] = None):
        return await self.notification_mcp.send_push_notification(student_id, title, message, metadata=metadata or {})

    async def schedule(self, student_id: str, when: str, payload: Dict[str, Any]):
        return await self.notification_mcp.schedule_notification(student_id, when, payload)

    async def cancel(self, notification_id: str):
        return await self.notification_mcp.cancel_notification(notification_id)
