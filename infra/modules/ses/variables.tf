variable "prefix" {
  description = "Prefix for all resources"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "domain_name" {
  description = "Domain name for SES identity"
  type        = string
}

variable "from_email" {
  description = "Email address to send emails from"
  type        = string
}

variable "create_route53_records" {
  description = "Whether to create Route53 DNS records for domain verification"
  type        = bool
  default     = false
}

variable "route53_zone_id" {
  description = "Route53 zone ID for DNS records (required if create_route53_records is true)"
  type        = string
  default     = ""
}

variable "enable_cloudwatch_events" {
  description = "Enable CloudWatch event destination for SES"
  type        = bool
  default     = true
}

# Email Template Variables
variable "verification_email_subject" {
  description = "Subject for email verification emails"
  type        = string
  default     = "Verifique seu endereço de email"
}

variable "verification_email_html" {
  description = "HTML template for email verification"
  type        = string
  default     = <<-EOT
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Verificação de Email</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #007bff; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; background-color: #f8f9fa; }
            .code { background-color: #e9ecef; padding: 10px; font-size: 24px; font-weight: bold; text-align: center; margin: 20px 0; border-radius: 5px; }
            .footer { text-align: center; padding: 20px; color: #6c757d; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Verificação de Email</h1>
            </div>
            <div class="content">
                <p>Olá!</p>
                <p>Obrigado por se cadastrar em nossa plataforma. Para completar seu cadastro, por favor use o código de verificação abaixo:</p>
                <div class="code">{{verification_code}}</div>
                <p>Este código expira em 24 horas.</p>
                <p>Se você não solicitou esta verificação, pode ignorar este email.</p>
            </div>
            <div class="footer">
                <p>Este é um email automático, por favor não responda.</p>
            </div>
        </div>
    </body>
    </html>
  EOT
}

variable "verification_email_text" {
  description = "Text template for email verification"
  type        = string
  default     = <<-EOT
    Verificação de Email
    
    Olá!
    
    Obrigado por se cadastrar em nossa plataforma. Para completar seu cadastro, por favor use o código de verificação abaixo:
    
    Código: {{verification_code}}
    
    Este código expira em 24 horas.
    
    Se você não solicitou esta verificação, pode ignorar este email.
    
    Este é um email automático, por favor não responda.
  EOT
}

variable "password_reset_subject" {
  description = "Subject for password reset emails"
  type        = string
  default     = "Redefinição de senha"
}

variable "password_reset_html" {
  description = "HTML template for password reset"
  type        = string
  default     = <<-EOT
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Redefinição de Senha</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #dc3545; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; background-color: #f8f9fa; }
            .code { background-color: #e9ecef; padding: 10px; font-size: 24px; font-weight: bold; text-align: center; margin: 20px 0; border-radius: 5px; }
            .footer { text-align: center; padding: 20px; color: #6c757d; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Redefinição de Senha</h1>
            </div>
            <div class="content">
                <p>Olá!</p>
                <p>Você solicitou a redefinição de sua senha. Use o código abaixo para criar uma nova senha:</p>
                <div class="code">{{reset_code}}</div>
                <p>Este código expira em 1 hora.</p>
                <p>Se você não solicitou esta redefinição, pode ignorar este email com segurança.</p>
            </div>
            <div class="footer">
                <p>Este é um email automático, por favor não responda.</p>
            </div>
        </div>
    </body>
    </html>
  EOT
}

variable "password_reset_text" {
  description = "Text template for password reset"
  type        = string
  default     = <<-EOT
    Redefinição de Senha
    
    Olá!
    
    Você solicitou a redefinição de sua senha. Use o código abaixo para criar uma nova senha:
    
    Código: {{reset_code}}
    
    Este código expira em 1 hora.
    
    Se você não solicitou esta redefinição, pode ignorar este email com segurança.
    
    Este é um email automático, por favor não responda.
  EOT
}

variable "welcome_email_subject" {
  description = "Subject for welcome emails"
  type        = string
  default     = "Bem-vindo à nossa plataforma!"
}

variable "welcome_email_html" {
  description = "HTML template for welcome email"
  type        = string
  default     = <<-EOT
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Bem-vindo</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #28a745; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; background-color: #f8f9fa; }
            .footer { text-align: center; padding: 20px; color: #6c757d; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Bem-vindo!</h1>
            </div>
            <div class="content">
                <p>Olá {{username}}!</p>
                <p>Seja bem-vindo à nossa plataforma! Sua conta foi criada com sucesso.</p>
                <p>Agora você pode acessar todos os recursos disponíveis e começar a usar nossa aplicação.</p>
                <p>Se precisar de ajuda, não hesite em entrar em contato conosco.</p>
            </div>
            <div class="footer">
                <p>Este é um email automático, por favor não responda.</p>
            </div>
        </div>
    </body>
    </html>
  EOT
}

variable "welcome_email_text" {
  description = "Text template for welcome email"
  type        = string
  default     = <<-EOT
    Bem-vindo!
    
    Olá {{username}}!
    
    Seja bem-vindo à nossa plataforma! Sua conta foi criada com sucesso.
    
    Agora você pode acessar todos os recursos disponíveis e começar a usar nossa aplicação.
    
    Se precisar de ajuda, não hesite em entrar em contato conosco.
    
    Este é um email automático, por favor não responda.
  EOT
}
