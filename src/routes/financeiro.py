from datetime import datetime
# --- CORREÇÃO CRÍTICA ---
# Em vez de criar uma nova instância da base de dados com `db = SQLAlchemy()`,
# importamos a instância 'db' que já foi criada no ficheiro user.py.
# Isto garante que toda a aplicação partilha a mesma ligação à base de dados.
from .user import db

class Gasto(db.Model):
    __tablename__ = 'gastos'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # A Foreign Key aponta para a tabela 'user' e coluna 'id'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'valor': self.valor,
            'categoria': self.categoria,
            'data': self.data.isoformat(),
            'user_id': self.user_id
        }
