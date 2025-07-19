from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(50), unique=True, nullable=False) # Campo necessário

    def __repr__(self):
        return f'<User {self.phone_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
        }
