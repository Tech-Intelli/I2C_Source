"""
Module that registers users into the database
"""

import os
import ssl
import uuid
import smtplib
from email.message import EmailMessage

from boto3.dynamodb.conditions import Key
from ..database import TABLE, get_user_id
from ..hash_password import hash_password
from logger import log


EMAIL_VERIFICATION_UNIQUE_ID = {}


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
            f"Please click the following link to verify your email:\n\n{url}/{unique_id}"
        )
        msg["Subject"] = "Email Verification"
        msg["From"] = os.environ["EMAIL_ADDRESS"]
        msg["To"] = self.username
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            try:
                server.login(os.environ["EMAIL_ADDRESS"], os.environ["EMAIL_PASSWORD"])
                server.sendmail(
                    os.environ["EMAIL_ADDRESS"], self.username, msg.as_string()
                )
                EMAIL_VERIFICATION_UNIQUE_ID[self.username] = unique_id
            except Exception as error:
                log.error(f"Unable to send email due to error: \n{error}")

    def register_user(self):
        """
        Register the user to the database
        """
        hashed_password = hash_password(self.password)

        user_id = int(uuid.uuid4().int & (1 << 31) - 1)
        is_existing_user = TABLE.query(
            KeyConditionExpression=Key("username").eq(self.username)
        )
        if (
            len(is_existing_user["Items"]) != 0
            and is_existing_user["Items"][0]["username"] == self.username
        ):
            return 400
        unique_id = str(uuid.uuid4())
        response = TABLE.put_item(
            Item={
                "username": self.username,
                "user_id": user_id,
                "password": hashed_password,
                "verified": False,
            }
        )
        self.send_email("https://www.explaistic.com/verify", unique_id)
        return response["ResponseMetadata"]["HTTPStatusCode"]


class VerifyEmail:
    """Verifies the email address"""

    @staticmethod
    def verify_email(unique_id):
        """verify email address based on unique_id

        Args:
            unique_id (string): Unique Identifier
        """
        email = [
            key
            for key, value in EMAIL_VERIFICATION_UNIQUE_ID.items()
            if value == unique_id
        ]
        if email:
            email = email[0]
            del EMAIL_VERIFICATION_UNIQUE_ID[email]
            verified_status = True
            TABLE.update_item(
                Key={"username": email, "user_id": get_user_id(email)},
                UpdateExpression="SET verified = :val",
                ExpressionAttributeValues={":val": verified_status},
            )
            return True
        return False
