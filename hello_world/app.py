import json
import os
import time
import discogs_client
import hmac
import hashlib
import ast

DEBUG = json.loads(os.environ.get('DEBUG', 'false').lower())

def respond(err, res=None, err_code=400):
    return {
        'statusCode': err_code if err else '200',
        'body': json.dumps(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def verify_slack_request(event):

    slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
    request_body = event['body']
    timestamp = event['headers']['X-Slack-Request-Timestamp']

    if abs(time.time() - int(timestamp)) > 60 * 5:
        # The request timestamp is more than five minutes from local time.
        # It could be a replay attack, so let's ignore it.
        print('The request timestamp is more than five minutes from local time.')
        return False

    sig_basestring = 'v0:' + timestamp + ':' + request_body
    # Prepare bytes encoding to feed cryptography function
    secret_bytes_encoded = bytes(slack_signing_secret, 'utf-8')
    sig_basestring_bytes_encoded = bytes(sig_basestring, 'utf-8')

    my_signature_bytes_encoded = 'v0=' + hmac.new(secret_bytes_encoded, msg = sig_basestring_bytes_encoded, digestmod = hashlib.sha256).hexdigest()
    
    slack_signature = event['headers']['X-Slack-Signature']
    return hmac.compare_digest(my_signature_bytes_encoded, slack_signature)


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
    is_request_verified = verify_slack_request(event)

    if not is_request_verified and not DEBUG:
        return respond({
                "response_type": 'in_channel',
                "text": 'Signature verification has failed'
            }, None, 403)

    response_msg = 'Hello Slack support team'
    d = discogs_client.Client('ExampleApplication/0.1')

    return respond(None, {
            "response_type": 'in_channel',
            "text": response_msg,
            "attachments": [
                {
                    "text": "If you see this message then this slash command endpoint is working."
                }
            ]
        })