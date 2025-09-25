from src.models.user import db
from datetime import datetime

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_passeio = db.Column(db.Integer, db.ForeignKey('walk.id'), nullable=False)
    id_dono = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_passeador = db.Column(db.Integer, db.ForeignKey('walker.id'), nullable=False)
    nota = db.Column(db.Integer, nullable=False)  # 1-5
    comentario = db.Column(db.Text)
    data_avaliacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Review {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'id_passeio': self.id_passeio,
            'id_dono': self.id_dono,
            'id_passeador': self.id_passeador,
            'nota': self.nota,
            'comentario': self.comentario,
            'data_avaliacao': self.data_avaliacao.isoformat() if self.data_avaliacao else None
        }

