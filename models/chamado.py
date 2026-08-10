from database import db
from datetime import datetime

class Chamado(db.Model):
    __tablename__ = 'chamados'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    prioridade = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Aberto')
    tecnico = db.Column(db.String(100), nullable=True)
    data_abertura = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "prioridade": self.prioridade,
            "status": self.status,
            "tecnico": self.tecnico,
            "data_abertura": self.data_abertura.isoformat() if self.data_abertura else None,
            "usuario_id": self.usuario_id
        }