#!/bin/bash

# Script para iniciar a aplicação Flask
# Este script garante que todas as variáveis de ambiente sejam carregadas corretamente

echo "🚀 Iniciando Assistente Financeiro WhatsApp..."
echo "📅 Data/Hora: $(date)"
echo "🔧 Python Version: $(python --version)"
echo "📁 Diretório atual: $(pwd)"

# Verificar se as variáveis de ambiente essenciais estão definidas
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️ AVISO: GEMINI_API_KEY não está definida"
fi

if [ -z "$PORT" ]; then
    echo "⚠️ AVISO: PORT não está definida, usando 8080 como padrão"
    export PORT=8080
fi

echo "🌐 Porta configurada: $PORT"

# Iniciar o servidor Gunicorn
echo "🔥 Iniciando servidor Gunicorn..."
exec gunicorn --bind "0.0.0.0:$PORT" \
    --log-level=info \
    --access-logfile=- \
    --error-logfile=- \
    --workers=1 \
    --timeout=120 \
    "wsgi:app"