import json
import os
from slack_signature_verifier import slack_signature_verifier as ssv

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
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

    print('event')
    print(event)

    print('context')
    print(context)

    # What is that ?
    slack_request = {
        "body": {
            "token": "cwOw4fvUQavf65dEApYGVLhx",
            "team_id": "T011B56JANA",
            "team_domain": "victor5114-automation",
            "channel_id": "C010ZQC8EM9",
            "channel_name": "discogs-wantlist",
            "user_id": "U011B56JAT0",
            "user_name": "victor.pongnian",
            "command": "/discogs-wantlist",
            "text": "test+command",
            "response_url": "https://hooks.slack.com/commands/T011B56JANA/1036541593571/m0c3ZNy0yKTXf6lwtG4J2tBA",
            "trigger_id": "1036541593651.1045176622758.e97557ee3ed36726442c56815ccecabc"
        },
        "headers": {
            "X-Slack-Signature": "v0=003f31b41baecfe40f196125d018c61889de9b8913f8212750c7193936434b36",
            "X-Slack-Request-Timestamp": "1585917821"
        }
    }

    is_valid_request = ssv.verify_slack_signature(slack_request, os.environ["SLACK_SIGNING_SECRET"])

    print('Signature Results')
    print(is_valid_request)

    response_msg = 'Hello Slack support team'
    
    return respond(None, {
            "response_type": 'in_channel',
            "text": response_msg,
            "attachments": [
                {
                    "text": "If you see this message then this slash command endpoint is working."
                }
            ]
        })
