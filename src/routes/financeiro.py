import os
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta

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

        # Retorna uma mensagem de sucesso para o n8n enviar ao WhatsApp
        return jsonify({'message': f'Gasto "{descricao}" no valor de R$ {valor:.2f} registrado com sucesso!'}), 201

    except ValueError:
        db.session.rollback()
        current_app.logger.error(f"ValueError: O valor '{valor}' não é um número válido.")
        return jsonify({'error': f'O valor fornecido "{valor}" não é um número válido.'}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"ERRO INTERNO NO ENDPOINT: {e}", exc_info=True)
        return jsonify({'error': 'Ocorreu um erro inesperado no servidor ao salvar os dados.'}), 500

# --- NOVAS ROTAS ADICIONADAS ABAIXO ---

@financeiro_bp.route('/consultar_gastos', methods=['POST'])
def consultar_gastos_endpoint():
    """
    Endpoint para consultar os gastos do dia ou do mês.
    """
    data = request.get_json()
    phone_number = data.get('user_id')
    periodo = data.get('periodo') # "dia" ou "mes"

    user = User.query.filter_by(phone_number=str(phone_number)).first()
    if not user:
        return jsonify({'response': 'Você ainda não tem gastos registrados.'})

    now = datetime.utcnow()
    if periodo == 'dia':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        periodo_texto = "hoje"
    elif periodo == 'mes':
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        periodo_texto = "neste mês"
    else:
        return jsonify({'response': 'Período inválido. Tente #dia ou #mes.'})

    gastos = Gasto.query.filter(Gasto.user_id == user.id, Gasto.data >= start_date).all()
    
    if not gastos:
        return jsonify({'response': f'Você não tem nenhum gasto registrado {periodo_texto}.'})

    total_gasto = sum(g.valor for g in gastos)
    resposta = f'Seu total de gastos {periodo_texto} é de R$ {total_gasto:.2f}.'
    
    return jsonify({'response': resposta})


@financeiro_bp.route('/gerar_conselho', methods=['POST'])
def gerar_conselho_endpoint():
    """
    Endpoint para gerar um conselho financeiro.
    """
    data = request.get_json()
    phone_number = data.get('user_id')

    user = User.query.filter_by(phone_number=str(phone_number)).first()
    if not user:
        return jsonify({'response': 'Você precisa ter alguns gastos registrados para eu poder te dar um conselho.'})

    # Pega os gastos dos últimos 30 dias
    start_date = datetime.utcnow() - timedelta(days=30)
    gastos = Gasto.query.filter(Gasto.user_id == user.id, Gasto.data >= start_date).all()

    if not gastos:
        return jsonify({'response': 'Você não tem gastos recentes para eu analisar.'})
    
    total_gasto = sum(g.valor for g in gastos)
    
    # Futuramente, a lógica da IA pode ser inserida aqui.
    resposta = f"Nos últimos 30 dias, você gastou R$ {total_gasto:.2f}. Uma dica é sempre categorizar seus gastos para entender para onde seu dinheiro está indo. Continue registrando!"

    return jsonify({'response': resposta})


@financeiro_bp.route('/ajuda', methods=['POST'])
def ajuda_endpoint():
    """
    Endpoint que retorna uma mensagem de ajuda com os comandos disponíveis.
    """
    texto_ajuda = (
        "Olá! Sou seu assistente financeiro. Veja como posso te ajudar:\n\n"
        "➡️ Para registrar um gasto, apenas me diga o que comprou. Ex: 'Almoço 25.50 alimentação'\n\n"
        "➡️ Para ver seus gastos, use os comandos:\n"
        "   • `#dia` - Mostra o total gasto hoje.\n"
        "   • `#mes` - Mostra o total gasto no mês.\n\n"
        "➡️ Para receber uma dica, use:\n"
        "   • `#conselho` - Analiso seus gastos e te dou uma dica de economia."
    )
    return jsonify({'response': texto_ajuda})
