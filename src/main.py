import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS

# Garante que o diretório 'src' esteja no path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa o db a partir do user.py, que será a nossa fonte única
from src.models.user import db, User 
from src.models.gasto import Gasto
from src.routes.user import user_bp
from src.routes.financeiro import financeiro_bp

# O padrão "Application Factory"
def create_app():
    """
    Cria e configura uma instância da aplicação Flask.
    """
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Configuração da aplicação
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'uma-chave-secreta-padrao-muito-forte')
    CORS(app)

    # Configuração do banco de dados
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print("--- CONFIG: Usando banco de dados POSTGRES. ---")
    else:
        local_db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
        os.makedirs(os.path.dirname(local_db_path), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{local_db_path}'
        print("--- CONFIG: Usando banco de dados SQLITE local. ---")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o banco de dados com o app
    db.init_app(app)

    # Regista os Blueprints (rotas da API)
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(financeiro_bp, url_prefix='/api/financeiro')

    # Define as rotas para servir o frontend estático
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if not static_folder_path:
            return "Static folder not configured", 404
        
        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404

    return app

# Bloco para execução local
if __name__ == '__main__':
    app = create_app()
    # Adiciona o contexto da aplicação para criar as tabelas localmente se não existirem
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
