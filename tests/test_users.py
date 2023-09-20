from flask import session, request
import pytest

from types import SimpleNamespace

from flask_app.forms import RegistrationForm
from flask_app.models import User


def test_register(client, auth):
    """ Test that registration page opens up """
    resp = client.get("/register")
    assert resp.status_code == 200

    response = auth.register()

    assert response.status_code == 200
    user = User.objects(username="test").first()

    assert user is not None


@pytest.mark.parametrize(
    ("username", "email", "password", "confirm", "message"),
    (
        ("test", "test@email.com", "test", "test", b"Username is taken"),
        ("p" * 41, "test@email.com", "test", "test", b"Field must be between 1 and 40"),
        ("username", "test", "test", "test", b"Invalid email address."),
        ("username", "test@email.com", "test", "test2", b"Field must be equal to"),
    ),
)
def test_register_validate_input(auth, username, email, password, confirm, message):
    if message == b"Username is taken":
        auth.register()

    response = auth.register(username, email, password, confirm)

    assert message in response.data


def test_login(client, auth):
    """ Test that login page opens up """
    resp = client.get("/login")
    assert resp.status_code == 200

    auth.register()
    response = auth.login()

    with client:
        client.get("/")
        assert session["_user_id"] == "test"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "password123", b"This field is required"),  # Missing username
        ("test", "", b"This field is required"),  # Missing password
        ("bad_username", "password123", b"Login failed. Check your username and/or password"),  # Bad username
        ("test", "bad_password", b"Login failed. Check your username and/or password"),  # Bad password
    )
)
def test_login_input_validation(auth, username, password, message):
    if message == b"Login failed. Check your username and/or password.":
        auth.register("test", "test@email.com", "password123")
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.register()
    auth.login()
    with client:
        client.get("/")
        assert session["_user_id"] == "test"
        response = auth.logout()
        assert response.status_code == 302
        assert "_user_id" not in session


def test_change_username(client, auth):
    auth.register("test", "test@email.com", "password123")
    auth.login("test", "password123")

    response = client.get("/account")
    assert response.status_code == 302

    new_username = "new_test"
    response = client.post("/account", data={"username": new_username})
    assert response.status_code == 302

    response = client.get("/account")
    assert response.status_code == 302


def test_change_username_taken(client, auth):
    auth.register()
    auth.register("test2", "test2@email.com", "test", "test")
    auth.login()
    with client:
        client.get("/account")
        data = {"username": "test2"}
        response = client.post("/account", data=data, follow_redirects=True)
        assert b"That username is already taken" in response.data


@pytest.mark.parametrize(
    ("new_username", "message"),
    (
        ("", b"This field is required."),
        ("a" * 41, b"Field must be between 1 and 40 characters long."),
    ),
)
def test_change_username_input_validation(client, auth, new_username, message):
    auth.register()
    auth.login()
    with client:
        client.get("/account")
        data = {"username": new_username}
        response = client.post("/account", data=data, follow_redirects=True)
        assert message in response.data
