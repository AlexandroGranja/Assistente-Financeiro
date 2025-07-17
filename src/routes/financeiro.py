# Em src/routes/financeiro.py
from flask import Blueprint, request, jsonify
from datetime import datetime
import google.generativeai as genai
import os

# Importe os modelos e o objeto 'db'
from ..models.gasto import Gasto
from ..models.user import db

financeiro_bp = Blueprint('financeiro', __name__)

# Configuração da API do Gemini (isso já deve estar funcionando)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Função para chamar o Gemini e extrair dados da mensagem
def extrair_dados_com_gemini(mensagem):
    if not GEMINI_API_KEY:
        return None
        
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
        Analise a seguinte mensagem de um usuário registrando um gasto e extraia a descrição, o valor e a categoria.
        Retorne os dados em formato JSON com as chaves "descricao", "valor" e "categoria".
        Exemplo de mensagem: "Almoço 25.50 alimentação"
        Exemplo de saída: {{"descricao": "Almoço", "valor": 25.50, "categoria": "alimentação"}}
        Mensagem do usuário: "{mensagem}"
    """
    try:
        response = model.generate_content(prompt)
        # Limpa a saída para ser um JSON válido
        json_response = response.text.strip().replace('`', '').replace('json', '')
        return json.loads(json_response)
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        return None

@financeiro_bp.route('/processar_mensagem', methods=['POST'])
def processar_mensagem():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Mensagem não fornecida"}), 400

    mensagem = data['message'].lower()
    today = datetime.now().strftime('%Y-%m-%d')

    # Comandos especiais
    if mensagem == 'total':
        total_gasto = db.session.query(db.func.sum(Gasto.valor)).scalar() or 0.0
        return jsonify({"response": f"💸 O total de gastos registrado é: R$ {total_gasto:.2f}"})
    
    # Adicionar lógica para outros comandos como 'conselho', 'ajuda', etc.

    # Processamento normal de gastos via Gemini
    dados_gasto = extrair_dados_com_gemini(mensagem)
    
    if not dados_gasto or not all(k in dados_gasto for k in ["descricao", "valor", "categoria"]):
         return jsonify({"error": "Não foi possível processar a sua mensagem. Tente o formato: 'descrição valor categoria'."}), 400

    # Crie o novo objeto Gasto
    novo_gasto = Gasto(
        data=today,
        descricao=dados_gasto['descricao'].capitalize(),
        valor=float(dados_gasto['valor']),
        categoria=dados_gasto['categoria'].lower()
    )

    # Adicione ao banco de dados
    db.session.add(novo_gasto)
    db.session.commit()

    response_text = f"✅ Gasto registrado!\n💸 {novo_gasto.descricao}: R$ {novo_gasto.valor:.2f}\n📂 Categoria: {novo_gasto.categoria}"
    
    return jsonify({
        "response": response_text,
        "data": novo_gasto.to_dict()
    }), 200


@financeiro_bp.route('/relatorio', methods=['GET'])
def gerar_relatorio():
    try:
        # Consulta todos os gastos no banco de dados
        todos_os_gastos = Gasto.query.order_by(Gasto.data.desc()).all()
        
        # Converte os objetos para dicionários
        gastos_dict = [gasto.to_dict() for gasto in todos_os_gastos]

        if not gastos_dict:
            return jsonify({"mensagem": "Nenhum gasto registrado ainda."})

        return jsonify(gastos_dict)

    except Exception as e:
        return jsonify({"error": f"Erro ao gerar relatório: {str(e)}"}), 500