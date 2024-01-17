from starlette.testclient import TestClient

from src.main import app


client = TestClient(app)


def clone_success_test():
    response = client.post(
        "/clone",
        data={"repo_url": "test", "local_url": "test"},
        headers={"x-hub-signature-256": "sha256=66a0c074deaa0f489ead6537e0d32f9a344b90bbeda705b6ed45ecd3b413fb40"})

    assert response.status_code == 200
    assert response.json().get("message", {}).get("clone")
