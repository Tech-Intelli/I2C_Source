"""
Define DynamoDB and Table
"""

import boto3
from boto3.dynamodb.conditions import Key

DYNAMODB = boto3.resource("dynamodb", region_name="eu-central-1")
TABLE = DYNAMODB.Table("UserRegistration")


def get_user_id(username):
    """Get the user id from DynamoDB

    Returns:
        user_id: string
    """
    response = TABLE.query(KeyConditionExpression=Key("username").eq(username))
    if not response["Items"]:
        return "No User Found"
    return response["Items"][0]["user_id"]
