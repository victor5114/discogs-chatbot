
############################################################
#               One Topic by command type                  #
############################################################
resource "aws_sns_topic" "search_release" {
  name              = "search-release"
  display_name      = "Search Release Bus"
  kms_master_key_id = aws_kms_key.sns.key_id
  tags = merge(
    local.common_tags,
    map(
      "Name", "sns-topic-search-release"
    )
  )
}

# resource "aws_sns_topic_policy" "search-release-policy" {
#   arn    = aws_sns_topic.search_release.arn
#   policy = data.aws_iam_policy_document.sns_topic_bot_discogs_policy_document.json
# }

# resource "aws_sns_topic_subscription" "sns_mybizz_ventes" {
#   topic_arn = "${aws_sns_topic.search_release.arn}"
#   protocol  = "lambda"
#   endpoint  = "${data.aws_lambda_function.[release-search].arn}"
# }



