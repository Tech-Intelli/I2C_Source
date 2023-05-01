"""
Define DynamoDB and Table
"""
# pylint: disable=E0401
import boto3

DYNAMODB = boto3.resource('dynamodb', region_name='eu-central-1')
TABLE = DYNAMODB.Table('UserRegistration')
