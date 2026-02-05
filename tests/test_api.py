from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    # Ensure backend is up and running before other tests
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

def test_query_validation():
    # Verify that the system enforces company_id for data isolation
    # This is a core security requirement for multi-tenancy
    payload = {"query": "What are our revenue targets?"}
    response = client.post("/query", json=payload)
    assert response.status_code == 422