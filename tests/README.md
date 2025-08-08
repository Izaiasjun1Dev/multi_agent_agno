# Testes do Projeto Inner

Este diretório contém os testes automatizados para o projeto Inner, uma aplicação de agentes IA.

## Estrutura de Testes

### ✅ Implementados

#### `tests/core/entities/agent/`

- **test_agent_entities.py**: Testes completos para todas as entidades de agente
  - `TestAgentConfig`: Configurações de agente
  - `TestBaseAgent`: Agente base e funcionalidades básicas
  - `TestComplexityAgent`: Agente para tarefas complexas
  - `TestJudgingBaseAgent`: Agente de análise de intenções
  - `TestGeneratorImageAgent`: Agente gerador de imagens (DALL-E)
  - `TestTeamAgent`: Agente de equipe para coordenação

#### `tests/core/usecases/agent/`

- **test_agent_usecases.py**: Testes para casos de uso de agentes
  - `TestCreateAgentUseCase`: Criação de agentes
  - `TestStreamAgentResponseUseCase`: Stream de respostas

### 🔄 Em Progresso / Planejados

- Tests para repositórios (`tests/infraestructure/repositories/`)
- Tests para controllers (`tests/presentation/controllers/`)
- Tests para exceções (`tests/core/exceptions/`)
- Tests de integração
- Tests de DTOs
- Tests para middlewares

## Como Executar

### Método 1: Script Automatizado

```bash
./scripts/run_tests.sh
```

### Método 2: Comando Direct

```bash
# Configurar PYTHONPATH
export PYTHONPATH="/home/izaias/projetos/inner/src"

# Executar testes específicos
/home/izaias/projetos/inner/.venv/bin/python -m pytest tests/core/entities/agent/ -v

# Executar com coverage
/home/izaias/projetos/inner/.venv/bin/python -m pytest tests/core/entities/agent/ -v --cov=src --cov-report=term-missing
```

## Resultados dos Testes

### Última Execução ✅

- **15/15 testes passando** nos testes de entidades de agente
- **100% de cobertura** nas entidades testadas
- **Todos os tipos de agente cobertos**: BaseAgent, ComplexityAgent, JudgingBaseAgent, GeneratorImageAgent, TeamAgent

### Cobertura de Código

- Entidades de agente: **100%**
- Casos de uso de agente: **Parcial** (em desenvolvimento)
- Repositórios: **0%** (não implementado)
- Controllers: **0%** (não implementado)

## Dependências de Teste

- `pytest`: Framework de testes principal
- `pytest-asyncio`: Suporte para testes assíncronos
- `pytest-cov`: Cobertura de código
- `unittest.mock`: Mocking para isolamento de testes
- `agno`: Biblioteca de agentes IA

## Configuração do Ambiente

Os testes requerem:

1. **Python 3.11+**
2. **Ambiente virtual ativo** (`.venv`)
3. **PYTHONPATH configurado** para `src/`
4. **Dependências instaladas** (`requirements-dev.txt`)

## Padrões e Convenções

### Nomenclatura

- Arquivos de teste: `test_*.py`
- Classes de teste: `TestClassName`
- Métodos de teste: `test_method_name`

### Estrutura de Teste

```python
def test_method_name(self):
    """Descrição clara do que está sendo testado"""
    # Arrange - Configurar dados de teste

    # Act - Executar a funcionalidade

    # Assert - Verificar resultados
```

### Cobertura Mínima

- **Entidades**: 100% dos métodos públicos
- **Casos de uso**: 90% incluindo cenários de erro
- **Repositories**: 85% com mocking de banco de dados
- **Controllers**: 80% com mocking de dependências

## Troubleshooting

### Erro de ImportError

```
ModuleNotFoundError: No module named 'src'
```

**Solução**: Verificar se PYTHONPATH está configurado corretamente:

```bash
export PYTHONPATH="/home/izaias/projetos/inner/src"
```

### Erro de Dependências

```
ModuleNotFoundError: No module named 'agno'
```

**Solução**: Instalar dependências:

```bash
pip install -r requirements-dev.txt
```

### Testes Assíncronos

Para testes que envolvem `async/await`, usar o decorator:

```python
@pytest.mark.asyncio
async def test_async_method(self):
    result = await some_async_function()
    assert result is not None
```

## Contribuindo

1. **Adicionar novos testes**: Seguir a estrutura existente
2. **Manter cobertura**: Garantir que novos códigos tenham testes
3. **Documentar**: Adicionar docstrings descritivos nos testes
4. **Executar antes de commit**: Rodar `./scripts/run_tests.sh`

## Status do Projeto

| Componente         | Testes | Status      |
| ------------------ | ------ | ----------- |
| Entidades Agent    | 15     | ✅ 100%     |
| Casos de Uso Agent | 9      | 🔄 Parcial  |
| Repositórios       | 0      | ❌ Pendente |
| Controllers        | 0      | ❌ Pendente |
| Exceções           | 0      | ❌ Pendente |
| DTOs               | 0      | ❌ Pendente |

**Última atualização**: 2025-08-07
