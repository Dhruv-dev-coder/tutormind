"""Notification MCP server stub.

Handles in-app and push notifications through MPC. Production must route via
an MCP gateway to APNs/FCM and in-app websockets.
"""
from typing import Dict, Any


class NotificationMCP:
    async def send_push_notification(self, student_id: str, title: str, message: str, metadata: Dict[str, Any] = None):
        return {"status": "sent", "student_id": student_id}

    async def schedule_notification(self, student_id: str, when: str, payload: Dict[str, Any]):
        return {"status": "scheduled", "when": when, "payload": payload}

    async def cancel_notification(self, notification_id: str):
        return {"status": "cancelled", "notification_id": notification_id}
