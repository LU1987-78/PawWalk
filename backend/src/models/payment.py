from src.models.user import db
from datetime import datetime
from enum import Enum

class PaymentStatus(Enum):
    PENDING = 'pending'
    PROCESSED = 'processed'
    FAILED = 'failed'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_passeio = db.Column(db.Integer, db.ForeignKey('walk.id'), nullable=False)
    id_dono = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_passeador = db.Column(db.Integer, db.ForeignKey('walker.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    data_pagamento = db.Column(db.DateTime, default=datetime.utcnow)
    metodo_pagamento = db.Column(db.String(50))

    def __repr__(self):
        return f'<Payment {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'id_passeio': self.id_passeio,
            'id_dono': self.id_dono,
            'id_passeador': self.id_passeador,
            'valor': self.valor,
            'status': self.status.value if self.status else None,
            'data_pagamento': self.data_pagamento.isoformat() if self.data_pagamento else None,
            'metodo_pagamento': self.metodo_pagamento
        }

