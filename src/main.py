import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from sqlalchemy import inspect

# Importe os seus modelos e o objeto db
from src.models.user import db, User
from src.models.gasto import Gasto
from src.routes.user import user_bp
from src.routes.financeiro import financeiro_bp

# O padrão "Application Factory"
def create_app():
    # 1. Inicializa o app
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # 2. Configura a aplicação
    app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
    CORS(app)

    # 3. Configura o banco de dados
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print(f"--- CONFIG: A usar banco de dados POSTGRES. ---")
    else:
        # Fallback para SQLite se a variável não for encontrada
        local_db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
        os.makedirs(os.path.dirname(local_db_path), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{local_db_path}'
        print(f"--- CONFIG: A usar banco de dados SQLITE local. ---")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 4. Inicializa o banco de dados com o app
    db.init_app(app)

    # 5. Regista os Blueprints (rotas da API)
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(financeiro_bp, url_prefix='/api/financeiro')

    # 6. Define as rotas principais dentro da factory
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

    

# Este bloco só é usado quando você executa 'python src/main.py' no seu computador
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
