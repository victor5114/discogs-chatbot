import json
import os
import time
import hmac
import hashlib
import ast
import boto3
from json.decoder import JSONDecodeError

sns_client = boto3.client('sns')

DEBUG = json.loads(os.environ.get('DEBUG', 'false').lower())

# SNS TOPICS TO DISPATCH
SNS_TOPIC_SEARCH_RELEASE = 'arn:aws:sns:eu-west-3:618464369307:search-release'



def respond(err, res=None, err_code=400, content_type='application/json'):
    """ Format browser readable http response. """
    return {
        'statusCode': err_code if err else '200',
        'body': json.dumps(err) if err else json.dumps(res),
        'headers': {
            'Content-Type': content_type,
        },
    }

def _formparams_to_dict(req_body):
    """ Converts the incoming form_params from Slack into a dictionary. """
    retval = {}
    for val in req_body.split('&'):
        k, v = val.split('=')
        retval[k] = v
    return retval


def verify_slack_request(event):
    """ Verify if requests come from Slack system. """
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

    # Get useful payload from request body
    req_body = event['body']
        
    # Validate Slack Event API Challenge
    if event['headers']['Content-Type'] == 'application/json':
        try:
            _body = json.loads(req_body)
            assert _body.get('type') == 'url_verification'
            return respond(None, _body.get('challenge'), 'text/plain')
        except JSONDecodeError:
            return respond({
                "response_type": 'in_channel',
                "text": 'Challenge decoding has failed'
            }, None, 403)

    try:
        params = _formparams_to_dict(req_body)
        
        # command_list is a sequence of strings in the slash command such as "slashcommand weather pune"
        command_list = params['text'].split('+')

        # publish SNS message to delegate the actual work to worker lambda function
        message = {
            "params": params,
            "command_list": command_list
        }

        # print(message)

        sns_response = sns_client.publish(
            TopicArn=SNS_TOPIC_SEARCH_RELEASE,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )
        response_msg = "Ok, working on your slash command ..."
    except Exception as e:
        response_msg = '[ERROR] {}'.format(str(e))

    return respond(None, {
            "response_type": 'in_channel',
            "text": response_msg,
            "attachments": [
                {
                    "text": "If you see this message then this slash command endpoint is working."
                }
            ]
        })