import os
import google.generativeai as genai
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta

# Importa os modelos e a instância 'db' partilhada
from src.models.gasto import Gasto
from src.models.user import User, db

financeiro_bp = Blueprint('financeiro', __name__)

# --- ROTA DE REGISTRO (SEM ALTERAÇÕES) ---
@financeiro_bp.route('/registrar_gasto', methods=['POST'])
def registrar_gasto_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Corpo da requisição inválido ou não é JSON.'}), 400

    phone_number = data.get('user_id')
    descricao = data.get('descricao')
    valor = data.get('valor')
    categoria = data.get('categoria')

    if not all([phone_number, descricao, valor, categoria]):
        return jsonify({'error': 'Os campos user_id, descricao, valor e categoria são obrigatórios.'}), 400

    try:
        user = User.query.filter_by(phone_number=str(phone_number)).first()
        if not user:
            user = User(phone_number=str(phone_number))
            db.session.add(user)
            db.session.flush()
            current_app.logger.info(f"Novo utilizador preparado com o telefone {phone_number}")
        
        novo_gasto = Gasto(
            descricao=str(descricao),
            valor=float(valor),
            categoria=str(categoria),
            user_id=user.id
        )
        db.session.add(novo_gasto)
        db.session.commit()
        return jsonify({'message': f'Gasto "{descricao}" no valor de R$ {valor:.2f} registrado com sucesso!'}), 201
    except ValueError:
        db.session.rollback()
        return jsonify({'error': f'O valor fornecido "{valor}" não é um número válido.'}), 400
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"ERRO INTERNO NO ENDPOINT: {e}", exc_info=True)
        return jsonify({'error': 'Ocorreu um erro inesperado no servidor ao salvar os dados.'}), 500


# --- ROTA DE CONSULTA (SEM ALTERAÇÕES) ---
@financeiro_bp.route('/consultar_gastos', methods=['POST'])
def consultar_gastos_endpoint():
    data = request.get_json()
    phone_number = data.get('user_id')
    periodo = data.get('periodo')

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


# --- ROTA DE CONSELHO ---
@financeiro_bp.route('/gerar_conselho', methods=['POST'])
def gerar_conselho():
    data = request.get_json()
    phone_number = data.get('user_id')

    if not phone_number:
        return jsonify({'error': 'user_id é obrigatório'}), 400

    user = User.query.filter_by(phone_number=str(phone_number)).first()
    if not user:
        return jsonify({'response': 'Usuário não encontrado.'})

    hoje = datetime.utcnow()
    trinta_dias_atras = hoje - timedelta(days=30)

    gastos = (
        db.session.query(Gasto.categoria, db.func.sum(Gasto.valor).label('total'))
        .filter(Gasto.user_id == user.id, Gasto.data >= trinta_dias_atras)
        .group_by(Gasto.categoria)
        .all()
    )

    if not gastos:
        return jsonify({'response': 'Você ainda não possui gastos suficientes para gerar um conselho.'})

    texto_gastos = "\n".join([f"{categoria}: R${total:.2f}" for categoria, total in gastos])

    prompt = (
        "Você é um assistente financeiro. Com base nos gastos do usuário nas últimas 4 semanas, "
        "gere um conselho personalizado de forma empática e profissional.\n"
        f"Gastos:\n{texto_gastos}\n"
        "Conselho:"
    )

    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    response = chat.send_message(prompt)
    conselho = response.text

    safety_settings = [
        {"category": "HARM_CATEGORY_DEROGATORY", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_TOXICITY", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_VIOLENCE", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUAL", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_MEDICAL", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"}
    ]

    try:
        response = model.generate_content(prompt, safety_settings=safety_settings)
        conselho_raw = response.text if response and response.text else ""
        conselho = conselho_raw.strip()
    except Exception as e:
        current_app.logger.error(f"Erro ao chamar a API do Gemini para gerar conselho: {e}")
        conselho = (
            "Não consegui gerar um conselho personalizado no momento, mas uma dica geral é sempre anotar seus gastos para ter mais controle."
        )

    return jsonify({'response': conselho})


# --- ROTA DE AJUDA (SEM ALTERAÇÕES) ---
@financeiro_bp.route('/ajuda', methods=['POST'])
def ajuda_endpoint():
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
