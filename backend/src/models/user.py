from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class UserType(Enum):
    OWNER = 'owner'
    WALKER = 'walker'
    ADMIN = 'admin'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.Text)
    tipo_usuario = db.Column(db.Enum(UserType), nullable=False, default=UserType.OWNER)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    cachorros = db.relationship('Dog', backref='dono', lazy=True, cascade='all, delete-orphan')
    passeios_como_dono = db.relationship('Walk', foreign_keys='Walk.id_dono', backref='dono', lazy=True)
    avaliacoes_feitas = db.relationship('Review', foreign_keys='Review.id_dono', backref='avaliador', lazy=True)
    pagamentos_feitos = db.relationship('Payment', foreign_keys='Payment.id_dono', backref='pagador', lazy=True)

    def __repr__(self):
        return f'<User {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'tipo_usuario': self.tipo_usuario.value if self.tipo_usuario else None,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None
        }

