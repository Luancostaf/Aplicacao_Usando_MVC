from repositories.usuario_repository import UsuarioRepository
from repositories.chamado_repository import ChamadoRepository
from models.usuario import Usuario

class UsuarioService:
    @staticmethod
    def listar_todos():
        return UsuarioRepository.get_all()

    @staticmethod
    def buscar_por_id(usuario_id):
        usuario = UsuarioRepository.get_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado.")
        return usuario

    @staticmethod
    def criar_usuario(data):
        nome = data.get('nome')
        email = data.get('email')
        setor = data.get('setor')

        if not nome or not str(nome).strip():
            raise ValueError("O nome é obrigatório.")
        if not email or not str(email).strip():
            raise ValueError("O e-mail é obrigatório.")

        if UsuarioRepository.get_by_email(email):
            raise ValueError("Já existe um usuário cadastrado com este e-mail.")

        novo_usuario = Usuario(nome=nome.strip(), email=email.strip(), setor=setor)
        return UsuarioRepository.save(novo_usuario)

    @staticmethod
    def atualizar_usuario(usuario_id, data):
        usuario = UsuarioService.buscar_por_id(usuario_id)

        email = data.get('email')
        if email and email != usuario.email:
            if UsuarioRepository.get_by_email(email):
                raise ValueError("Já existe outro usuário com este e-mail.")
            usuario.email = email

        if 'nome' in data:
            nome = data.get('nome')
            if not nome or not str(nome).strip():
                raise ValueError("O nome é obrigatório.")
            usuario.nome = nome.strip()

        if 'setor' in data:
            usuario.setor = data.get('setor')

        return UsuarioRepository.save(usuario)

    @staticmethod
    def deletar_usuario(usuario_id):
        usuario = UsuarioService.buscar_por_id(usuario_id)
        
        chamados = ChamadoRepository.get_by_usuario_id(usuario_id)
        if len(chamados) > 0:
            raise ValueError("Não é possível excluir um usuário que possua chamados cadastrados.")

        UsuarioRepository.delete(usuario)

    @staticmethod
    def buscar_chamados_do_usuario(usuario_id):
        UsuarioService.buscar_por_id(usuario_id)
        return ChamadoRepository.get_by_usuario_id(usuario_id)