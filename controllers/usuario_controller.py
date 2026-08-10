from flask import Blueprint, request, jsonify
from services.usuario_service import UsuarioService

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = UsuarioService.listar_todos()
    return jsonify([u.to_dict() for u in usuarios]), 200

@usuario_bp.route('/usuarios/', methods=['POST'])
@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.get_json() or {}
    try:
        usuario = UsuarioService.criar_usuario(data)
        return jsonify(usuario.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    data = request.get_json() or {}
    try:
        usuario = UsuarioService.atualizar_usuario(usuario_id, data)
        return jsonify(usuario.to_dict()), 200
    except ValueError as e:
        status_code = 404 if "não encontrado" in str(e) else 400
        return jsonify({"erro": str(e)}), status_code

@usuario_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def deletar_usuario(usuario_id):
    try:
        UsuarioService.deletar_usuario(usuario_id)
        return jsonify({"mensagem": "Usuário excluído com sucesso."}), 200
    except ValueError as e:
        status_code = 404 if "não encontrado" in str(e) else 400
        return jsonify({"erro": str(e)}), status_code

@usuario_bp.route('/usuarios/<int:usuario_id>/chamados', methods=['GET'])
@usuario_bp.route('/usuarios/<int:usuario_id>/Chamados', methods=['GET'])
def listar_chamados_usuario(usuario_id):
    try:
        chamados = UsuarioService.buscar_chamados_do_usuario(usuario_id)
        return jsonify([c.to_dict() for c in chamados]), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404