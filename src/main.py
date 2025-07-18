import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from sqlalchemy import inspect # <-- Importante para o diagnóstico

# Importe os seus modelos e o objeto db
from src.models.user import db, User
from src.models.gasto import Gasto
from src.routes.user import user_bp
from src.routes.financeiro import financeiro_bp

# 1. Inicializa o app
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# 2. Habilita o CORS
CORS(app)

# 3. Regista os Blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(financeiro_bp, url_prefix='/api/financeiro')

# 4. Configura o banco de dados
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    local_db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
    os.makedirs(os.path.dirname(local_db_path), exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{local_db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 5. Inicializa o banco de dados
db.init_app(app)

# 6. Rota para servir o frontend
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

# 7. ROTA DE DIAGNÓSTICO AVANÇADO
@app.route('/init-db')
def init_db():
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    output = f"<h1>Diagnóstico do Banco de Dados</h1>"
    output += f"<p>Tentando conectar e criar tabelas em: <strong>{db_uri}</strong></p>"
    
    try:
        with app.app_context():
            # Tenta criar as tabelas
            db.create_all()
            output += "<p>Comando 'db.create_all()' executado com sucesso.</p>"
            
            # Agora, vamos verificar quais tabelas realmente existem
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            output += f"<p>Tabelas encontradas no banco de dados: <strong>{tables}</strong></p>"
            
            if 'gastos' in tables:
                output += "<h2>SUCESSO! A tabela 'gastos' foi encontrada.</h2>"
            else:
                output += "<h2>FALHA: A tabela 'gastos' NÃO foi encontrada após a criação.</h2>"
                
    except Exception as e:
        output += f"<h2>ERRO DURANTE A OPERAÇÃO:</h2><p>{str(e)}</p>"
        
    return output

# 8. Executa o servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
