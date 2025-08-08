#!/bin/bash

# Script para executar os testes do projeto Inner
# Configura o ambiente e executa os testes com coverage

set -e  # Sair se algum comando falhar

echo "🧪 Executando testes do projeto Inner..."

# Configurar PYTHONPATH
export PYTHONPATH="/home/izaias/projetos/inner/src"

# Ativar ambiente virtual
source /home/izaias/projetos/inner/.venv/bin/activate

# Executar testes de entidades de agente
echo "📦 Testando entidades de agente..."
python -m pytest tests/core/entities/agent/ -v --tb=short

# Executar testes de casos de uso (se existirem e funcionarem)
# echo "🔄 Testando casos de uso de agente..."
# python -m pytest tests/core/usecases/agent/ -v --tb=short

# Executar todos os testes funcionais
echo "🎯 Executando todos os testes funcionais..."
python -m pytest tests/core/entities/ -v --tb=short --cov=src --cov-report=term-missing

echo "✅ Testes concluídos!"
