"""
Module for Creating a User Database in DynamoDB
"""
import boto3

# pylint: disable=R0903


class CreateDatabase:

    """
    Class for creating a User Database in DynamoDB
    """

    def __init__(self, table_name):
        self.table_name = table_name

    def create_database(self):
        """
        Creates the database in DynamoDB
        """
        dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')

        table = dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'user_id',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        print("Table status:", table.table_status)
