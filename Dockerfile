# Usar uma imagem base oficial do Python
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o ficheiro de dependências e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o resto do código do projeto para o contêiner
COPY . .

# Comando para iniciar o servidor usando o ficheiro wsgi.py e o formato shell
# Isto garante que a variável $PORT é lida e que o Gunicorn encontra a 'app'.
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app
