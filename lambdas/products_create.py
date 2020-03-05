import json
import boto3
import decimal
import uuid
import urllib3
from http import HTTPStatus
from datetime import datetime

ANALYTICS_URL = 'https://7qsoyqlued.execute-api.us-east-1.amazonaws.com/latest/analytics?action=create_products'


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):

    try:
        table = get_dynamo_table()

        response = insert_item(event, table)

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            send_to_analytics(event)
            return event
        else:
            return {
                "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                "body": json.dumps({"message": "error"})
            }
    except:
        return {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": json.dumps({"message": "error"})
        }


def insert_item(event, table):
    id = uuid.uuid1()
    payload = event
    payload.update({'id': id.hex})
    response = table.put_item(Item=payload)
    return response


def get_dynamo_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('products')
    return table


def send_to_analytics(payload):
    payload['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(payload['timestamp'])

    http = urllib3.PoolManager()

    response = http.request('POST',
                            ANALYTICS_URL,
                            body=json.dumps(payload),
                            retries=False)

    print(response.status)
