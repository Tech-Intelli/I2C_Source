"""
Authenticate user with email address and password
"""
# pylint: disable=E0401
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
        if not response['Items']:
            return False
        hashed_password = response['Items'][0]['password']
        return (len(response['Items']) != 0) and (hash_password(self.password) == hashed_password)

    def get_user_id(self):
        """Get the user id from DynamoDB

        Returns:
            user_id: string
        """
        response = TABLE.query(
            KeyConditionExpression=Key('username').eq(self.username)
        )
        if not response['Items']:
            return "No User Found"
        return response['Items'][0]['user_id']


class ForgetPassword:
    """
    Forget Password with email address
    """

    def __init__(self, username):
        self.username = username

    def forget_password(self, new_password):
        """Forget password
        """
        response = TABLE.query(
            KeyConditionExpression=Key('username').eq(self.username)
        )
        if not response['Items']:
            return False
        user_id = response['Items'][0]['user_id']
        new_password = hash_password(new_password)
        response = TABLE.update_item(
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
