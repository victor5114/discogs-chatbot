import json
import os
import time
import ast
import boto3
import requests
from json.decoder import JSONDecodeError

sns_client = boto3.client('sns')

DEBUG = json.loads(os.environ.get('DEBUG', 'false').lower())

# SNS TOPICS TO DISPATCH
SNS_TOPIC_SEARCH_RELEASE = os.environ.get('DEBUG')


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
    message = json.loads(event['Records'][0]['Sns']['Message'])
    param_map = message['params']
    response_url = param_map['response_url']

    command_list = message['command_list']
    main_command = command_list[0].lower()
    return respond(None, {
            "response_type": 'in_channel',
            "text": 'hello world - search release',
            "attachments": [
                {
                    "text": "If you see this message then this slash command endpoint is working."
                }
            ]
        })