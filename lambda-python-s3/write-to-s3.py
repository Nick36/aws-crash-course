import json
import boto3

def save_to_bucket(event, context):
    s3 = boto3.resource('s3')
    bucketName = event['bucket-name']
    path = event['file-path']
    data = event['file-content']

    bucket = s3.Bucket(bucketName)
    bucket.put_object(
        ContentType='application/json',
        Key=path,
        Body=data,
    )

    body = {
        "uploaded": "true",
        "bucket": bucketName,
        "path": path,
    }

    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
