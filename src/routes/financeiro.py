import os
from flask import Blueprint, request, jsonify, current_app
# Importa os modelos e a instância 'db' partilhada
from src.models.gasto import Gasto
from src.models.user import User, db 

financeiro_bp = Blueprint('financeiro', __name__)

@financeiro_bp.route('/registrar_gasto', methods=['POST'])
def registrar_gasto_endpoint():
    """
    Endpoint simplificado para registrar um novo gasto.
    Agora, ele espera receber os dados já processados pela IA do n8n.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Corpo da requisição inválido ou não é JSON.'}), 400

    # Os dados agora vêm prontos do n8n
    phone_number = data.get('user_id') 
    descricao = data.get('descricao')
    valor = data.get('valor')
    categoria = data.get('categoria')

    if not all([phone_number, descricao, valor, categoria]):
        return jsonify({'error': 'Os campos user_id, descricao, valor e categoria são obrigatórios.'}), 400

    try:
        # Encontra ou cria o utilizador
        user = User.query.filter_by(phone_number=str(phone_number)).first()
        if not user:
            user = User(phone_number=str(phone_number))
            db.session.add(user)
            # Usa flush para obter o ID do utilizador antes de fazer commit
            db.session.flush()
            current_app.logger.info(f"Novo utilizador preparado com o telefone {phone_number}")
        
        # Prepara o novo gasto
        novo_gasto = Gasto(
            descricao=str(descricao),
            valor=float(valor),
            categoria=str(categoria),
            user_id=user.id
        )
        db.session.add(novo_gasto)
        
        # Faz commit de tudo de uma só vez
        db.session.commit()

        return jsonify({'message': f'Gasto "{descricao}" no valor de {valor} registrado com sucesso!'}), 201

    except ValueError:
        db.session.rollback()
        current_app.logger.error(f"ValueError: O valor '{valor}' não é um número válido.")
        return jsonify({'error': f'O valor fornecido "{valor}" não é um número válido.'}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"ERRO INTERNO NO ENDPOINT: {e}", exc_info=True)
        return jsonify({'error': 'Ocorreu um erro inesperado no servidor ao salvar os dados.'}), 500
