variable "prefix" {
  description = "Prefix for all resources"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "callback_urls" {
  description = "List of callback URLs for OAuth"
  type        = list(string)
  default     = ["http://localhost:3000/callback"]
}

variable "logout_urls" {
  description = "List of logout URLs for OAuth"
  type        = list(string)
  default     = ["http://localhost:3000/logout"]
}

variable "enable_hosted_ui" {
  description = "Enable Cognito Hosted UI"
  type        = bool
  default     = false
}

variable "use_ses" {
  description = "Use SES for sending emails instead of Cognito default"
  type        = bool
  default     = false
}

variable "ses_from_email" {
  description = "Email address to send emails from (when using SES)"
  type        = string
  default     = ""
}

variable "ses_domain_arn" {
  description = "ARN of the SES domain identity (when using SES)"
  type        = string
  default     = ""
}

variable "ses_configuration_set" {
  description = "SES configuration set name (when using SES)"
  type        = string
  default     = ""
}
