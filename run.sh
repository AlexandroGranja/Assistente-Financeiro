#!/bin/sh

echo "--- A iniciar o processo de deploy com Application Factory ---"

# Inicia o Gunicorn com a flag --unbuffered para mostrar os logs imediatamente
# Usamos 'python -m src.init_db' para executar o ficheiro como um módulo
echo "A executar o script de inicialização do banco de dados..."
python -m src.init_db

# Inicia o Gunicorn com a flag --unbuffered
echo "A iniciar o servidor Gunicorn com logs imediatos..."
gunicorn --unbuffered --bind 0.0.0.0:$PORT 'src.main:create_app()'
