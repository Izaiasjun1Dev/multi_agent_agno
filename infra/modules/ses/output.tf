output "domain_identity_arn" {
  description = "ARN of the SES domain identity"
  value       = aws_ses_domain_identity.main.arn
}

output "domain_verification_token" {
  description = "Domain verification token for DNS record"
  value       = aws_ses_domain_identity.main.verification_token
}

output "dkim_tokens" {
  description = "DKIM tokens for DNS records"
  value       = aws_ses_domain_dkim.main.dkim_tokens
}

output "configuration_set_name" {
  description = "Name of the SES configuration set"
  value       = aws_ses_configuration_set.main.name
}

output "configuration_set_arn" {
  description = "ARN of the SES configuration set"
  value       = aws_ses_configuration_set.main.arn
}

output "email_identity_arn" {
  description = "ARN of the SES email identity"
  value       = aws_ses_email_identity.noreply.arn
}

output "cognito_ses_role_arn" {
  description = "ARN of the IAM role for Cognito to use SES"
  value       = aws_iam_role.cognito_ses_role.arn
}

output "from_email" {
  description = "Email address configured for sending"
  value       = var.from_email
}

output "verification_template_name" {
  description = "Name of the verification email template"
  value       = aws_ses_template.verification_email.name
}

output "password_reset_template_name" {
  description = "Name of the password reset email template"
  value       = aws_ses_template.password_reset.name
}

output "welcome_template_name" {
  description = "Name of the welcome email template"
  value       = aws_ses_template.welcome_email.name
}

output "domain_name" {
  description = "Domain name configured for SES"
  value       = var.domain_name
}

output "ses_smtp_username" {
  description = "SMTP username for SES (if using SMTP)"
  value       = "Generated after SES setup - check AWS Console"
}

output "ses_region" {
  description = "AWS region where SES is configured"
  value       = data.aws_region.current.name
}

# Data source for current region
data "aws_region" "current" {}
