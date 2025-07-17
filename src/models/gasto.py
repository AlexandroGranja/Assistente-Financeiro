# Em src/models/gasto.py
from .user import db # Reutilizamos a mesma instância do db

class Gasto(db.Model):
    __tablename__ = 'gastos' # Nome da tabela no banco de dados

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)

    # A "mágica" para ligar o Gasto ao Usuário.
    # Por enquanto vamos deixar comentado para simplificar, mas é aqui que a mágica acontece.
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "descricao": self.descricao,
            "valor": self.valor,
            "categoria": self.categoria
        }