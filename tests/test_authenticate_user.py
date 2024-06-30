"""Pytest to test authenticate_user
"""

# pylint: disable=E0401
import os
import jwt
from src.login.authenticate_user import AuthenticateUser
from src.login.database import TABLE
from src.login.hash_password import hash_password


def test_authenticate_user_correct_password(mocker):
    """
    Test authenticate_user when password is correct
    """
    username = "username"
    password = "password"
    verified = True
    hashed_password = hash_password(password)
    mocker.patch.object(
        TABLE,
        "query",
        return_value={
            "Items": [
                {
                    "username": username,
                    "password": hashed_password,
                    "verified": verified,
                }
            ]
        },
    )
    auth = AuthenticateUser(username, password)
    assert auth.authenticate_user() is True


def test_authenticate_user_incorrect_password(mocker):
    """
    Test authenticate_user when password is incorrect.
    """
    username = "username"
    password = "password"
    verified = True
    hashed_password = hash_password("Incorrect")
    mocker.patch.object(
        TABLE,
        "query",
        return_value={
            "Items": [
                {
                    "username": username,
                    "password": hashed_password,
                    "verified": verified,
                }
            ]
        },
    )
    auth = AuthenticateUser(username, password)
    assert auth.authenticate_user() is False


def test_authenticate_user_not_verified(mocker):
    """
    Test authenticate_user when password is incorrect.
    """
    username = "username"
    password = "password"
    verified = False
    hashed_password = hash_password("password")
    mocker.patch.object(
        TABLE,
        "query",
        return_value={
            "Items": [
                {
                    "username": username,
                    "password": hashed_password,
                    "verified": verified,
                }
            ]
        },
    )
    auth = AuthenticateUser(username, password)
    assert auth.authenticate_user() is False


def test_authentication_token(mocker):
    """
    Test authentication token generation
    """

    username = "username"
    user_id = "user_id"
    password = "password"
    verified = True
    hashed_password = hash_password("password")
    mocker.patch.object(
        TABLE,
        "query",
        return_value={
            "Items": [
                {
                    "username": username,
                    "password": hashed_password,
                    "verified": verified,
                }
            ]
        },
    )
    auth = AuthenticateUser(username, password)
    token = auth.generate_auth_token(user_id)
    email = ""
    try:
        payload = jwt.decode(token, os.environ["AUTH_SECRET_KEY"], algorithms=["HS256"])
        email = payload["email"]
        print(username)
        print(email)
        assert username == email
    except jwt.ExpiredSignatureError:
        assert False
    except jwt.InvalidTokenError:
        assert False


def test_authenticate_user_incorrect_user(mocker):
    """
    Test authenticate_user when user does not exist.
    """
    username = "username"
    password = "password"
    mocker.patch.object(TABLE, "query", return_value={"Items": []})
    auth = AuthenticateUser(username, password)
    assert auth.authenticate_user() is False
