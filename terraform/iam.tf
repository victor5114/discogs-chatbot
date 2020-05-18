#  Global policy document for every SNS TOPIC
data "aws_iam_policy_document" "sns_topic_bot_discogs_policy_document" {
  statement {
    sid    = "LambdaDispatcherSNSPolicy"
    effect = "Allow"

    actions = ["sns:Publish"]
    resources = [
      aws_sns_topic.search_release.arn,
      # "${aws_sns_topic.add_to_wantlist.arn}"
    ]
  }


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
}

resource "aws_iam_role_policy" "sns_topic_bot_discogs_policy" {
  name   = "sns_topic_bot_discogs"
  role   = data.aws_iam_role.discogs_bot_command_dispatcher_role.name
  policy = data.aws_iam_policy_document.sns_topic_bot_discogs_policy_document.json
}

