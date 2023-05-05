"""Pytest to test authenticate_user
"""
import pytest
from login.authenticate_user import AuthenticateUser
from login.database import TABLE
from login.hash_password import hash_password


def test_authenticate_user_correct_password(mocker):
    """
    Test authenticate_user when password is correct
    """
    username = "username"
    password = "password"
    hashed_password = hash_password(password)
    mocker.patch.object(TABLE, 'query', return_value={
                        'Items': [{username: 'username', password: hashed_password}]})
    auth = AuthenticateUser(username, password)
    assert auth.authenticate_user() is True


def test_authenticate_user_incorrect_password(mocker):
    """
    Test authenticate_user when password is incorrect.
    """
    username = "username"
    password = "password"
    hashed_password = hash_password("Incorrect")
    mocker.patch.object(TABLE, 'query', return_value={
                        'Items': [{username: 'username', password: hashed_password}]})
    auth = AuthenticateUser(username, password)
    assert auth.authenticate_user() is False


def test_authenticate_user_incorrect_user(mocker):
    """
    Test authenticate_user when user does not exist.
    """
    username = "username"
    password = "password"
    mocker.patch.object(TABLE, 'query', return_value={'Items': []})
    auth = AuthenticateUser(username, password)
    assert auth.authenticate_user() is False
