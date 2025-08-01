# Makefile para o projeto Inner

# Variáveis
PYTHON = .venv/bin/python
PIP = .venv/bin/pip
PYTHONPATH = src

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
	@echo "  run           - Executa a aplicação"
	@echo "  run-dev       - Executa a aplicação em modo desenvolvimento"
	@echo "  run-prod      - Executa a aplicação em modo produção"
	@echo "  lint          - Executa linting do código"
	@echo "  format        - Formata o código"
	@echo "  clean         - Remove arquivos temporários"
	@echo "  clean-all     - Remove tudo incluindo venv"
	@echo "  help          - Mostra esta ajuda" = $(PYTHON) -m pytest

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
	$(PYTEST) tests/ -v

.PHONY: test-coverage
test-coverage:
	$(PYTEST) tests/ -v --cov=src --cov-report=term-missing --cov-report=html

.PHONY: test-unit
test-unit:
	$(PYTEST) tests/core/ -v

.PHONY: test-usecases
test-usecases:
	$(PYTEST) tests/core/user/ -v

.PHONY: test-entities
test-entities:
	$(PYTEST) tests/core/entities/ -v

.PHONY: test-exceptions
test-exceptions:
	$(PYTEST) tests/core/exceptions/ -v

.PHONY: test-watch
test-watch:
	$(PYTEST) tests/ -v --watch

# Comandos de linting e formatação
.PHONY: lint
lint:
	$(PYTHON) -m flake8 src/ tests/

.PHONY: format
format:
	$(PYTHON) -m black src/ tests/
	$(PYTHON) -m isort src/ tests/

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
	@echo "  lint          - Executa linting do código"
	@echo "  format        - Formata o código"
	@echo "  clean         - Remove arquivos temporários"
	@echo "  clean-all     - Remove tudo incluindo venv"
	@echo "  help          - Mostra esta ajuda"

# Default
.DEFAULT_GOAL := help
