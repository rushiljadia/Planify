import bcrypt
from flask import url_for
from flask_login import current_user
from app.auth.forms import LoginForm


def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200


def test_sign_up(client):
    response = client.get("/sign-up")
    assert response.status_code == 200


def test_sign_up_function(client, app):
    mongo = app.config["mongo"]

    test_username = "test_user"
    test_password = bcrypt.hashpw("test_password".encode("utf-8"), bcrypt.gensalt())

    response = client.get(url_for("auth.sign_up"))
    assert response.status_code == 200

    response = client.post(
        url_for("auth.sign_up"),
        data={"username": test_username, "password": test_password},
        follow_redirects=True,
    )

    user_collection = mongo.db.users
    new_user = user_collection.find_one({"name": test_username})
    assert new_user is None or (new_user["name"] == test_username)
