resource "aws_dynamodb_table" "user" {
  name         = "slack-user"
  hash_key     = "SlackID"
  billing_mode = "PAY_PER_REQUEST"

  attribute {
    name = "SlackID"
    type = "S"
  }

  ttl {
    enabled        = true
    attribute_name = "ExpirationTime"
  }

  tags = merge(
    local.common_tags,
  )

  server_side_encryption {
    enabled = true
  }

  # lifecycle {
  #   ignore_changes = [
  #     # Ignore changes to tags, e.g. because a management agent
  #     # updates these based on some ruleset managed elsewhere.
  #     tags,
  #   ]
  # }
}
