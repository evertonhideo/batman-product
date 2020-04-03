import json
import boto3
import decimal
from http import HTTPStatus
from boto3.dynamodb.conditions import Key, Attr


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):
    print(event)

    try:
        table = get_dynamo_table()

        response = execute_query(event, table)

        product_list = []

        for i in response['Items']:
            if isinstance(event["queryStringParameters"], dict) and "id" in event["queryStringParameters"]:
                id = event["queryStringParameters"]['id']
                if id == i['id']:
                    return {
                        "statusCode": HTTPStatus.OK,
                        "body": json.dumps(i, cls=DecimalEncoder)
                    }
            else:
                product_list.append(i)

        return {
            "statusCode": HTTPStatus.OK,
            "body": json.dumps(product_list, cls=DecimalEncoder)

        }
    except:
        return {
            "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
            "body": json.dumps({"message": "error"})
        }



def execute_query(event, table):
    if isinstance(event["queryStringParameters"], dict) and "sku" in event["queryStringParameters"]:
        sku = event["queryStringParameters"]['sku']
        response = table.query(KeyConditionExpression=Key('sku').eq(sku))

    else:
        response = table.scan()
    return response


def get_dynamo_table():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('products')
    return table

