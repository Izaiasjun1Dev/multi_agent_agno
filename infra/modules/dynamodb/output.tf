##########################################################################
#--------------------------- Outputs ------------------------------------#
##########################################################################

output "table_name" {
  description = "Nome da tabela DynamoDB"
  value       = aws_dynamodb_table.main_table.name
}

output "table_arn" {
  description = "ARN da tabela DynamoDB"
  value       = aws_dynamodb_table.main_table.arn
}

output "table_id" {
  description = "ID da tabela DynamoDB"
  value       = aws_dynamodb_table.main_table.id
}

output "table_stream_arn" {
  description = "ARN do stream da tabela DynamoDB (se habilitado)"
  value       = var.stream_enabled ? aws_dynamodb_table.main_table.stream_arn : null
}

output "table_stream_label" {
  description = "Label do stream da tabela DynamoDB (se habilitado)"
  value       = var.stream_enabled ? aws_dynamodb_table.main_table.stream_label : null
}

output "global_secondary_index_names" {
  description = "Lista de nomes dos Global Secondary Indexes"
  value       = [for gsi in var.global_secondary_indexes : gsi.name]
}

output "local_secondary_index_names" {
  description = "Lista de nomes dos Local Secondary Indexes"
  value       = [for lsi in var.local_secondary_indexes : lsi.name]
}

output "table_hash_key" {
  description = "Chave primária da tabela"
  value       = aws_dynamodb_table.main_table.hash_key
}

output "table_range_key" {
  description = "Chave de ordenação da tabela"
  value       = aws_dynamodb_table.main_table.range_key
}

output "billing_mode" {
  description = "Modo de cobrança da tabela"
  value       = aws_dynamodb_table.main_table.billing_mode
}

output "read_capacity" {
  description = "Capacidade de leitura provisionada (se aplicável)"
  value       = var.billing_mode == "PROVISIONED" ? var.read_capacity : null
}

output "write_capacity" {
  description = "Capacidade de escrita provisionada (se aplicável)"
  value       = var.billing_mode == "PROVISIONED" ? var.write_capacity : null
}
