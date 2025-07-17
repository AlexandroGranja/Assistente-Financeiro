from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os
import sys
from datetime import datetime
import re
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Adicionar o diretório pai ao path para importar excel_handler
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from excel_handler import add_expense, get_total_expenses, get_all_expenses

financeiro_bp = Blueprint('financeiro', __name__)

# Configurar Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

def parse_expense_message(message):
    """
    Parse da mensagem para extrair dados do gasto
    Formatos aceitos:
    - "Almoço 25.50 alimentação"
    - "Gasolina 80 transporte"
    - "Cinema 30.00 lazer"
    """
    # Remove espaços extras e converte para minúsculo
    message = message.strip()
    
    # Padrão para capturar: descrição valor categoria
    pattern = r'^(.+?)\s+(\d+(?:[.,]\d{2})?)\s+(.+)$'
    match = re.match(pattern, message)
    
    if match:
        descricao = match.group(1).strip()
        valor_str = match.group(2).replace(',', '.')
        categoria = match.group(3).strip()
        
        try:
            valor = float(valor_str)
            return {
                'descricao': descricao,
                'valor': valor,
                'categoria': categoria,
                'data': datetime.now().strftime('%Y-%m-%d')
            }
        except ValueError:
            return None
    
    return None

@financeiro_bp.route('/processar_mensagem', methods=['POST'])
def processar_mensagem():
    """
    Endpoint principal para processar mensagens do WhatsApp via n8n
    """
    try:
        data = request.get_json()
        message = data.get('message', '').strip().lower()
        
        if not message:
            return jsonify({'error': 'Mensagem vazia'}), 400
        
        # Comandos especiais
        if message == 'total':
            total = get_total_expenses()
            return jsonify({
                'response': f'💰 Total gasto: R$ {total:.2f}',
                'type': 'total'
            })
        
        elif message == 'conselho':
            return jsonify({
                'response': 'Gerando conselho personalizado...',
                'type': 'conselho',
                'action': 'generate_advice'
            })
        
        elif message == 'ajuda' or message == 'help':
            help_text = """
🤖 *Agente Financeiro IA*

📝 *Como registrar gastos:*
Digite: [descrição] [valor] [categoria]
Exemplo: Almoço 25.50 alimentação

💰 *Comandos disponíveis:*
• `total` - Ver total gasto
• `conselho` - Receber dicas de economia
• `ajuda` - Ver esta mensagem

📊 *Categorias sugeridas:*
alimentação, transporte, lazer, saúde, educação, casa, roupas, outros
            """
            return jsonify({
                'response': help_text,
                'type': 'help'
            })
        
        # Tentar fazer parse como gasto
        expense_data = parse_expense_message(data.get('message', ''))
        
        if expense_data:
            # Registrar o gasto
            add_expense(
                expense_data['data'],
                expense_data['descricao'],
                expense_data['valor'],
                expense_data['categoria']
            )
            
            return jsonify({
                'response': f'✅ Gasto registrado!\n💸 {expense_data["descricao"]}: R$ {expense_data["valor"]:.2f}\n🏷️ Categoria: {expense_data["categoria"]}',
                'type': 'expense_added',
                'data': expense_data
            })
        
        else:
            return jsonify({
                'response': '❌ Formato inválido. Digite "ajuda" para ver como usar.',
                'type': 'error'
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@financeiro_bp.route('/gerar_conselho', methods=['POST'])
def gerar_conselho():
    """
    Endpoint para gerar conselhos usando Gemini
    """
    try:
        # Obter todos os gastos
        expenses = get_all_expenses()
        total = get_total_expenses()
        
        if not expenses:
            return jsonify({
                'response': '📊 Você ainda não registrou nenhum gasto. Comece registrando seus gastos para receber conselhos personalizados!'
            })
        
        # Preparar dados para o Gemini
        expense_summary = {}
        for expense in expenses:
            categoria = expense['Categoria']
            valor = expense['Valor']
            if categoria in expense_summary:
                expense_summary[categoria] += valor
            else:
                expense_summary[categoria] = valor
        
        # Criar prompt para o Gemini
        prompt = f"""
Você é um consultor financeiro especializado em economia doméstica. Analise os seguintes gastos e forneça conselhos práticos e personalizados:

RESUMO DOS GASTOS:
Total gasto: R$ {total:.2f}

Gastos por categoria:
"""
        
        for categoria, valor in expense_summary.items():
            percentual = (valor / total) * 100
            prompt += f"- {categoria.title()}: R$ {valor:.2f} ({percentual:.1f}%)\n"
        
        prompt += """

Por favor, forneça:
1. Uma análise dos padrões de gasto
2. 3 dicas específicas de economia baseadas nos dados
3. Sugestões de metas financeiras realistas

Mantenha a resposta concisa (máximo 200 palavras) e use emojis para tornar mais amigável.
"""
        
        # Conselho simulado como fallback
        conselho_simulado = f"""
📊 *Análise dos seus gastos:*

💰 Total: R$ {total:.2f}
🏆 Maior categoria: {max(expense_summary.items(), key=lambda x: x[1])[0].title()}

💡 *Dicas de economia:*
1. 🍽️ Considere cozinhar mais em casa
2. 🚗 Avalie caronas ou transporte público
3. 📱 Revise assinaturas e serviços

🎯 *Meta sugerida:* Reduza 10% dos gastos no próximo mês!
        """
        
        # Usar Gemini se disponível, senão usar resposta simulada
        if model and GEMINI_API_KEY:
            try:
                response = model.generate_content(prompt)
                conselho = response.text
            except Exception as e:
                conselho = f"⚠️ Erro ao gerar conselho com IA: {str(e)}\n\n" + conselho_simulado
        else:
            conselho = "⚠️ API do Gemini não configurada. Configure GEMINI_API_KEY no arquivo .env\n\n" + conselho_simulado
        
        return jsonify({
            'response': conselho,
            'type': 'advice'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@financeiro_bp.route('/relatorio', methods=['GET'])
def relatorio():
    """
    Endpoint para gerar relatório completo
    """
    try:
        expenses = get_all_expenses()
        total = get_total_expenses()
        
        if not expenses:
            return jsonify({
                'response': '📊 Nenhum gasto registrado ainda.',
                'data': []
            })
        
        # Agrupar por categoria
        categorias = {}
        for expense in expenses:
            categoria = expense['Categoria']
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append(expense)
        
        return jsonify({
            'total': total,
            'expenses': expenses,
            'categories': categorias,
            'count': len(expenses)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

