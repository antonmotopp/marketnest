import io
from fastapi.testclient import TestClient
from main import app
from loguru import logger

client = TestClient(app)

def test_logging_for_404():
    log_output = io.StringIO()
    logger.add(log_output, format="{message}", level="INFO")

    response = client.get("/nonexistent-endpoint")

    logs = log_output.getvalue()
    assert response.status_code == 404
    assert "Status: 404" in logs

