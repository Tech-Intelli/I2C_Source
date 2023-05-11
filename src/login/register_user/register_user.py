"""
Module that registers users into the database
"""

import os
import ssl
import uuid
import smtplib
from email.message import EmailMessage
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

    def send_email(self, url, unique_id):
        """Send and email to the user to verify the email address"""
        msg = EmailMessage()
        msg.set_content(
            f"Please click the following link to verify your email:\n\n{url}/{unique_id}")
        msg["Subject"] = "Email Verification"
        msg["From"] = os.environ["EMAIL_ADDRESS"]
        msg["To"] = self.username
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(os.environ["EMAIL_ADDRESS"],
                         os.environ["EMAIL_PASSWORD"])
            server.sendmail(os.environ["EMAIL_ADDRESS"],
                            self.username, msg.as_string())

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
        unique_id = str(uuid.uuid4())
        self.send_email("http://localhost:9000/somevalue/", unique_id)
        response = TABLE.put_item(
            Item={
                'username': self.username,
                'user_id': user_id,
                'password': hashed_password,
                'verified': False
            }
        )
        return response['ResponseMetadata']['HTTPStatusCode']
