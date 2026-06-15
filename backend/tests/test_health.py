from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get('/api/health')
    assert resp.status_code == 200
    assert resp.json().get('status') == 'ok'


def test_auth_status():
    resp = client.get('/api/auth/status')
    assert resp.status_code == 200
    assert resp.json().get('auth') == 'ready'
