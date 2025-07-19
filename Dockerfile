# Usa uma imagem base oficial e leve do Python
FROM python:3.9-slim

# Define o diretório de trabalho no contentor
WORKDIR /app

# Copia o ficheiro de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da aplicação
COPY . .

# Expõe a porta que a aplicação vai usar
EXPOSE 8080

# --- COMANDO DEFINITIVO ---
# Inicia o servidor Gunicorn usando o ficheiro wsgi.py.
# Esta sintaxe garante que a variável $PORT do Railway é usada corretamente
# e que todos os logs (debug, access, error) são exibidos.
CMD gunicorn --bind "0.0.0.0:$PORT" --log-level=debug --access-logfile=- --error-logfile=- "wsgi:app"
