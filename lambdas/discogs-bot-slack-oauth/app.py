import json
import os
import time
import ast
import boto3
import requests
from json.decoder import JSONDecodeError

sns_client = boto3.client('sns')

DEBUG = json.loads(os.environ.get('DEBUG', 'false').lower())

def respond(err, res=None, err_code=400, content_type='application/json'):
    """ Format browser readable http response. """
    return {
        'statusCode': err_code if err else '200',
        'body': json.dumps(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': content_type,
        },
    }


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    return respond(None, {
            "response_type": 'in_channel',
            "text": 'hello world - oauth',
            "attachments": [
                {
                    "text": "If you see this message then this slash command endpoint is working."
                }
            ]
        })