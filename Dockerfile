# Use uma imagem Python otimizada
FROM python:3.11-slim

# Defina o diretório de trabalho
WORKDIR /app

# Instale dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copie apenas o arquivo de requirements primeiro (para cache do Docker)
COPY requirements.txt .

# Instale as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie o resto dos arquivos da aplicação
COPY . .

# Crie um usuário não-root para segurança
RUN useradd --create-home --shell /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

# Exponha a porta
EXPOSE 8080

# Defina variáveis de ambiente padrão
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV PORT=8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Comando para iniciar a aplicação
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:aplicacao"]
