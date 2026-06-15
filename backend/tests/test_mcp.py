"""Test MCP endpoints integration."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_email_mcp_health():
    """Test Email MCP health check endpoint."""
    response = client.get("/api/mcp/health/email")
    assert response.status_code == 200
    assert "status" in response.json()


def test_email_mcp_test_endpoint():
    """Test Email MCP test endpoint (will fail without email config, but endpoint should exist)."""
    payload = {
        "to": "test@example.com",
        "subject": "Test",
        "body": "Test message"
    }
    response = client.post("/api/mcp/test/email", json=payload)
    assert response.status_code == 200
    assert "status" in response.json()


def test_email_mcp_reminder_test():
    """Test Email MCP reminder async method."""
    payload = {
        "student_id": "123",
        "subject": "Test Reminder",
        "body": "Test reminder message",
        "metadata": {"email": "test@example.com"}
    }
    response = client.post("/api/mcp/test/reminder_email", json=payload)
    assert response.status_code == 200
    assert "status" in response.json()
