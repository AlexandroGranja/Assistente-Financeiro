import os
import json
from flask import Blueprint, request, jsonify
from src.models.gasto import Gasto, db
import google.generativeai as genai

# Configura a chave da API do Gemini a partir das variáveis de ambiente
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print("--- DEBUG INFO: Chave da API do Gemini configurada. ---")
else:
    print("--- AVISO: Chave da API do Gemini não encontrada. A funcionalidade de IA estará desativada. ---")

financeiro_bp = Blueprint('financeiro', __name__)

def extrair_dados_de_gasto_com_ia(query):
    """
    Usa a API do Gemini para extrair descrição, valor e categoria de uma frase.
    """
    if not GEMINI_API_KEY:
        raise ValueError("A chave da API do Gemini não foi configurada.")

    # Cria o modelo generativo
    model = genai.GenerativeModel('gemini-pro')

    # Prompt para a IA, instruindo o que fazer e o formato da resposta
    prompt = f"""
    Analise a frase de um gasto e extraia as seguintes informações:
    1.  "descricao": Um resumo do que foi o gasto.
    2.  "valor": O custo numérico do gasto.
    3.  "categoria": Uma das seguintes categorias: Alimentação, Transporte, Lazer, Moradia, Saúde, Educação, Outros.

    A resposta DEVE ser um objeto JSON válido.

    Frase para análise: "{query}"

    Exemplo de resposta JSON:
    {{
      "descricao": "Café na padaria",
      "valor": 7.50,
      "categoria": "Alimentação"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Limpa a resposta para garantir que é um JSON válido
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
    except Exception as e:
        print(f"Erro na API do Gemini: {e}")
        # Retorna None em caso de falha na comunicação com a IA
        return None

@financeiro_bp.route('/registrar_gasto', methods=['POST'])
def registrar_gasto_endpoint():
    """
    Endpoint para registrar um novo gasto a partir de uma query em linguagem natural.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    query = data.get('query')

    if not user_id or not query:
        return jsonify({'error': 'Os campos user_id e query são obrigatórios.'}), 400

    try:
        # --- LÓGICA MELHORADA USANDO IA ---
        dados_gasto = extrair_dados_de_gasto_com_ia(query)

        if not dados_gasto:
            return jsonify({'error': 'Não foi possível processar a sua mensagem com a IA. Tente novamente.'}), 500

        descricao = dados_gasto.get('descricao')
        valor = dados_gasto.get('valor')
        categoria = dados_gasto.get('categoria')

        if not all([descricao, valor, categoria]):
            return jsonify({'error': 'A IA não conseguiu extrair todas as informações necessárias. Tente ser mais específico(a).'}), 400

        novo_gasto = Gasto(
            descricao=str(descricao),
            valor=float(valor),
            categoria=str(categoria),
            user_id=int(user_id)
        )
        db.session.add(novo_gasto)
        db.session.commit()

        return jsonify({'message': f'Gasto "{descricao}" registrado com sucesso!'}), 201

    except ValueError as ve:
        # Erro caso o valor não seja um número
        return jsonify({'error': f'Erro ao processar o valor do gasto: {ve}'}), 400
    except Exception as e:
        db.session.rollback()
        print(f"ERRO INTERNO: {e}")
        return jsonify({'error': 'Ocorreu um erro inesperado no servidor.'}), 500
