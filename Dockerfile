# Usar uma imagem base oficial do Python
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o ficheiro de dependências e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o resto do código do projeto para o contêiner
COPY . .

# Dar permissão de execução ao nosso novo script
RUN chmod +x run.sh

# O comando para iniciar o servidor agora é o nosso script
CMD ["./run.sh"]