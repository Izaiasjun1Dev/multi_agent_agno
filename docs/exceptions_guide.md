# Guia de Exceções - Inner API

Este documento descreve o sistema de exceções customizadas da Inner API e como utilizá-las corretamente.

## Visão Geral

O sistema de exceções foi projetado para fornecer mensagens de erro consistentes, informativas e localizadas (PT/EN) para todos os endpoints da API.

## Estrutura das Exceções

### Exceção Base

Todas as exceções customizadas herdam de `BaseApplicationException`:

```python
from core.exceptions import BaseApplicationException

class BaseApplicationException(Exception):
    def __init__(
        self,
        message_pt: str,
        message_en: str,
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None,
        status_code: int = 500,
    ):
        # ...
```

### Resposta de Erro Padrão

Todas as exceções retornam uma resposta JSON no formato:

```json
{
  "error": true,
  "message": "Mensagem de erro localizada",
  "error_code": "CODIGO_DO_ERRO",
  "status_code": 400,
  "details": {
    "campo": "valor",
    "informacao_adicional": "..."
  }
}
```

## Categorias de Exceções

### 1. Exceções de Validação

Para erros de validação de dados:

```python
from core.exceptions import ValidationException

raise ValidationException(
    message_pt="Email inválido",
    message_en="Invalid email",
    field="email",
    value="invalid-email",
    error_code="INVALID_EMAIL"
)
```

### 2. Exceções de Negócio

Para violações de regras de negócio:

```python
from core.exceptions import BusinessRuleException

raise BusinessRuleException(
    message_pt="Limite de crédito excedido",
    message_en="Credit limit exceeded",
    rule="credit_limit",
    error_code="CREDIT_LIMIT_EXCEEDED"
)
```

### 3. Exceções de Recursos

#### Não Encontrado (404)

```python
from core.exceptions import NotFoundException

raise NotFoundException(
    message_pt="Usuário não encontrado",
    message_en="User not found",
    resource="user",
    identifier=user_id,
    error_code="USER_NOT_FOUND"
)
```

#### Conflito (409)

```python
from core.exceptions import ConflictException

raise ConflictException(
    message_pt="Email já cadastrado",
    message_en="Email already registered",
    conflicting_field="email",
    conflicting_value=email,
    error_code="EMAIL_CONFLICT"
)
```

### 4. Exceções de Autenticação/Autorização

#### Não Autorizado (401)

```python
from core.exceptions import UnauthorizedException

raise UnauthorizedException(
    message_pt="Token inválido",
    message_en="Invalid token",
    error_code="INVALID_TOKEN"
)
```

#### Acesso Proibido (403)

```python
from core.exceptions import ForbiddenException

raise ForbiddenException(
    message_pt="Sem permissão para acessar este recurso",
    message_en="No permission to access this resource",
    permission="admin",
    resource="users",
    error_code="INSUFFICIENT_PERMISSIONS"
)
```

### 5. Exceções de Infraestrutura

#### Erro de Banco de Dados

```python
from core.exceptions import DatabaseException

raise DatabaseException(
    message_pt="Erro ao salvar dados",
    message_en="Error saving data",
    operation="insert",
    table="users",
    error_code="DB_SAVE_ERROR"
)
```

#### Timeout

```python
from core.exceptions import TimeoutException

raise TimeoutException(
    service="payment_gateway",
    operation="process_payment",
    timeout_seconds=30,
    error_code="PAYMENT_TIMEOUT"
)
```

#### Serviço Externo

```python
from core.exceptions import ExternalServiceException

raise ExternalServiceException(
    service="email_service",
    message_pt="Erro ao enviar email",
    message_en="Error sending email",
    status_code=503,
    error_code="EMAIL_SERVICE_ERROR"
)
```

### 6. Exceções de Requisição

#### Rate Limit (429)

```python
from core.exceptions import RateLimitException

raise RateLimitException(
    limit=100,
    period="hour",
    retry_after=3600,
    error_code="RATE_LIMIT_EXCEEDED"
)
```

#### Payload Muito Grande (413)

```python
from core.exceptions import PayloadTooLargeException

raise PayloadTooLargeException(
    max_size="10MB",
    actual_size="15MB",
    error_code="PAYLOAD_TOO_LARGE"
)
```

## Exceções Específicas de Domínio

