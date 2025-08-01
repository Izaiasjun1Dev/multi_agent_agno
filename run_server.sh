#!/bin/bash

# Script para executar a aplicação Inner API

# Definir diretório do projeto
PROJECT_DIR="/home/izaias/projetos/inner"
VENV_PATH="$PROJECT_DIR/.venv/bin/python"

# Entrar no diretório do projeto
cd "$PROJECT_DIR"

# Configurar PYTHONPATH
export PYTHONPATH="$PROJECT_DIR/src:$PYTHONPATH"

# Executar a aplicação
echo "🚀 Iniciando Inner API..."
echo "📍 URL: http://localhost:8000"
echo "📚 Documentação: http://localhost:8000/docs"
echo ""

$VENV_PATH src/application/main.py
