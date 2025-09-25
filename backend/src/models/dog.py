from src.models.user import db

class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_dono = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(50))
    idade = db.Column(db.Integer)
    temperamento = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    foto_url = db.Column(db.String(255))
    
    # Relacionamentos
    passeios = db.relationship('Walk', backref='cachorro', lazy=True)

    def __repr__(self):
        return f'<Dog {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'id_dono': self.id_dono,
            'nome': self.nome,
            'raca': self.raca,
            'idade': self.idade,
            'temperamento': self.temperamento,
            'observacoes': self.observacoes,
            'foto_url': self.foto_url
        }

