#!/bin/sh

echo "--- A iniciar o processo de deploy ---"

# Passo 1: Executar o script de inicialização do banco de dados
# Usamos 'python -m src.init_db' para executar o ficheiro como um módulo
echo "A executar o script de inicialização do banco de dados..."
python -m src.init_db

# Passo 2: Iniciar o servidor Gunicorn
echo "A iniciar o servidor Gunicorn..."
gunicorn --bind 0.0.0.0:$PORT src.main:app
