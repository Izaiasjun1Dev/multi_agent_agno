# Data source para obter informações da conta
data "aws_caller_identity" "current" {}

# AWS SES Domain Identity
resource "aws_ses_domain_identity" "main" {
  domain = var.domain_name
}

# Verificação DNS do domínio
resource "aws_route53_record" "ses_verification" {
  count   = var.create_route53_records ? 1 : 0
  zone_id = var.route53_zone_id
  name    = "_amazonses.${var.domain_name}"
  type    = "TXT"
  ttl     = "600"
  records = [aws_ses_domain_identity.main.verification_token]
}

# Configuração DKIM
resource "aws_ses_domain_dkim" "main" {
  domain = aws_ses_domain_identity.main.domain
}

# Registros DNS para DKIM
resource "aws_route53_record" "dkim" {
  count   = var.create_route53_records ? 3 : 0
  zone_id = var.route53_zone_id
  name    = "${aws_ses_domain_dkim.main.dkim_tokens[count.index]}._domainkey.${var.domain_name}"
  type    = "CNAME"
  ttl     = "600"
  records = ["${aws_ses_domain_dkim.main.dkim_tokens[count.index]}.dkim.amazonses.com"]
}

# Email Identity para verificação
resource "aws_ses_email_identity" "noreply" {
  email = var.from_email
}

# Política de identidade do SES
resource "aws_ses_identity_policy" "main" {
  identity = aws_ses_domain_identity.main.domain
  name     = "${var.prefix}-${var.environment}-ses-policy"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "cognito-idp.amazonaws.com"
        }
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail"
        ]
        Resource = "arn:aws:ses:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:identity/${var.domain_name}"
        Condition = {
          StringEquals = {
            "ses:FromAddress" = var.from_email
          }
        }
      }
    ]
  })
}

# Configuration Set para tracking
resource "aws_ses_configuration_set" "main" {
  name = "${var.prefix}-${var.environment}-config-set"

  delivery_options {
    tls_policy = "Require"
  }

  reputation_metrics_enabled = true
}

# Event Destination para CloudWatch (opcional)
resource "aws_ses_event_destination" "cloudwatch" {
  count                  = var.enable_cloudwatch_events ? 1 : 0
  name                   = "${var.prefix}-${var.environment}-cloudwatch"
  configuration_set_name = aws_ses_configuration_set.main.name
  enabled                = true
  matching_types = [
    "send",
    "reject",
    "bounce",
    "complaint",
    "delivery"
  ]

  cloudwatch_destination {
    default_value  = "default"
    dimension_name = "MessageTag"
    value_source   = "messageTag"
  }
}

# Template para emails de verificação
resource "aws_ses_template" "verification_email" {
  name    = "${var.prefix}-${var.environment}-verification-template"
  subject = var.verification_email_subject
  html    = var.verification_email_html
  text    = var.verification_email_text
}

# Template para emails de redefinição de senha
resource "aws_ses_template" "password_reset" {
  name    = "${var.prefix}-${var.environment}-password-reset-template"
  subject = var.password_reset_subject
  html    = var.password_reset_html
  text    = var.password_reset_text
}

# Template para emails de boas-vindas
resource "aws_ses_template" "welcome_email" {
  name    = "${var.prefix}-${var.environment}-welcome-template"
  subject = var.welcome_email_subject
  html    = var.welcome_email_html
  text    = var.welcome_email_text
}

# IAM Role para o Cognito usar o SES
resource "aws_iam_role" "cognito_ses_role" {
  name = "${var.prefix}-${var.environment}-cognito-ses-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "cognito-idp.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Environment = var.environment
    Service     = var.prefix
    ManagedBy   = "Terraform"
  }
}

# Policy para o Cognito enviar emails via SES
resource "aws_iam_role_policy" "cognito_ses_policy" {
  name = "${var.prefix}-${var.environment}-cognito-ses-policy"
  role = aws_iam_role.cognito_ses_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail"
        ]
        Resource = "arn:aws:ses:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:identity/${var.domain_name}"
        Condition = {
          StringEquals = {
            "ses:FromAddress" = var.from_email
          }
        }
      }
    ]
  })
}

# Verificação do domínio (aguardar verificação)
resource "aws_ses_domain_identity_verification" "main" {
  count      = var.create_route53_records ? 1 : 0
  domain     = aws_ses_domain_identity.main.id
  depends_on = [aws_route53_record.ses_verification]

  timeouts {
    create = "10m"
  }
}