### Exceções de Usuário

```python
from core.exceptions.user.exceptions import (
    UserAlreadyExistsException,
    UserEmailValidationException,
    UserPasswordValidationException,
)

# Usuário já existe
raise UserAlreadyExistsException(email="user@example.com")

# Email inválido
raise UserEmailValidationException(email="invalid-email")

# Senha fraca
raise UserPasswordValidationException(
    reason_pt="Senha deve ter pelo menos 8 caracteres",
    reason_en="Password must be at least 8 characters long"
)
```

## Boas Práticas

### 1. Use Exceções Específicas

❌ Não faça:

```python
raise Exception("Erro genérico")
raise HTTPException(status_code=400, detail="Erro")
```

✅ Faça:

```python
raise ValidationException(
    message_pt="Campo obrigatório",
    message_en="Required field",
    field="name",
    error_code="REQUIRED_FIELD"
)
```

### 2. Forneça Contexto Adequado

```python
raise NotFoundException(
    message_pt=f"Pedido #{order_id} não encontrado",
    message_en=f"Order #{order_id} not found",
    resource="order",
    identifier=order_id,
    details={
        "searched_in": "active_orders",
        "user_id": user_id
    },
    error_code="ORDER_NOT_FOUND"
)
```

### 3. Use Códigos de Erro Consistentes

- Use UPPER_SNAKE_CASE
- Seja específico: `USER_EMAIL_ALREADY_EXISTS` ao invés de `ERROR`
- Mantenha um padrão: `RESOURCE_ACTION_REASON`

### 4. Tratamento em Camadas

```python
# Use Case
try:
    user = self.repository.find_by_id(user_id)
    if not user:
        raise NotFoundException(
            message_pt="Usuário não encontrado",
            message_en="User not found",
            resource="user",
            identifier=user_id
        )
except DatabaseException:
    # Re-raise exceções de infraestrutura
    raise
except Exception as e:
    # Wrap exceções inesperadas
    raise InfrastructureException(
        message_pt="Erro ao buscar usuário",
        message_en="Error fetching user",
        service="user_service",
        operation="find_by_id"
    )
```

## Localização

O sistema suporta mensagens em PT-BR e EN-US. O idioma é determinado pelo header `Accept-Language`:

```bash
# Português
curl -H "Accept-Language: pt-BR" http://api/users/123

# Inglês
curl -H "Accept-Language: en-US" http://api/users/123
```

## Middlewares

### Request ID

Todas as requisições recebem um ID único para rastreamento:

```json
{
  "error": true,
  "message": "Erro",
  "details": {
    "request_context": {
      "request_id": "123e4567-e89b-12d3-a456-426614174000"
    }
  }
}
```

### Logging

Todas as exceções são automaticamente logadas com contexto completo.

## Testando Exceções

```python
import pytest
from core.exceptions import ValidationException

def test_user_creation_with_invalid_email():
    with pytest.raises(ValidationException) as exc_info:
        create_user(email="invalid")

    assert exc_info.value.error_code == "INVALID_EMAIL"
    assert exc_info.value.status_code == 400
    assert exc_info.value.details["field"] == "email"
```

## Referência Rápida

| Exceção                   | Status Code | Uso                            |
| ------------------------- | ----------- | ------------------------------ |
| ValidationException       | 400         | Dados de entrada inválidos     |
| BadRequestException       | 400         | Requisição mal formada         |
| UnauthorizedException     | 401         | Autenticação necessária        |
| ForbiddenException        | 403         | Sem permissão                  |
| NotFoundException         | 404         | Recurso não encontrado         |
| MethodNotAllowedException | 405         | Método HTTP não permitido      |
| ConflictException         | 409         | Conflito de recursos           |
| PayloadTooLargeException  | 413         | Payload muito grande           |
| BusinessRuleException     | 422         | Violação de regra de negócio   |
| RateLimitException        | 429         | Limite de requisições excedido |
| InfrastructureException   | 503         | Erro de infraestrutura         |
| DatabaseException         | 503         | Erro de banco de dados         |
| TimeoutException          | 504         | Timeout                        |

## Conclusão

O sistema de exceções fornece uma maneira consistente e robusta de lidar com erros em toda a aplicação. Ao seguir estas diretrizes, você garante que os usuários da API recebam mensagens de erro claras e informativas.
