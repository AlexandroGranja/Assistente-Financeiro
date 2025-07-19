import os
import json
import re
from flask import Blueprint, request, jsonify
from src.models.gasto import Gasto, db
import google.generativeai as genai

# Tenta configurar a chave da API do Gemini a partir das variáveis de ambiente
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
    """
    Usa a API do Gemini para extrair descrição, valor e categoria de uma frase.
    Esta versão é mais robusta para extrair JSON da resposta da IA.
    """
    if not GEMINI_API_KEY:
        # Retorna um erro claro se a chave da API não estiver disponível
        return {'error': "A chave da API do Gemini não foi configurada no servidor."}

    # Cria o modelo generativo
    model = genai.GenerativeModel('gemini-pro')

    # Prompt melhorado: mais direto e com instruções claras para evitar texto extra.
    prompt = f"""
    Analise a frase a seguir e retorne APENAS um objeto JSON com as chaves "descricao", "valor" e "categoria".
    - "descricao": Um resumo do gasto.
    - "valor": O custo numérico, usando ponto como separador decimal.
    - "categoria": Uma das seguintes: Alimentação, Transporte, Lazer, Moradia, Saúde, Educação, Outros.

    Frase: "{query}"
    """
    
    try:
        response = model.generate_content(prompt)
        
        # Lógica de extração de JSON mais robusta
        # Procura por um bloco JSON delimitado por ```json e ``` ou por { e }
        match = re.search(r'```json\s*(\{.*?\})\s*```|(\{.*?\})', response.text, re.DOTALL)
        
        if match:
            # Pega o primeiro grupo que não for nulo (o bloco JSON)
            json_str = next((g for g in match.groups() if g is not None), None)
            if json_str:
                return json.loads(json_str)

        # Se não encontrar um bloco JSON, retorna um erro
        print(f"--- AVISO: A resposta da IA não continha um JSON válido. Resposta: {response.text} ---")
        return {'error': 'A IA retornou uma resposta em formato inesperado.'}

    except Exception as e:
        print(f"--- ERRO: Exceção na chamada da API do Gemini ou no processamento: {e} ---")
        return {'error': f'Ocorreu um erro ao comunicar com a IA: {e}'}

@financeiro_bp.route('/registrar_gasto', methods=['POST'])
def registrar_gasto_endpoint():
    """
    Endpoint para registrar um novo gasto a partir de uma query em linguagem natural.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Corpo da requisição inválido ou não é JSON.'}), 400

    user_id = data.get('user_id')
    query = data.get('query')

    if not user_id or not query:
        return jsonify({'error': 'Os campos user_id e query são obrigatórios.'}), 400

    try:
        # --- LÓGICA MELHORADA USANDO IA ---
        dados_gasto = extrair_dados_de_gasto_com_ia(query)

        # Verifica se a função de IA retornou um erro
        if 'error' in dados_gasto:
            return jsonify({'error': dados_gasto['error']}), 500

        descricao = dados_gasto.get('descricao')
        valor = dados_gasto.get('valor')
        categoria = dados_gasto.get('categoria')

        if not all([descricao, valor, categoria]):
            return jsonify({'error': 'A IA não conseguiu extrair todas as informações necessárias (descrição, valor, categoria). Tente ser mais específico(a).' }), 400

        novo_gasto = Gasto(
            descricao=str(descricao),
            valor=float(valor),
            categoria=str(categoria),
            user_id=str(user_id) # Garante que o user_id seja uma string
        )
        db.session.add(novo_gasto)
        db.session.commit()

        return jsonify({'message': f'Gasto "{descricao}" no valor de {valor} registrado com sucesso!'}), 201

    except ValueError:
        return jsonify({'error': f'O valor "{valor}" retornado pela IA não é um número válido.'}), 400
    except Exception as e:
        db.session.rollback()
        print(f"--- ERRO INTERNO NO ENDPOINT: {e} ---")
        return jsonify({'error': 'Ocorreu um erro inesperado no servidor ao salvar os dados.'}), 500
