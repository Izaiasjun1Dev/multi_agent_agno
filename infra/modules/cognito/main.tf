# AWS Cognito User Pool
resource "aws_cognito_user_pool" "main" {
  name = "${var.prefix}-${var.environment}-users"

  # Configurações de senha
  password_policy {
    minimum_length    = 8
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
  }

  # Atributos obrigatórios
  schema {
    attribute_data_type = "String"
    name                = "email"
    required            = true
    mutable             = true
  }

  schema {
    attribute_data_type = "String"
    name                = "name"
    required            = true
    mutable             = true
  }

  # Verificação por email
  auto_verified_attributes = ["email"]

  # Configurações de email
  email_configuration {
    email_sending_account = var.use_ses ? "DEVELOPER" : "COGNITO_DEFAULT"
    from_email_address    = var.use_ses ? var.ses_from_email : null
    source_arn            = var.use_ses ? var.ses_domain_arn : null
    configuration_set     = var.use_ses ? var.ses_configuration_set : null
  }

  # Configuração de verificação de email
  verification_message_template {
    default_email_option = "CONFIRM_WITH_CODE"
    email_subject        = var.use_ses ? "Verifique seu endereço de email" : "Confirme sua conta"
    email_message        = var.use_ses ? "Olá! Para completar seu cadastro, use o código de verificação: {####}. Este código expira em 24 horas." : "Seu código de verificação é {####}"
  }

  # Configurações de recuperação de conta
  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  # Configurações de usuário
  user_attribute_update_settings {
    attributes_require_verification_before_update = ["email"]
  }

  tags = {
    Environment = var.environment
    Service     = var.prefix
    ManagedBy   = "Terraform"
  }
}

# Cognito User Pool Client
resource "aws_cognito_user_pool_client" "main" {
  name         = "${var.prefix}-${var.environment}-client"
  user_pool_id = aws_cognito_user_pool.main.id

  # Fluxos de autenticação permitidos
  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_SRP_AUTH"
  ]

  # Configurações de token
  access_token_validity  = 24 # 24 horas
  refresh_token_validity = 30 # 30 dias
  id_token_validity      = 24 # 24 horas

  token_validity_units {
    access_token  = "hours"
    id_token      = "hours"
    refresh_token = "days"
  }

  # OAuth 2.0 (opcional para login social)
  supported_identity_providers = ["COGNITO"]

  # URLs de callback e logout (ajustar conforme necessário)
  callback_urls = var.callback_urls
  logout_urls   = var.logout_urls

  allowed_oauth_flows  = ["code"]
  allowed_oauth_scopes = ["email", "openid", "profile"]

  # Configurações de segurança
  prevent_user_existence_errors = "ENABLED"

  # Configurações de leitura/escrita de atributos
  read_attributes = [
    "email",
    "email_verified",
    "name"
  ]

  write_attributes = [
    "email",
    "name"
  ]
}

# Domain para Hosted UI (opcional)
resource "aws_cognito_user_pool_domain" "main" {
  count        = var.enable_hosted_ui ? 1 : 0
  domain       = "${var.prefix}-${var.environment}-auth"
  user_pool_id = aws_cognito_user_pool.main.id
}
