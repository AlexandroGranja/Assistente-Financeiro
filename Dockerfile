# Usa uma imagem base oficial e leve do Python
FROM python:3.11-slim

# Define o diretório de trabalho no contentor
WORKDIR /app

# Copia o ficheiro de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da aplicação
COPY . .

# Dar permissão de execução ao script
RUN chmod +x run.sh

# Expõe a porta que a aplicação vai usar
EXPOSE 8080

# Usar o script run.sh para iniciar a aplicação
CMD ["./run.sh"]
