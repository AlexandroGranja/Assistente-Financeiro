import os
import json
import re
from flask import Blueprint, request, jsonify
# Importa os modelos e a instância 'db' partilhada
from src.models.gasto import Gasto
from src.models.user import User, db 
import google.generativeai as genai

# Configuração da API do Gemini
try:
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    if not GEMINI_API_KEY:
        print("--- AVISO: Variável de ambiente GEMINI_API_KEY não encontrada. ---")
    else:
        genai.configure(api_key=GEMINI_API_KEY)
        print("--- DEBUG INFO: Chave da API do Gemini configurada com sucesso. ---")
except Exception as e:
    GEMINI_API_KEY = None
    print(f"--- ERRO: Falha ao configurar a API do Gemini: {e} ---")


financeiro_bp = Blueprint('financeiro', __name__)

def extrair_dados_de_gasto_com_ia(query):
    """Usa a API do Gemini para extrair dados de uma frase."""
    if not GEMINI_API_KEY:
        return {'error': "A chave da API do Gemini não foi configurada no servidor."}

    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Analise a frase a seguir e retorne APENAS um objeto JSON com as chaves "descricao", "valor" e "categoria".
    - "descricao": Um resumo do gasto.
    - "valor": O custo numérico, usando ponto como separador decimal.
    - "categoria": Uma das seguintes: Alimentação, Transporte, Lazer, Moradia, Saúde, Educação, Outros.

    Frase: "{query}"
    """
    
    try:
        response = model.generate_content(prompt)
        match = re.search(r'```json\s*(\{.*?\})\s*```|(\{.*?\})', response.text, re.DOTALL)
        if match:
            json_str = next((g for g in match.groups() if g is not None), None)
            if json_str:
                return json.loads(json_str)
        print(f"--- AVISO: A resposta da IA não continha um JSON válido. Resposta: {response.text} ---")
        return {'error': 'A IA retornou uma resposta em formato inesperado.'}
    except Exception as e:
        print(f"--- ERRO: Exceção na chamada da API do Gemini ou no processamento: {e} ---")
        return {'error': f'Ocorreu um erro ao comunicar com a IA: {e}'}

@financeiro_bp.route('/registrar_gasto', methods=['POST'])
def registrar_gasto_endpoint():
    """Endpoint para registrar um novo gasto."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Corpo da requisição inválido ou não é JSON.'}), 400

    phone_number = data.get('user_id') 
    query = data.get('query')

    if not phone_number or not query:
        return jsonify({'error': 'Os campos user_id (telefone) e query são obrigatórios.'}), 400

    try:
        # --- LÓGICA DE TRANSAÇÃO OTIMIZADA ---
        
        # 1. Encontra ou prepara o utilizador
        user = User.query.filter_by(phone_number=phone_number).first()
        if not user:
            user = User(phone_number=phone_number)
            db.session.add(user)
            # Usa flush para obter o ID do utilizador antes de fazer commit
            db.session.flush()
            print(f"--- INFO: Novo utilizador preparado para a transação com o telefone {phone_number} ---")
        
        # 2. Extrai dados com a IA
        dados_gasto = extrair_dados_de_gasto_com_ia(query)
        if 'error' in dados_gasto:
            # Se a IA falhar, desfaz a adição do utilizador se ele for novo
            db.session.rollback()
            return jsonify({'error': dados_gasto['error']}), 500

        descricao = dados_gasto.get('descricao')
        valor = dados_gasto.get('valor')
        categoria = dados_gasto.get('categoria')

        if not all([descricao, valor, categoria]):
            db.session.rollback()
            return jsonify({'error': 'A IA não conseguiu extrair todas as informações necessárias.' }), 400

        # 3. Prepara o novo gasto
        novo_gasto = Gasto(
            descricao=str(descricao),
            valor=float(valor),
            categoria=str(categoria),
            user_id=user.id
        )
        db.session.add(novo_gasto)
        
        # 4. Faz commit de tudo (utilizador e gasto) de uma só vez
        db.session.commit()

        return jsonify({'message': f'Gasto "{descricao}" no valor de {valor} registrado com sucesso!'}), 201

    except ValueError:
        db.session.rollback()
        return jsonify({'error': f'O valor retornado pela IA não é um número válido.'}), 400
    except Exception as e:
        # Desfaz quaisquer alterações na base de dados se ocorrer um erro
        db.session.rollback()
        print(f"--- ERRO INTERNO NO ENDPOINT: {e} ---")
        return jsonify({'error': 'Ocorreu um erro inesperado no servidor ao salvar os dados.'}), 500
