import json
import boto3

def put_into_table(event, context):
    dynamodb = boto3.resource('dynamodb')
    tableName = "Books"
    newItem = event['new-item']

    table = dynamodb.Table(tableName)
    table.put_item(Item=newItem)

    body = {
        "success": "true",
        "table-name": tableName,
        "new-item": newItem
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
