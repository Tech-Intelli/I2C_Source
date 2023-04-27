"""
Authenticate user with email address and password
"""

from boto3.dynamodb.conditions import Key
from ..database import TABLE
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

        hashed_password = response['Items'][0]['password']
        return (len(response['Items']) != 0) and (hash_password(self.password) == hashed_password)
