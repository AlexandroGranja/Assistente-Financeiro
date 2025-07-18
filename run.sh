#!/bin/sh

echo "--- A iniciar o processo de deploy com Application Factory ---"

# Inicia o Gunicorn chamando a função create_app()
# O formato é 'modulo:nome_da_funcao()'
gunicorn --bind 0.0.0.0:$PORT 'src.main:create_app()'
