import pytest
import boto3
from moto import mock_dynamodb2
import lambdas.products_create as products_create

@mock_dynamodb2
def test_get_dynamo_db():
    create_dynamo_table()

    actual_table = products_create.get_dynamo_table()

    assert actual_table.name == 'products'

def create_dynamo_table():
    dynamodb = boto3.resource('dynamodb', 'us-east-1')
    table = dynamodb.create_table(
        TableName='products',
        KeySchema=[
            {
                'AttributeName': 'sku',
                'KeyType': 'string'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'sku',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    return table
