import pytest
import boto3
from moto import mock_dynamodb2
import lambdas.products_list as products_list

@mock_dynamodb2
def test_get_dynamo_db():
    create_dynamo_table()

    actual_table = products_list.get_dynamo_table()

    assert actual_table.name == 'products'

# @mock_dynamodb2
# def test_execute_query_sku():
#     event = {"queryStringParameters": {"sku": 1}}
#
#     insert_samples(create_dynamo_table())

    # table = products_list.get_dynamo_table()
    #
    # actual_result = products_list.execute_query(event, table)
    # expected_result = [{'sku': '1', 'name': 'test'}]
    #
    # print(actual_result)
    #
    # assert len(actual_result) == len(expected_result)




def insert_samples(table):
    item_1 = {'sku': '1', 'name': 'test'}
    item_2 = {'sku': '2', 'name': 'test'}

    table.put_item(Item=item_1)
    table.put_item(Item=item_2)

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

