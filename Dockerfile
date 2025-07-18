# Usar uma imagem base oficial do Python
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o ficheiro de dependências e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o resto do código do projeto para o contêiner
COPY . .

# Comando para iniciar o servidor diretamente, sem usar o script run.sh
# Usamos o formato exec para evitar problemas de shell
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "src.main:create_app()"]
