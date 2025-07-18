# Este ficheiro cria a instância da aplicação para o servidor Gunicorn usar.
from src.main import create_app

app = create_app()
