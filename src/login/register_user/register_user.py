"""
Module that registers users into the database
"""

import uuid
# pylint: disable=E0401
from boto3.dynamodb.conditions import Key
from ..database import TABLE
from ..hash_password import hash_password

# pylint: disable=R0903


class RegisterUser:
    """
    Register a user into the database
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register_user(self):
        """
        Register the user to the database
        """
        hashed_password = hash_password(self.password)

        user_id = int(uuid.uuid4().int & (1 << 31)-1)
        is_existing_user = TABLE.query(
            KeyConditionExpression=Key('username').eq(self.username)
        )
        if len(is_existing_user['Items']) != 0 and \
                is_existing_user['Items'][0]['username'] == self.username:
            return 400
        response = TABLE.put_item(
            Item={
                'username': self.username,
                'user_id': user_id,
                'password': hashed_password,
                'verified': False
            }
        )
        return response['ResponseMetadata']['HTTPStatusCode']
