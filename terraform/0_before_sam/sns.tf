
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



