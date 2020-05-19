data "aws_iam_policy_document" "discogs_bot_basic_execution" {
  statement {
    sid    = "LambdaGenerateDataKey"
    effect = "Allow"

    actions = [
      "kms:Decrypt",
      "kms:Encrypt",
      "kms:GenerateDataKey",
    ]

    resources = [
      aws_kms_key.sns.arn,
    ]
  }

  statement {
    sid    = "DiscogsBotLambdaBasicExecution"
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = [
      "*",
    ]
  }
}

resource "aws_iam_policy" "discogs_bot_basic_execution_policy" {
  name        = "discogs_bot_basic_execution_policy"
  description = "Basic policies given to lambda functions"
  policy      = data.aws_iam_policy_document.discogs_bot_basic_execution.json
}


data "aws_iam_policy_document" "sns_dispatcher_policy_document" {
  statement {
    sid    = "LambdaDispatcherSNSPolicy"
    effect = "Allow"

    actions = ["sns:Publish"]
    resources = [
      aws_sns_topic.search_release.arn,
      # "${aws_sns_topic.add_to_wantlist.arn}"
    ]
  }
}

resource "aws_iam_policy" "sns_dispatcher_policy" {
  name        = "sns_dispatcher_policy"
  description = "SNS publishing permissions"
  policy      = data.aws_iam_policy_document.sns_dispatcher_policy_document.json
}

data "aws_iam_policy_document" "dynamo_full_user" {
  # DynamoDB
  statement {
    sid    = "DynamoDB"
    effect = "Allow"

    actions = [
      "dynamodb:GetItem",
      "dynamodb:BatchGetItem",
      "dynamodb:PutItem",
      "dynamodb:BatchWriteItem",
      "dynamodb:UpdateItem",
      "dynamodb:DeleteItem",
    ]

    resources = [
      aws_dynamodb_table.user.arn,
    ]
  }
}

resource "aws_iam_policy" "dynamo_full_user_policy" {
  name        = "DynamoFullTableUser"
  description = "Dynamo permissions on User table"
  policy      = data.aws_iam_policy_document.dynamo_full_user.json
}
