variable "environment" {
  type        = string
  description = "Sigla do ambiente (dev, qa, prod) para uso nos recursos, setado via variável de ambiente do pipeline (não informar no tfvar)"
}

variable "prefix" {
  type        = string
  description = "Prefixo para os recursos"
}


variable "environment_variables" {
  type    = list(map(string))
  default = []
}

variable "docker_file_name" {
  description = "O nome do Dockerfile"
  type        = list(string)
  default     = ["Dockerfile"]
}


# DynamoDB Configuration Variables
variable "dynamodb_billing_mode" {
  description = "Modo de cobrança da tabela DynamoDB (PAY_PER_REQUEST ou PROVISIONED)"
  type        = string
  default     = "PAY_PER_REQUEST"
}

variable "dynamodb_point_in_time_recovery_enabled" {
  description = "Habilitar Point-in-Time Recovery para DynamoDB"
  type        = bool
  default     = true
}

variable "dynamodb_encryption_enabled" {
  description = "Habilitar criptografia server-side para DynamoDB"
  type        = bool
  default     = true
}

variable "dynamodb_stream_enabled" {
  description = "Habilitar DynamoDB Streams"
  type        = bool
  default     = false
}

variable "dynamodb_stream_view_type" {
  description = "Tipo de visualização do stream DynamoDB"
  type        = string
  default     = "NEW_AND_OLD_IMAGES"
}

variable "dynamodb_ttl_enabled" {
  description = "Habilitar TTL (Time To Live) para DynamoDB"
  type        = bool
  default     = false
}

variable "dynamodb_autoscaling_enabled" {
  description = "Habilitar autoscaling para DynamoDB em modo PROVISIONED"
  type        = bool
  default     = false
}

variable "dynamodb_read_capacity" {
  description = "Capacidade de leitura provisionada para DynamoDB"
  type        = number
  default     = 5
}

variable "dynamodb_write_capacity" {
  description = "Capacidade de escrita provisionada para DynamoDB"
  type        = number
  default     = 5
}

variable "dynamodb_autoscaling_read_max_capacity" {
  description = "Capacidade máxima de leitura para autoscaling do DynamoDB"
  type        = number
  default     = 100
}

variable "dynamodb_autoscaling_write_max_capacity" {
  description = "Capacidade máxima de escrita para autoscaling do DynamoDB"
  type        = number
  default     = 100
}

variable "dynamodb_autoscaling_read_target_value" {
  description = "Valor alvo de utilização para leitura do DynamoDB (em %)"
  type        = number
  default     = 70
}

variable "dynamodb_autoscaling_write_target_value" {
  description = "Valor alvo de utilização para escrita do DynamoDB (em %)"
  type        = number
  default     = 70
}

variable "dynamodb_additional_tags" {
  description = "Tags adicionais para recursos DynamoDB"
  type        = map(string)
  default     = {}
}

variable "build_id" {
  description = "build_id para o ecr da lambda de criação de usuário"
  type        = string
  default     = null
}

variable "force_rebuild" {
  description = "Forçar rebuild das imagens Docker"
  type        = bool
  default     = false
}


variable "ses_domain_name" {
  description = "Nome do domínio para configuração do SES"
  type        = string
  default     = "example.com"
}

variable "ses_from_email" {
  description = "Endereço de email para envio via SES"
  type        = string
  default     = "noreply@example.com"
}

variable "ses_create_route53_records" {
  description = "Criar registros DNS no Route53 automaticamente para verificação do domínio"
  type        = bool
  default     = false
}

variable "ses_route53_zone_id" {
  description = "ID da zona Route53 para criação de registros DNS (obrigatório se ses_create_route53_records = true)"
  type        = string
  default     = ""
}

variable "ses_enable_cloudwatch_events" {
  description = "Habilitar eventos CloudWatch para monitoramento do SES"
  type        = bool
  default     = true
}
