
module "ses" {
  source      = "./modules/ses"
  prefix      = var.prefix
  environment = var.environment

  # Configuração de domínio (ajustar conforme seu domínio)
  domain_name = var.ses_domain_name
  from_email  = var.ses_from_email

  # Configuração DNS automática (desabilitada por padrão)
  create_route53_records = var.ses_create_route53_records
  route53_zone_id        = var.ses_route53_zone_id

  # Monitoramento
  enable_cloudwatch_events = var.ses_enable_cloudwatch_events
}

module "cognito" {
  source      = "./modules/cognito"
  prefix      = var.prefix
  environment = var.environment

  use_ses               = false
  ses_from_email        = ""
  ses_domain_arn        = ""
  ses_configuration_set = ""

  callback_urls = [
    "https://app-app.com/callback",
    "http://localhost:3000/callback"
  ]

  logout_urls = [
    "https://app-app.com/logout",
    "http://localhost:3000/logout"
  ]

  enable_hosted_ui = false
}


module "dynamodb_users" {
  source = "./modules/dynamodb"
  table_name  = "${var.prefix}-${var.environment}-users"
  environment = var.environment
  hash_key    = "userId"

  attributes = [
    {
      name = "userId"
      type = "S"
    },
    {
      name = "email"
      type = "S"
    }
  ]

  global_secondary_indexes = [
    {
      name            = "email-index"
      hash_key        = "email"
      range_key       = null
      projection_type = "ALL"
    },
    {
      name            = "userId-index"
      hash_key        = "userId"
      range_key       = null
      projection_type = "ALL"
    }
  ]

  # Configurações usando variáveis
  billing_mode                   = var.dynamodb_billing_mode
  point_in_time_recovery_enabled = var.dynamodb_point_in_time_recovery_enabled
  encryption_enabled             = var.dynamodb_encryption_enabled
  stream_enabled                 = var.dynamodb_stream_enabled
  stream_view_type               = var.dynamodb_stream_view_type
  ttl_enabled                    = var.dynamodb_ttl_enabled
  autoscaling_enabled            = var.dynamodb_autoscaling_enabled
  read_capacity                  = var.dynamodb_read_capacity
  write_capacity                 = var.dynamodb_write_capacity
  autoscaling_read_max_capacity  = var.dynamodb_autoscaling_read_max_capacity
  autoscaling_write_max_capacity = var.dynamodb_autoscaling_write_max_capacity
  autoscaling_read_target_value  = var.dynamodb_autoscaling_read_target_value
  autoscaling_write_target_value = var.dynamodb_autoscaling_write_target_value

  additional_tags = merge(
    var.dynamodb_additional_tags,
    {
      Service = var.prefix
      Purpose = "user-management"
    }
  )
}


module "dynamodb_chats" {
  source = "./modules/dynamodb"
  table_name  = "${var.prefix}-${var.environment}-chats"
  environment = var.environment
  hash_key    = "chatId"

  attributes = [
    {
      name = "chatId"
      type = "S"
    },
    {
      name = "userId"
      type = "S"
    },
  ]

  global_secondary_indexes = [
    {
      name            = "userId-index"
      hash_key        = "userId"
      range_key       = null
      projection_type = "ALL"
    },
    {
      name            = "chatId-index"
      hash_key        = "chatId"
      range_key       = null
      projection_type = "ALL"
    }
  ]

  # Configurações usando variáveis
  billing_mode                   = var.dynamodb_billing_mode
  point_in_time_recovery_enabled = var.dynamodb_point_in_time_recovery_enabled
  encryption_enabled             = var.dynamodb_encryption_enabled
  stream_enabled                 = var.dynamodb_stream_enabled
  stream_view_type               = var.dynamodb_stream_view_type
  ttl_enabled                    = var.dynamodb_ttl_enabled
  autoscaling_enabled            = var.dynamodb_autoscaling_enabled
  read_capacity                  = var.dynamodb_read_capacity
  write_capacity                 = var.dynamodb_write_capacity
  autoscaling_read_max_capacity  = var.dynamodb_autoscaling_read_max_capacity
  autoscaling_write_max_capacity = var.dynamodb_autoscaling_write_max_capacity
  autoscaling_read_target_value  = var.dynamodb_autoscaling_read_target_value
  autoscaling_write_target_value = var.dynamodb_autoscaling_write_target_value

  additional_tags = merge(
    var.dynamodb_additional_tags,
    {
      Service = var.prefix
      Purpose = "chats-management"
    }
  )
}

