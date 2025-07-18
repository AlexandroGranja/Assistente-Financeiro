#!/bin/sh

echo "--- A iniciar o processo de deploy ---"

# Passo 1: Executar o script de inicialização do banco de dados
echo "A executar o script de inicialização do banco de dados..."
python -m src.init_db

# Passo 2: Iniciar o servidor Gunicorn
# Definimos a variável PYTHONUNBUFFERED=1 para logs imediatos (método padrão)
echo "A iniciar o servidor Gunicorn..."
export PYTHONUNBUFFERED=1
gunicorn --bind 0.0.0.0:$PORT 'src.main:create_app()'
