api_gateway_name = "assistente-private-api"

# Configurações VPC para Produção
vpc_cidr             = "10.2.0.0/16"
availability_zones   = ["us-east-1a", "us-east-1b", "us-east-1c"]
public_subnet_cidrs  = ["10.2.1.0/24", "10.2.2.0/24", "10.2.3.0/24"]
private_subnet_cidrs = ["10.2.11.0/24", "10.2.12.0/24", "10.2.13.0/24"]
enable_nat_gateway   = true
enable_vpc_endpoints = true

# Configurações EKS para Produção
kubernetes_version                   = "1.28"
enabled_cluster_log_types            = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
node_group_desired_size              = 3
node_group_max_size                  = 10
node_group_min_size                  = 2
node_group_instance_types            = ["t3.large"]
cluster_endpoint_private_access      = true
cluster_endpoint_public_access       = false # Mais seguro em produção
cluster_endpoint_public_access_cidrs = []    # Vazio quando público está desabilitado
enable_irsa                          = true
enable_aws_load_balancer_controller  = true
enable_cluster_autoscaler            = true
