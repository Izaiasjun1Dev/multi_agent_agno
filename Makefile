# Makefile para o projeto Inner

# Variáveis
PYTHON = .venv/bin/python
PIP = .venv/bin/pip
PYTEST = $(PYTHON) -m pytest
PYTHONPATH = src

# Comandos de configuração
.PHONY: install
install:
	$(PIP) install -r requirements.txt

.PHONY: install-dev
install-dev: install
	$(PIP) install pytest pytest-asyncio pytest-cov pytest-mock faker email-validator

# Comandos de teste
.PHONY: test
test:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/ -v

.PHONY: test-coverage
test-coverage:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/ -v --cov=src --cov-report=term-missing --cov-report=html

.PHONY: test-unit
test-unit:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/core/ -v

.PHONY: test-usecases
test-usecases:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/core/usecases/ -v

.PHONY: test-entities
test-entities:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/core/entities/ -v

.PHONY: test-exceptions
test-exceptions:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/core/exceptions/ -v

.PHONY: test-watch
test-watch:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) tests/ -v --watch

# Comandos de linting e formatação
.PHONY: lint
lint:
	$(PYTHON) -m flake8 src/ tests/

.PHONY: format
format:
	$(PYTHON) -m black src/ tests/
	$(PYTHON) -m isort src/ tests/

# Comandos de migração do banco de dados
.PHONY: migrate-create migrate-upgrade migrate-status migrate-agent
migrate-create:
	@echo "🔄 Criando nova migração..."
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m alembic -c alembic.ini revision --autogenerate -m "$(MESSAGE)"
	@echo "✅ Migração criada com sucesso!"

migrate-upgrade:
	@echo "🔄 Aplicando migrações pendentes..."
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m alembic -c alembic.ini upgrade head
	@echo "✅ Migrações aplicadas com sucesso!"

migrate-status:
	@echo "📊 Status das migrações:"
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m alembic -c alembic.ini current
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m alembic -c alembic.ini history


# Comandos de execução da aplicação
.PHONY: run run-dev run-prod
run: run-dev

run-dev:
	@echo "🚀 Iniciando Inner API em modo desenvolvimento..."
	@echo "📍 URL: http://localhost:8000"
	@echo "📚 Documentação: http://localhost:8000/docs"
	@echo ""
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) src/application/main.py

run-prod:
	@echo "🚀 Iniciando Inner API em modo produção..."
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m uvicorn presentation.app:app --host 0.0.0.0 --port 8000

# Comandos de limpeza
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/

.PHONY: clean-all
clean-all: clean
	rm -rf .venv/


.PHONY: delete-users
delete-users:
	@./scripts/delete_all_users.py --user-pool-id us-east-1_JIEznH51N

.PHONY: delete-users-dry-run
delete-users-dry-run:
	@./scripts/delete_all_users.py --user-pool-id us-east-1_JIEznH51N --dry-run


.PHONY: infra-apply
infra-apply:
	@echo "🚀 Aplicando infraestrutura..."
	@cd infra && clear && terraform init && terraform apply -var-file=tfvars/dev.tfvars -auto-approve -parallelism=10
	@echo "✅ Infraestrutura aplicada com sucesso!"
	@cd ..

.PHONY: run-environment
run-environment:
	@echo "🚀 Iniciando Inner API em modo desenvolvimento..."
	@docker compose -f docker/docker-compose.yaml up -d
	@clear && PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m presentation.playground &
	@cd agent-ui && npm run dev
	@echo "📍 URL: http://localhost:3000"

.PHONY: playground
playground:
	@echo "🚀 Iniciando Playground..."
	@clear && PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m presentation.playground &
	@cd agent-ui && npm run dev
	@echo "📍 URL: http://localhost:3000"

# Comandos de help
.PHONY: help
help:
	@echo "Comandos disponíveis:"
	@echo "  install       - Instala dependências básicas"
	@echo "  install-dev   - Instala dependências de desenvolvimento"
	@echo "  test          - Executa todos os testes"
	@echo "  test-coverage - Executa testes com relatório de cobertura"
	@echo "  test-unit     - Executa apenas testes unitários"
	@echo "  test-usecases - Executa testes de casos de uso"
	@echo "  test-entities - Executa testes de entidades"
	@echo "  test-exceptions - Executa testes de exceções"
	@echo "  test-watch    - Executa testes em modo watch"
	@echo "  migrate-create MESSAGE='msg' - Cria nova migração com mensagem"
	@echo "  migrate-upgrade - Aplica migrações pendentes"
	@echo "  migrate-status - Mostra status das migrações"
	@echo "  run           - Executa a aplicação"
	@echo "  run-dev       - Executa a aplicação em modo desenvolvimento"
	@echo "  run-prod      - Executa a aplicação em modo produção"
	@echo "  lint          - Executa linting do código"
	@echo "  format        - Formata o código"
	@echo "  clean         - Remove arquivos temporários"
	@echo "  clean-all     - Remove tudo incluindo venv"
	@echo "  delete-users  - Deleta todos os usuários do Cognito"
	@echo "  delete-users-dry-run - Simula a deleção de usuários do Cognito"
	@echo "  infra-apply   - Aplica a infraestrutura com Terraform"
	@echo "  run-environment - Inicia o ambiente de desenvolvimento com Docker"
	@echo "  run-playground - Inicia o playground da aplicação"
	@echo "  help          - Mostra esta ajuda"

# Default
.DEFAULT_GOAL := help
