#!/bin/sh

# Este script garante que as variáveis de ambiente são carregadas antes de iniciar o servidor.

echo "--- A iniciar o servidor ---"
echo "A DATABASE_URL que a aplicação vai usar é: $DATABASE_URL"

# Inicia o Gunicorn
gunicorn --bind 0.0.0.0:$PORT src.main:app