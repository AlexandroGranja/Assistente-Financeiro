# Configuração do Gunicorn para o Backend Prosper
import os

# Configurações básicas do servidor
bind = f"0.0.0.0:{os.environ.get('PORT', 8080)}"
workers = int(os.environ.get('WEB_CONCURRENCY', 1))
threads = int(os.environ.get('THREADS', 2))
worker_class = "sync"

# Timeout settings
timeout = 120  # Aumentado para dar tempo para a IA responder
keepalive = 5
graceful_timeout = 30

# Logging
loglevel = os.environ.get('LOG_LEVEL', 'info')
accesslog = '-'  # Log para stdout
errorlog = '-'   # Log para stderr
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Performance
preload_app = True
max_requests = 1000  # Reinicia worker após 1000 requests
max_requests_jitter = 100

# Security headers
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}

# Permitir proxies do Railway/outras plataformas
forwarded_allow_ips = ['127.0.0.1', '::1', '*']

# Configurações específicas para o ambiente
if os.environ.get('RAILWAY_ENVIRONMENT'):
    # Configurações específicas para Railway
    workers = 1  # Railway funciona melhor com 1 worker
    threads = 4  # Mais threads para lidar com requests concorrentes
    worker_connections = 1000
elif os.environ.get('HEROKU'):
    # Configurações específicas para Heroku
    workers = int(os.environ.get('WEB_CONCURRENCY', 2))
    
print(f"🚀 Gunicorn configurado com {workers} workers e {threads} threads por worker")
print(f"🌐 Bind: {bind}")
print(f"📊 Log level: {loglevel}")
