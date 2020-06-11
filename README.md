# discogs-bot

## TODO
- [x] Test SNS publish
- [x] Move Terraform dependencies in an other folder and use terraform remote storage to separate what's needed before Discogs Lambda Application bootstrap and what can be created afterward.
- [] Move Oauth code from dispatcher to slack Oauth function (Not sure Oauth will be used)
- [] Test and query Discogs API
- [] Test Dialogflow API/SDK
- [] Create Google cloud resources with terraform (IAM  mostly)

## Resources
[detect intent w/ dialogflow](https://cloud.google.com/dialogflow/docs/quick/api?hl=fr#detect-intent-text-python)
[Discogs Python client](https://github.com/discogs/discogs_client/tree/d8c0620a02dbd98be5aceefc4c8d7f0bbe8c7001)
[Discogs API]()
[Boto3 SDK - DynamoDB](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client)
[Slack Block kit builder](https://api.slack.com/tools/block-kit-builder)