prefix        = "inner"
environment   = "dev"
force_rebuild = true

# DynamoDB specific configurations
dynamodb_billing_mode                   = "PAY_PER_REQUEST"
dynamodb_point_in_time_recovery_enabled = true
dynamodb_encryption_enabled             = true
dynamodb_stream_enabled                 = false
dynamodb_stream_view_type               = "NEW_AND_OLD_IMAGES"
dynamodb_ttl_enabled                    = false
dynamodb_autoscaling_enabled            = false

# DynamoDB capacity settings (only for PROVISIONED mode)
dynamodb_read_capacity                  = 5
dynamodb_write_capacity                 = 5
dynamodb_autoscaling_read_max_capacity  = 100
dynamodb_autoscaling_write_max_capacity = 100
dynamodb_autoscaling_read_target_value  = 70
dynamodb_autoscaling_write_target_value = 70

# Additional tags for DynamoDB resources
dynamodb_additional_tags = {
  Environment = "development"
  Project     = "inner"
  Owner       = "development-team"
  CostCenter  = "engineering"
  Backup      = "daily"
}
