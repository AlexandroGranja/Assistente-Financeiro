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


# --- ROTA DE CONSELHO (COM A CORREÇÃO FINAL) ---
# (As outras rotas e importações no topo do arquivo continuam as mesmas)

@financeiro_bp.route('/gerar_conselho', methods=['POST'])
def gerar_conselho_endpoint():
    """
    Endpoint para gerar um conselho financeiro personalizado e sincero usando a IA.
    """
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("A chave da API do Gemini não foi encontrada nas variáveis de ambiente.")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        current_app.logger.error(f"Erro ao configurar a API do Gemini: {e}")
        return jsonify({'response': 'Desculpe, estou com problemas para me conectar à minha inteligência. Tente novamente mais tarde.'})

    data = request.get_json()
    phone_number = data.get('user_id')

    user = User.query.filter_by(phone_number=str(phone_number)).first()
    if not user:
        return jsonify({'response': 'Você precisa ter alguns gastos registrados para eu poder te dar um conselho.'})

    start_date = datetime.utcnow() - timedelta(days=30)
    gastos = Gasto.query.filter(Gasto.user_id == user.id, Gasto.data >= start_date).all()

    if not gastos:
        return jsonify({'response': 'Você não tem gastos recentes para eu analisar.'})
    
    lista_de_gastos_texto = "\n".join([f"- {g.descricao} (categoria: {g.categoria}): R$ {g.valor:.2f}" for g in gastos])
    total_gasto = sum(g.valor for g in gastos)

    prompt = f"""
    Aja como um consultor financeiro pessoal, direto e sem rodeios. Seu objetivo é ajudar o usuário a economizar dinheiro.
    Analise a lista de gastos dos últimos 30 dias de um usuário. Identifique padrões de consumo e dê conselhos práticos.
    Use exemplos DIRETOS da lista de gastos para ilustrar seus pontos.

    **Dados do Usuário:**
    - Total Gasto nos Últimos 30 Dias: R$ {total_gasto:.2f}
    - Lista de Gastos:
    {lista_de_gastos_texto}

    **Sua Resposta:**
    """

    try:
        # --- ESTA É A ALTERAÇÃO CRUCIAL ---
        # Adicionamos configurações de segurança para evitar bloqueios desnecessários.
        safety_settings = {
            'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
            'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
            'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
            'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'
        }

        # Chama a IA com as novas configurações de segurança
        response = model.generate_content(
            prompt,
            safety_settings=safety_settings
        )
        conselho = response.text
    except Exception as e:
        current_app.logger.error(f"Erro ao chamar a API do Gemini para gerar conselho: {e}")
        conselho = "Não consegui gerar um conselho personalizado no momento, mas uma dica geral é sempre anotar seus gastos para ter mais controle."

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
