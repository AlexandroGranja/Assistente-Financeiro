import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db, User
from src.models.gasto import Gasto  # <-- ADICIONEI ESTA LINHA
from src.routes.user import user_bp
from src.routes.financeiro import financeiro_bp

# Inicializa o app
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilita o CORS para todas as rotas
CORS(app)

# Registra os Blueprints (rotas da API)
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(financeiro_bp, url_prefix='/api/financeiro')

# Configura o banco de dados
# O caminho aponta para a pasta 'database' dentro de 'src'
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    # Substitui o protocolo para compatibilidade com SQLAlchemy
    database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Se não encontrar a variável do Railway, usa o banco local
    local_db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
    os.makedirs(os.path.dirname(local_db_path), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{local_db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados com o app
db.init_app(app)

# Cria todas as tabelas (agora inclui User e Gasto) dentro do contexto da aplicação
with app.app_context():
    db.create_all()

# Rota para servir o frontend (ex: React, Angular, Vue ou HTML simples)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Executa o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# Em src/main.py

# ... (todo o seu código existente antes disto) ...

# ROTA TEMPORÁRIA PARA FORÇAR A CRIAÇÃO DO BANCO DE DADOS
@app.route('/init-db')
def init_db():
    with app.app_context():
        try:
            db.create_all()
            return "Tabelas criadas com sucesso!"
        except Exception as e:
            return f"Erro ao criar tabelas: {str(e)}"

# Executa o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)