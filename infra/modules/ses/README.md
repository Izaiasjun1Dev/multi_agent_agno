# Módulo SES - Simple Email Service

Este módulo Terraform configura o Amazon SES (Simple Email Service) para envio de emails de verificação e notificações através do Amazon Cognito.

## Funcionalidades

- ✅ Configuração completa do SES com domínio personalizado
- ✅ Verificação de domínio automática (opcional com Route53)
- ✅ Configuração DKIM para autenticação de email
- ✅ Templates de email personalizáveis (HTML e texto)
- ✅ Integração com Amazon Cognito
- ✅ IAM roles e policies para segurança
- ✅ Configuration Set para tracking e métricas
- ✅ Suporte a CloudWatch Events

## Uso Básico

```hcl
module "ses" {
  source = "./modules/ses"

  prefix      = "myapp"
  environment = "dev"
  domain_name = "myapp.com"
  from_email  = "noreply@myapp.com"

  # Configuração DNS automática (opcional)
  create_route53_records = true
  route53_zone_id       = "Z123456789"

  # Monitoramento
  enable_cloudwatch_events = true
}
```

## Integração com Cognito

Para usar este módulo com o Cognito, você precisa:

1. Configurar o SES primeiro
2. Atualizar o Cognito para usar o SES

```hcl
# No módulo Cognito
resource "aws_cognito_user_pool" "main" {
  # ... outras configurações ...

  email_configuration {
    email_sending_account  = "DEVELOPER"
    from_email_address    = module.ses.from_email
    source_arn           = module.ses.domain_identity_arn
  }
}
```

## Variáveis

| Nome                       | Descrição                                                         | Tipo     | Padrão  | Obrigatório |
| -------------------------- | ----------------------------------------------------------------- | -------- | ------- | ----------- |
| `prefix`                   | Prefixo para todos os recursos                                    | `string` | -       | ✅          |
| `environment`              | Nome do ambiente (dev, staging, prod)                             | `string` | -       | ✅          |
| `domain_name`              | Nome do domínio para identidade SES                               | `string` | -       | ✅          |
| `from_email`               | Endereço de email para envio                                      | `string` | -       | ✅          |
| `create_route53_records`   | Criar registros DNS no Route53 automaticamente                    | `bool`   | `false` | ❌          |
| `route53_zone_id`          | ID da zona Route53 (obrigatório se create_route53_records = true) | `string` | `""`    | ❌          |
| `enable_cloudwatch_events` | Habilitar eventos CloudWatch para SES                             | `bool`   | `true`  | ❌          |

## Outputs

| Nome                         | Descrição                                |
| ---------------------------- | ---------------------------------------- |
| `domain_identity_arn`        | ARN da identidade de domínio SES         |
| `cognito_ses_role_arn`       | ARN da role IAM para Cognito usar SES    |
| `configuration_set_name`     | Nome do configuration set SES            |
| `from_email`                 | Endereço de email configurado para envio |
| `verification_template_name` | Nome do template de verificação de email |

## Configuração DNS Manual

Se você não usar o Route53 (`create_route53_records = false`), precisará criar os seguintes registros DNS manualmente:

### Verificação de Domínio

```
Tipo: TXT
Nome: _amazonses.seudominio.com
Valor: [verification_token do output]
```

### DKIM (3 registros)

```
Tipo: CNAME
Nome: [dkim_token_1]._domainkey.seudominio.com
Valor: [dkim_token_1].dkim.amazonses.com

Tipo: CNAME
Nome: [dkim_token_2]._domainkey.seudominio.com
Valor: [dkim_token_2].dkim.amazonses.com

Tipo: CNAME
Nome: [dkim_token_3]._domainkey.seudominio.com
Valor: [dkim_token_3].dkim.amazonses.com
```

## Templates de Email

O módulo inclui três templates pré-configurados:

1. **Verificação de Email**: Para novos usuários confirmarem seu email
2. **Redefinição de Senha**: Para usuários que esqueceram a senha
3. **Bem-vindo**: Email de boas-vindas após verificação

Todos os templates são responsivos e incluem versões HTML e texto.

## Segurança

- IAM roles com princípio de menor privilégio
- Políticas específicas para Cognito
- Configuração TLS obrigatória
- Validação de endereço de origem

## Monitoramento

O módulo configura automaticamente:

- CloudWatch metrics para SES
- Event destinations para tracking
- Reputation metrics

## Limitações

- SES inicia em sandbox mode (50 emails/dia)
- Para produção, solicite remoção do sandbox
- Verificação de domínio pode levar até 72 horas
- DKIM requer configuração DNS adequada

## Próximos Passos

Após aplicar o módulo:

1. Verifique se os registros DNS foram criados corretamente
2. Aguarde a verificação do domínio (pode levar até 72h)
3. Se necessário, solicite remoção do sandbox mode
4. Configure o Cognito para usar o SES
5. Teste o envio de emails
