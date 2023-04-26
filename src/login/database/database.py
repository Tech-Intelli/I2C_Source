"""
Define DynamoDB and Table
"""
import boto3

DYNAMODB = boto3.resource('dynamodb', region_name='eu-central-1')
TABLE = DYNAMODB.Table('UserRegistration')
