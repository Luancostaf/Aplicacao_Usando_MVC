from database import db
from models.chamado import Chamado

class ChamadoRepository:
    @staticmethod
    def get_all():
        return Chamado.query.all()

    @staticmethod
    def get_by_id(chamado_id):
        return Chamado.query.get(chamado_id)

    @staticmethod
    def get_by_usuario_id(usuario_id):
        return Chamado.query.filter_by(usuario_id=usuario_id).all()

    @staticmethod
    def get_by_status(status):
        return Chamado.query.filter_by(status=status).all()

    @staticmethod
    def get_by_prioridade(prioridade):
        return Chamado.query.filter_by(prioridade=prioridade).all()

    @staticmethod
    def count_by_usuario_prioridade_alta_nao_encerrados(usuario_id):
        return Chamado.query.filter(
            Chamado.usuario_id == usuario_id,
            Chamado.prioridade == 'Alta',
            Chamado.status != 'Encerrado'
        ).count()

    @staticmethod
    def count_by_status(status):
        return Chamado.query.filter_by(status=status).count()

    @staticmethod
    def count_all():
        return Chamado.query.count()

    @staticmethod
    def save(chamado):
        db.session.add(chamado)
        db.session.commit()
        return chamado

    @staticmethod
    def delete(chamado):
        db.session.delete(chamado)
        db.session.commit()