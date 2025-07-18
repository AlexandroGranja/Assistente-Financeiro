import os
from sqlalchemy import inspect

# Importa a 'app' e o 'db' do seu ficheiro principal
from .main import app, db

print("--- A executar o script de inicialização do banco de dados ---")

# Pega a URI do banco de dados diretamente do ambiente
db_uri = os.environ.get('DATABASE_URL')

if not db_uri:
    print("ERRO FATAL: DATABASE_URL não encontrada. A abortar a inicialização.")
    exit(1)

print(f"A conectar-se a: {db_uri.split('@')[1]}") # Mostra o host sem a senha

# Configura a app para usar a URI
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

try:
    # O contexto da app é necessário para o SQLAlchemy funcionar
    with app.app_context():
        print("A tentar criar as tabelas...")
        db.create_all()
        print("Comando 'db.create_all()' executado.")

        # Verificação final
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tabelas encontradas após a criação: {tables}")
        if 'gastos' in tables:
            print("SUCESSO: Tabela 'gastos' criada com sucesso no banco de dados.")
        else:
            print("AVISO: Tabela 'gastos' não foi encontrada após a execução.")

except Exception as e:
    print(f"Ocorreu um erro durante a inicialização do banco de dados: {e}")
    exit(1)

print("--- Script de inicialização do banco de dados concluído ---")
