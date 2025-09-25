from src.models.user import db

class Walker(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    experiencia = db.Column(db.Text)
    descricao = db.Column(db.Text)
    preco_por_passeio = db.Column(db.Float, nullable=False)
    disponibilidade = db.Column(db.JSON)  # Armazenar horários disponíveis
    documentos_verificados = db.Column(db.Boolean, default=False)
    avaliacao_media = db.Column(db.Float, default=0.0)
    numero_avaliacoes = db.Column(db.Integer, default=0)
    
    # Relacionamentos
    usuario = db.relationship('User', backref='perfil_passeador', uselist=False)
    passeios = db.relationship('Walk', foreign_keys='Walk.id_passeador', backref='passeador', lazy=True)
    avaliacoes_recebidas = db.relationship('Review', foreign_keys='Review.id_passeador', backref='avaliado', lazy=True)
    pagamentos_recebidos = db.relationship('Payment', foreign_keys='Payment.id_passeador', backref='recebedor', lazy=True)

    def __repr__(self):
        return f'<Walker {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'experiencia': self.experiencia,
            'descricao': self.descricao,
            'preco_por_passeio': self.preco_por_passeio,
            'disponibilidade': self.disponibilidade,
            'documentos_verificados': self.documentos_verificados,
            'avaliacao_media': self.avaliacao_media,
            'numero_avaliacoes': self.numero_avaliacoes,
            'usuario': self.usuario.to_dict() if self.usuario else None
        }

