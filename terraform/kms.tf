data "aws_iam_policy_document" "kms_sns" {
  statement {
    sid    = "Enable IAM User Permissions"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"]
    }

    actions   = ["kms:*"]
    resources = ["*"]
  }

  statement {
    sid    = "Enable S3 Notifications"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["s3.amazonaws.com"]
    }

    actions = [
      "kms:GenerateDataKey",
      "kms:Decrypt",
    ]

    resources = ["*"]
  }

  statement {
    sid    = "Enable Lambda Notifications"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = [
      "kms:GenerateDataKey",
      "kms:Decrypt",
    ]

    resources = ["*"]
  }
}

resource "aws_kms_key" "sns" {
  description             = "KMS key for SNS"
  key_usage               = "ENCRYPT_DECRYPT"
  deletion_window_in_days = 20
  is_enabled              = true
  enable_key_rotation     = true

  policy = data.aws_iam_policy_document.kms_sns.json

  tags = merge(
        local.common_tags,
        map(
            "Name", "kms-sns"
        )
    )
}

resource "aws_kms_alias" "sns" {
  name          = "alias/kms-sns"
  target_key_id = aws_kms_key.sns.key_id
}

