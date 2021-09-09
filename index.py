import boto3
import json
from boto3.dynamodb.types import TypeDeserializer
dynamo = boto3.client('dynamodb')


def dynamo_obj_to_python_obj(dynamo_obj: dict) -> dict:
    deserializer = TypeDeserializer()
    return {
        k: deserializer.deserialize(v)
        for k, v in dynamo_obj.items()
    }


def respond(err, res, tablename):
    if not err:
        results = {
            tablename.capitalize(): res
        }
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(results),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.scan(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x)
    }
    operation = event['httpMethod']
    urlpath = event['path']
    table = urlpath.split('/')[-1]
    dbparam = {'TableName': table}
    print('Assuming Scan of Table:', table)
    if operation in operations:
        payload = dbparam if operation == 'GET' else json.loads(event['body'])
        dbitems = operations[operation](dynamo, payload)
        new_format = []
        for i in range(len(dbitems['Items'])):
            new_format.append(dynamo_obj_to_python_obj(dbitems['Items'][i]))
        print('Converted records', json.dumps(new_format, indent=2))
        return respond(None, new_format, table)
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
