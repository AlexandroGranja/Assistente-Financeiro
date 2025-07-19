# Usa uma imagem base oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho no contentor
WORKDIR /app

# Copia o ficheiro de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da aplicação
COPY . .

# Expõe a porta que o Gunicorn vai usar
EXPOSE 8080

# --- COMANDO ATUALIZADO COM LOGGING DETALHADO ---
# Inicia o servidor Gunicorn, forçando os logs (debug, access, error) a serem exibidos.
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--log-level=debug", "--access-logfile=-", "--error-logfile=-", "wsgi:app"]
