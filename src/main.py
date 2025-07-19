import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from sqlalchemy import inspect

# Importe os seus modelos e o objeto db
# É uma boa prática garantir que o diretório 'src' esteja no path
# para que os imports funcionem de forma consistente.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.user import db, User
from src.models.gasto import Gasto
from src.routes.user import user_bp
from src.routes.financeiro import financeiro_bp

# O padrão "Application Factory"
def create_app():
    """
    Cria e configura uma instância da aplicação Flask.
    """
    # 1. Inicializa o app
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # 2. Configura a aplicação
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'uma-chave-secreta-padrao-muito-forte')
    CORS(app)

    # 3. Configura o banco de dados
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Garante que a URL do Heroku/Render funcione com SQLAlchemy
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print("--- CONFIG: Usando banco de dados POSTGRES. ---")
    else:
        # Fallback para SQLite se a variável de ambiente não for encontrada
        local_db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
        os.makedirs(os.path.dirname(local_db_path), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{local_db_path}'
        print("--- CONFIG: Usando banco de dados SQLITE local. ---")

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 4. Inicializa o banco de dados com o app
    db.init_app(app)

    # 5. Regista os Blueprints (rotas da API)
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(financeiro_bp, url_prefix='/api/financeiro')

    # 6. Define as rotas para servir o frontend estático
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if not static_folder_path:
            return "Static folder not configured", 404
        
        # Se o caminho solicitado existir nos arquivos estáticos, sirva-o
        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            # Caso contrário, sirva o index.html (para Single Page Applications)
            index_path = os.path.join(static_folder_path, 'index.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                return "index.html not found", 404

    # 7. CRÍTICO: Retorna a instância do app criada
    return app

# Este bloco só é usado quando você executa 'python src/main.py' diretamente
if __name__ == '__main__':
    app = create_app()
    # A porta é lida da variável de ambiente PORT, com um padrão de 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
