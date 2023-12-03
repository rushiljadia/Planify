def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200


def test_sign_up(client):
    response = client.get("/sign-up")
    assert response.status_code == 200
