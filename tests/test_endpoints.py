from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_text_ok():
    payload = {
        "age": 42,
        "smoker": True,
        "exercise": "rarely",
        "diet": "high sugar"
    }
    r = client.post("/api/analyze/text", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "recommendations" in body
