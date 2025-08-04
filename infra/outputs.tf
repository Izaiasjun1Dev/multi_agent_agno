##########################################################################
#--------------------------- Data Sources ------------------------------#
##########################################################################

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

##########################################################################
#--------------------------- Cognito Outputs ----------------------------#
##########################################################################

output "cognito_info" {
  description = "Informações do Cognito"
  value = {
    user_pool_id        = module.cognito.user_pool_id
    user_pool_client_id = module.cognito.user_pool_client_id
    user_pool_arn       = module.cognito.user_pool_arn
    issuer_url          = module.cognito.cognito_issuer_url
  }
}

##########################################################################
#--------------------------- DynamoDB Outputs ---------------------------#
##########################################################################

output "table_user_info" {
  description = "Informações das tabelas DynamoDB"
  value = {
    users_table_name = module.dynamodb_users.table_name
  }
}
