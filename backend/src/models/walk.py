from src.models.user import db
from datetime import datetime
from enum import Enum

class WalkStatus(Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

class Walk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_dono = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_passeador = db.Column(db.Integer, db.ForeignKey('walker.id'), nullable=False)
    id_cachorro = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=False)
    data_hora_inicio = db.Column(db.DateTime, nullable=False)
    data_hora_fim_estimada = db.Column(db.DateTime, nullable=False)
    data_hora_fim_real = db.Column(db.DateTime)
    status = db.Column(db.Enum(WalkStatus), nullable=False, default=WalkStatus.PENDING)
    local_encontro = db.Column(db.String(255))
    duracao_estimada = db.Column(db.Integer)  # em minutos
    preco_total = db.Column(db.Float, nullable=False)
    observacoes_dono = db.Column(db.Text)
    observacoes_passeador = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    avaliacao = db.relationship('Review', backref='passeio', uselist=False, cascade='all, delete-orphan')
    pagamento = db.relationship('Payment', backref='passeio', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Walk {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'id_dono': self.id_dono,
            'id_passeador': self.id_passeador,
            'id_cachorro': self.id_cachorro,
            'data_hora_inicio': self.data_hora_inicio.isoformat() if self.data_hora_inicio else None,
            'data_hora_fim_estimada': self.data_hora_fim_estimada.isoformat() if self.data_hora_fim_estimada else None,
            'data_hora_fim_real': self.data_hora_fim_real.isoformat() if self.data_hora_fim_real else None,
            'status': self.status.value if self.status else None,
            'local_encontro': self.local_encontro,
            'duracao_estimada': self.duracao_estimada,
            'preco_total': self.preco_total,
            'observacoes_dono': self.observacoes_dono,
            'observacoes_passeador': self.observacoes_passeador,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }

