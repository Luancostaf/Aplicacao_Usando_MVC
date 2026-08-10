from flask import Blueprint, request, jsonify
from services.chamado_service import ChamadoService

chamado_bp = Blueprint('chamado_bp', __name__)

@chamado_bp.route('/chamados', methods=['GET'])
def listar_chamados():
    chamados = ChamadoService.listar_todos()
    return jsonify([c.to_dict() for c in chamados]), 200

@chamado_bp.route('/chamados/', methods=['POST'])
@chamado_bp.route('/chamados', methods=['POST'])
def criar_chamado():
    data = request.get_json() or {}
    try:
        chamado = ChamadoService.criar_chamado(data)
        return jsonify(chamado.to_dict()), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400

@chamado_bp.route('/chamados/<int:chamado_id>', methods=['PUT'])
def atualizar_chamado(chamado_id):
    data = request.get_json() or {}
    try:
        chamado = ChamadoService.atualizar_chamado(chamado_id, data)
        return jsonify(chamado.to_dict()), 200
    except ValueError as e:
        status_code = 404 if "não encontrado" in str(e) else 400
        return jsonify({"erro": str(e)}), status_code

@chamado_bp.route('/chamados/<int:chamado_id>', methods=['DELETE'])
def deletar_chamado(chamado_id):
    try:
        ChamadoService.deletar_chamado(chamado_id)
        return jsonify({"mensagem": "Chamado excluído com sucesso."}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404

@chamado_bp.route('/chamados/<int:chamado_id>/iniciar', methods=['PATCH'])
def iniciar_atendimento(chamado_id):
    try:
        chamado = ChamadoService.iniciar_atendimento(chamado_id)
        return jsonify(chamado.to_dict()), 200
    except ValueError as e:
        status_code = 404 if "não encontrado" in str(e) else 400
        return jsonify({"erro": str(e)}), status_code

@chamado_bp.route('/chamados/<int:chamado_id>/encerrar', methods=['PATCH'])
def encerrar_chamado(chamado_id):
    try:
        chamado = ChamadoService.encerrar_chamado(chamado_id)
        return jsonify(chamado.to_dict()), 200
    except ValueError as e:
        status_code = 404 if "não encontrado" in str(e) else 400
        return jsonify({"erro": str(e)}), status_code

@chamado_bp.route('/chamados/abertos', methods=['GET'])
def listar_abertos():
    chamados = ChamadoService.listar_abertos()
    return jsonify([c.to_dict() for c in chamados]), 200

@chamado_bp.route('/chamados/prioridade/alta', methods=['GET'])
def listar_prioridade_alta():
    chamados = ChamadoService.listar_prioridade_alta()
    return jsonify([c.to_dict() for c in chamados]), 200

@chamado_bp.route('/estatisticas', methods=['GET'])
def obter_estatisticas():
    estatisticas = ChamadoService.obter_estatisticas()
    return jsonify(estatisticas), 200