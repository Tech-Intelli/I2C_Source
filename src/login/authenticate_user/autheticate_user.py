"""
Authenticate user with email address and password
"""
# pylint: disable=E0401
import os
from datetime import datetime, timedelta
import jwt
from boto3.dynamodb.conditions import Key
from ..database import TABLE, get_user_id
from ..hash_password import hash_password
# pylint: disable=R0903


class AuthenticateUser:
    """
    Authenticate user with email address and password
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate_user(self):
        """
        Authenticate user.
        """
        response = TABLE.query(
            KeyConditionExpression=Key('username').eq(self.username)
        )
        if not response['Items']:
            return False
        if not response['Items'][0]['verified']:
            print("Please verify your email address.")
            return False
        hashed_password = response['Items'][0]['password']
        return (len(response['Items']) != 0) and (hash_password(self.password) == hashed_password)

    def generate_auth_token(self):
        """Generate an authentication token

        Returns:
            _type_: _description_
        """
        expires_in = timedelta(hours=1)
        expiration = datetime.utcnow() + expires_in
        payload = {
            'user_id': str(get_user_id(self.username)),
            'email': self.username,
            'exp': expiration
        }
        return jwt.encode(payload, os.environ['AUTH_SECRET_KEY'], algorithm='HS256')


class ForgetPassword:
    """
    Forget Password with email address
    """

    def __init__(self, username):
        self.username = username

    def forget_password(self, new_password):
        """Forget password
        """
        user_id = get_user_id(self.username)
        new_password = hash_password(new_password)
        TABLE.update_item(
            Key={
                "username": self.username,
                "user_id": user_id,
            },
            UpdateExpression="SET #password = :new_password",
            ExpressionAttributeNames={
                "#password": "password"
            },
            ExpressionAttributeValues={
                ":new_password": new_password
            }
        )
        return True
