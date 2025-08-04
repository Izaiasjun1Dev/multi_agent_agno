##########################################################################
#--------------------------- Variables ----------------------------------#
##########################################################################

variable "table_name" {
  description = "Nome da tabela DynamoDB"
  type        = string
}

variable "environment" {
  description = "Ambiente (dev, staging, prod)"
  type        = string
}

variable "billing_mode" {
  description = "Modo de cobrança da tabela (PAY_PER_REQUEST ou PROVISIONED)"
  type        = string
  default     = "PAY_PER_REQUEST"

  validation {
    condition     = contains(["PAY_PER_REQUEST", "PROVISIONED"], var.billing_mode)
    error_message = "billing_mode deve ser PAY_PER_REQUEST ou PROVISIONED."
  }
}

variable "hash_key" {
  description = "Chave primária (partition key) da tabela"
  type        = string
}

variable "range_key" {
  description = "Chave de ordenação (sort key) da tabela"
  type        = string
  default     = null
}

variable "attributes" {
  description = "Lista de atributos da tabela"
  type = list(object({
    name = string
    type = string
  }))
}

variable "read_capacity" {
  description = "Capacidade de leitura provisionada (apenas para PROVISIONED mode)"
  type        = number
  default     = 5
}

variable "write_capacity" {
  description = "Capacidade de escrita provisionada (apenas para PROVISIONED mode)"
  type        = number
  default     = 5
}

variable "global_secondary_indexes" {
  description = "Lista de Global Secondary Indexes"
  type = list(object({
    name            = string
    hash_key        = string
    range_key       = optional(string)
    projection_type = string
    read_capacity   = optional(number, 5)
    write_capacity  = optional(number, 5)
  }))
  default = []
}

variable "local_secondary_indexes" {
  description = "Lista de Local Secondary Indexes"
  type = list(object({
    name            = string
    range_key       = string
    projection_type = string
  }))
  default = []
}

variable "ttl_enabled" {
  description = "Habilitar TTL (Time To Live)"
  type        = bool
  default     = false
}

variable "ttl_attribute_name" {
  description = "Nome do atributo para TTL"
  type        = string
  default     = ""
}

variable "encryption_enabled" {
  description = "Habilitar criptografia server-side"
  type        = bool
  default     = true
}

variable "kms_key_id" {
  description = "ID da chave KMS para criptografia (opcional)"
  type        = string
  default     = null
}

variable "point_in_time_recovery_enabled" {
  description = "Habilitar Point-in-Time Recovery"
  type        = bool
  default     = true
}

variable "stream_enabled" {
  description = "Habilitar DynamoDB Streams"
  type        = bool
  default     = false
}

variable "stream_view_type" {
  description = "Tipo de visualização do stream (KEYS_ONLY, NEW_IMAGE, OLD_IMAGE, NEW_AND_OLD_IMAGES)"
  type        = string
  default     = "NEW_AND_OLD_IMAGES"

  validation {
    condition     = contains(["KEYS_ONLY", "NEW_IMAGE", "OLD_IMAGE", "NEW_AND_OLD_IMAGES"], var.stream_view_type)
    error_message = "stream_view_type deve ser um dos valores válidos."
  }
}

variable "autoscaling_enabled" {
  description = "Habilitar autoscaling para modo PROVISIONED"
  type        = bool
  default     = false
}

variable "autoscaling_read_max_capacity" {
  description = "Capacidade máxima de leitura para autoscaling"
  type        = number
  default     = 100
}

variable "autoscaling_write_max_capacity" {
  description = "Capacidade máxima de escrita para autoscaling"
  type        = number
  default     = 100
}

variable "autoscaling_read_target_value" {
  description = "Valor alvo de utilização para leitura (em %)"
  type        = number
  default     = 70
}

variable "autoscaling_write_target_value" {
  description = "Valor alvo de utilização para escrita (em %)"
  type        = number
  default     = 70
}

variable "additional_tags" {
  description = "Tags adicionais para aplicar aos recursos"
  type        = map(string)
  default     = {}
}
