"""
Module that registers users into the database
"""

import uuid
from ..database import TABLE
from ..hash_password import hash_password
from boto3.dynamodb.conditions import Key


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
        isExistingUser = TABLE.query(
            KeyConditionExpression=Key('username').eq(self.username)
        )
        if len(isExistingUser['Items']) != 0 and \
                isExistingUser['Items'][0]['username'] == self.username:
            return 400
        response = TABLE.put_item(
            Item={
                'username': self.username,
                'user_id': user_id,
                'password': hashed_password
            }
        )
        return response['ResponseMetadata']['HTTPStatusCode']
