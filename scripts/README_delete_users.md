# AWS Cognito User Pool - Script de Deleção

Este script permite deletar todos os usuários de um User Pool do AWS Cognito de forma recursiva e controlada.

## Pré-requisitos

### 1. Instalar dependências

```bash
pip install boto3
```

### 2. Configurar credenciais AWS

```bash
# Opção 1: AWS CLI
aws configure

# Opção 2: Variáveis de ambiente
export AWS_ACCESS_KEY_ID=seu_access_key
export AWS_SECRET_ACCESS_KEY=seu_secret_key
export AWS_DEFAULT_REGION=us-east-1

# Opção 3: IAM Role (EC2, Lambda, etc.)
```

### 3. Permissões IAM necessárias

O usuário/role deve ter as seguintes permissões:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["cognito-idp:ListUsers", "cognito-idp:AdminDeleteUser"],
      "Resource": "arn:aws:cognito-idp:*:*:userpool/*"
    }
  ]
}
```

## Uso

### Sintaxe básica

```bash
python scripts/delete_all_users.py --user-pool-id <USER_POOL_ID> [opções]
```

### Exemplos

#### 1. Simulação (Dry-run) - RECOMENDADO PRIMEIRO

```bash
python scripts/delete_all_users.py --user-pool-id us-east-1_XXXXXXXXX --dry-run
```

#### 2. Deleção real

```bash
python scripts/delete_all_users.py --user-pool-id us-east-1_XXXXXXXXX --region us-east-1
```

#### 3. Deleção sem confirmação (automação)

```bash
python scripts/delete_all_users.py --user-pool-id us-east-1_XXXXXXXXX --force
```

#### 4. Especificar região diferente

```bash
python scripts/delete_all_users.py --user-pool-id eu-west-1_XXXXXXXXX --region eu-west-1
```

## Parâmetros

| Parâmetro        | Obrigatório | Descrição                                            |
| ---------------- | ----------- | ---------------------------------------------------- |
| `--user-pool-id` | Sim         | ID do User Pool do Cognito (ex: us-east-1_XXXXXXXXX) |
| `--region`       | Não         | Região AWS (padrão: us-east-1)                       |
| `--dry-run`      | Não         | Executa simulação sem deletar usuários               |
| `--force`        | Não         | Pula confirmação manual (use com cuidado!)           |

## Recursos de Segurança

### 1. Validação do User Pool ID

- Verifica se o formato está correto antes de executar

### 2. Confirmação manual

- Por padrão, solicita confirmação antes de deletar
- Use `--force` apenas em scripts automatizados

### 3. Modo Dry-run

- Sempre execute com `--dry-run` primeiro
- Mostra quais usuários seriam deletados sem executar a deleção

### 4. Rate limiting

- Implementa pausas entre chamadas para evitar throttling da AWS
- Respeita os limites de API do Cognito

### 5. Tratamento de erros

- Captura e exibe erros específicos do Cognito
- Continua processamento mesmo se algumas deleções falharem

## Exemplo de saída

### Dry-run

```
🚀 AWS Cognito User Pool - Deleção de Usuários
==================================================
📍 User Pool ID: us-east-1_XXXXXXXXX
🌍 Região: us-east-1
🔍 Modo: Simulação (Dry-run)
==================================================
✅ Conectado ao Cognito na região us-east-1
📋 Listando usuários do User Pool...
📄 Encontrados 60 usuários nesta página...
📄 Encontrados 25 usuários nesta página...
📊 Total de usuários encontrados: 85

🔍 SIMULAÇÃO - Processando 85 usuários...
============================================================
[  1/85] user1@example.com (user1@example.com) - Status: CONFIRMED
         🔍 SIMULAÇÃO: Usuário seria deletado
[  2/85] user2@example.com (user2@example.com) - Status: CONFIRMED
         🔍 SIMULAÇÃO: Usuário seria deletado
...
============================================================
🔍 SIMULAÇÃO CONCLUÍDA:
   📊 Total de usuários: 85
   🗑️  Seriam deletados: 85

✅ Processo concluído com sucesso!
```

### Deleção real

```
🚀 AWS Cognito User Pool - Deleção de Usuários
==================================================
📍 User Pool ID: us-east-1_XXXXXXXXX
🌍 Região: us-east-1
🔍 Modo: Deleção Real
==================================================
⚠️  ATENÇÃO: Esta operação irá DELETAR TODOS os usuários do User Pool: us-east-1_XXXXXXXXX
⚠️  Esta ação é IRREVERSÍVEL!

Tem certeza que deseja continuar? (Digite 'DELETAR' para confirmar)
Confirmação: DELETAR
✅ Confirmação recebida. Iniciando deleção...

🗑️  DELEÇÃO - Processando 85 usuários...
============================================================
[  1/85] user1@example.com (user1@example.com) - Status: CONFIRMED
         ✅ Usuário deletado com sucesso
[  2/85] user2@example.com (user2@example.com) - Status: CONFIRMED
         ✅ Usuário deletado com sucesso
...
============================================================
🗑️  DELEÇÃO CONCLUÍDA:
   📊 Total de usuários: 85
   ✅ Deletados com sucesso: 85
   ❌ Falhas: 0

✅ Processo concluído com sucesso!
```

## Limitações

1. **Rate Limiting**: O Cognito tem limites de API. O script implementa pausas, mas em User Pools muito grandes pode ser necessário executar múltiplas vezes.

2. **Paginação**: O script processa até 60 usuários por página (limite do Cognito) com paginação automática.

3. **Permissões**: Usuários com status especiais podem requerer permissões adicionais para deleção.

## Códigos de saída

- `0`: Sucesso
- `1`: Erro (falhas na deleção, credenciais inválidas, etc.)

## Troubleshooting

### Erro: "Credenciais AWS não encontradas"

```bash
aws configure
# ou
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
```

### Erro: "AccessDenied"

Verifique se o usuário/role tem as permissões IAM necessárias listadas acima.

### Erro: "UserPoolNotFound"

Verifique se o User Pool ID está correto e existe na região especificada.

### Erro: "ThrottlingException"

O script já implementa rate limiting, mas para User Pools muito grandes, pode ser necessário aguardar e executar novamente.
