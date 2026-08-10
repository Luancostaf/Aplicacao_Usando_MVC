from repositories.chamado_repository import ChamadoRepository
from repositories.usuario_repository import UsuarioRepository
from models.chamado import Chamado

class ChamadoService:
    PRIORIDADES_VALIDAS = ['Baixa', 'Média', 'Alta']

    @staticmethod
    def listar_todos():
        return ChamadoRepository.get_all()

    @staticmethod
    def buscar_por_id(chamado_id):
        chamado = ChamadoRepository.get_by_id(chamado_id)
        if not chamado:
            raise ValueError("Chamado não encontrado.")
        return chamado

    @staticmethod
    def criar_chamado(data):
        titulo = data.get('titulo')
        descricao = data.get('descricao')
        prioridade = data.get('prioridade')
        usuario_id = data.get('usuario_id')
        tecnico = data.get('tecnico')

        if not titulo or len(str(titulo).strip()) < 5:
            raise ValueError("O título é obrigatório e deve ter pelo menos 5 caracteres.")

        if not descricao or len(str(descricao).strip()) < 10:
            raise ValueError("A descrição é obrigatória e deve ter pelo menos 10 caracteres.")

        if not usuario_id or not UsuarioRepository.get_by_id(usuario_id):
            raise ValueError("O chamado deve estar vinculado a um usuário existente.")

        if prioridade not in ChamadoService.PRIORIDADES_VALIDAS:
            raise ValueError("Prioridade deve ser 'Baixa', 'Média' ou 'Alta'.")

        if prioridade == 'Alta':
            alta_abertos = ChamadoRepository.count_by_usuario_prioridade_alta_nao_encerrados(usuario_id)
            if alta_abertos >= 5:
                raise ValueError("O usuário já possui 5 chamados de prioridade Alta não encerrados.")

        novo_chamado = Chamado(
            titulo=titulo.strip(),
            descricao=descricao.strip(),
            prioridade=prioridade,
            status='Aberto',
            tecnico=tecnico,
            usuario_id=usuario_id
        )
        return ChamadoRepository.save(novo_chamado)

    @staticmethod
    def atualizar_chamado(chamado_id, data):
        chamado = ChamadoService.buscar_por_id(chamado_id)

        if 'titulo' in data:
            titulo = data.get('titulo')
            if not titulo or len(str(titulo).strip()) < 5:
                raise ValueError("O título deve ter pelo menos 5 caracteres.")
            chamado.titulo = titulo.strip()

        if 'descricao' in data:
            descricao = data.get('descricao')
            if not descricao or len(str(descricao).strip()) < 10:
                raise ValueError("A descrição deve ter pelo menos 10 caracteres.")
            chamado.descricao = descricao.strip()

        if 'prioridade' in data:
            prioridade = data.get('prioridade')
            if prioridade not in ChamadoService.PRIORIDADES_VALIDAS:
                raise ValueError("Prioridade deve ser 'Baixa', 'Média' ou 'Alta'.")
            chamado.prioridade = prioridade

        if 'tecnico' in data:
            chamado.tecnico = data.get('tecnico')

        return ChamadoRepository.save(chamado)

    @staticmethod
    def deletar_chamado(chamado_id):
        chamado = ChamadoService.buscar_por_id(chamado_id)
        ChamadoRepository.delete(chamado)

    @staticmethod
    def iniciar_atendimento(chamado_id):
        chamado = ChamadoService.buscar_por_id(chamado_id)

        if chamado.status != 'Aberto':
            raise ValueError(f"Transição inválida: Não é possível mudar de '{chamado.status}' para 'Em atendimento'.")

        chamado.status = 'Em atendimento'
        return ChamadoRepository.save(chamado)

    @staticmethod
    def encerrar_chamado(chamado_id):
        chamado = ChamadoService.buscar_por_id(chamado_id)

        if chamado.status != 'Em atendimento':
            raise ValueError(f"Transição inválida: Não é possível mudar de '{chamado.status}' para 'Encerrado'.")

        chamado.status = 'Encerrado'
        return ChamadoRepository.save(chamado)

    @staticmethod
    def listar_abertos():
        return ChamadoRepository.get_by_status('Aberto')

    @staticmethod
    def listar_prioridade_alta():
        return ChamadoRepository.get_by_prioridade('Alta')

    @staticmethod
    def obter_estatisticas():
        return {
            "usuarios": UsuarioRepository.count(),
            "chamados": ChamadoRepository.count_all(),
            "abertos": ChamadoRepository.count_by_status("Aberto"),
            "em_atendimento": ChamadoRepository.count_by_status("Em atendimento"),
            "encerrados": ChamadoRepository.count_by_status("Encerrado")
        }