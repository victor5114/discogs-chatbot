###########################################
# Lambda resources will be created by SAM #
###########################################
data "aws_iam_policy_document" "assume_lambda" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

################### DISPATCHER ROLE ######################
resource "aws_iam_role" "discogs_bot_dispatcher_role" {
  path               = "/lambda/"
  name               = "dispatcher"
  description        = "Custom role for dispatcher function"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda.json
}
# Dispatcher role policy attachment
resource "aws_iam_role_policy_attachment" "discogs_bot_dispatcher_role_basic_attachment" {
  role       = aws_iam_role.discogs_bot_dispatcher_role.name
  policy_arn = aws_iam_policy.discogs_bot_basic_execution_policy.arn
}

resource "aws_iam_role_policy_attachment" "discogs_bot_dispatcher_role_sns_attachment" {
  role       = aws_iam_role.discogs_bot_dispatcher_role.name
  policy_arn = aws_iam_policy.sns_dispatcher_policy.arn
}

resource "aws_iam_role_policy_attachment" "discogs_bot_dispatcher_role_sns_dynamo" {
  role       = aws_iam_role.discogs_bot_dispatcher_role.name
  policy_arn = aws_iam_policy.dynamo_full_user_policy.arn
}

output "dispatcher_role_arn" {
  value = aws_iam_role.discogs_bot_dispatcher_role.arn
}

################### SEARCH RELEASE ROLE ######################
resource "aws_iam_role" "discogs_bot_search_release_role" {
  path               = "/lambda/"
  name               = "search-release"
  description        = "Custom role for searche release function"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda.json
}
# Search release role policy attachment
resource "aws_iam_role_policy_attachment" "discogs_bot_search_release_role_basic_attachment" {
  role       = aws_iam_role.discogs_bot_search_release_role.name
  policy_arn = aws_iam_policy.discogs_bot_basic_execution_policy.arn
}

resource "aws_iam_role_policy_attachment" "discogs_bot_search_release_role_sns_dynamo" {
  role       = aws_iam_role.discogs_bot_search_release_role.name
  policy_arn = aws_iam_policy.dynamo_full_user_policy.arn
}

output "search_release_role_arn" {
  value = aws_iam_role.discogs_bot_search_release_role.arn
}
