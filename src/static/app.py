# -*- coding: utf-8 -*-
import os
import requests
from flask import Flask, request, jsonify
import google.generativeai as genai
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# URL do nosso n8n (o "ramal do assistente")
N8N_WEBHOOK_URL = os.environ.get('N8N_WEBHOOK_URL', "https://n8n-production-5bbe.up.railway.app/webhook/gerente-ia")

# Inicialização da aplicação Flask
aplicacao = Flask(__name__)

# Configuração de CORS para permitir requisições do frontend
@aplicacao.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# --- Configuração do Cliente para a IA (Gemini) ---
try:
    # Pega a chave da variável de ambiente
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    if not GEMINI_API_KEY:
        logger.error("🚨 GEMINI_API_KEY não encontrada nas variáveis de ambiente")
        cliente_ia = None
    else:
        # Configura o Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        cliente_ia = genai.GenerativeModel('gemini-pro')
        logger.info("✅ Cliente de IA configurado para conversar com o Gemini.")
    
except Exception as e:
    logger.error(f"🚨 Erro ao configurar o cliente de IA: {e}")
    cliente_ia = None

# --- Prompt personalizado para a Prosper ---
PROMPT_PROSPER = """
Você é a Prosper, uma assistente de IA especializada em ajudar funcionários de uma empresa.

Suas funções principais:
- Responder dúvidas sobre trabalho e produtividade
- Dar orientações sobre processos empresariais
- Oferecer suporte motivacional e bem-estar no trabalho
- Ajudar com organização e planejamento de tarefas
- Esclarecer políticas da empresa
- Sugerir melhorias na rotina de trabalho

Características da sua personalidade:
- Sempre profissional, mas amigável e acolhedora
- Responda sempre em português brasileiro
- Use emojis ocasionalmente para tornar as respostas mais amigáveis
- Seja concisa mas completa nas suas respostas
- Mantenha um tom positivo e motivador

Instruções importantes:
- Se a pergunta for sobre problemas técnicos (hardware, software, impressoras, etc.), informe que um chamado será criado para o TI
- Para outras dúvidas, forneça uma resposta útil e prática
- Se não souber algo específico da empresa, seja honesta e sugira fontes alternativas
"""

# --- Lista expandida de palavras-chave técnicas ---
PALAVRAS_TECNICAS = [
    # Hardware
    "impressora", "computador", "notebook", "desktop", "mouse", "teclado", "monitor", 
    "cpu", "memória", "hd", "ssd", "cabo", "fonte", "cooler", "webcam",
    
    # Software
    "windows", "mac", "linux", "office", "excel", "word", "powerpoint", "outlook",
    "chrome", "firefox", "antivirus", "sistema", "programa", "aplicativo", "software",
    
    # Rede e Internet
    "internet", "wifi", "rede", "conexão", "ip", "dns", "roteador", "modem",
    "vpn", "firewall", "navegador", "email",
    
    # Problemas gerais
    "problema", "erro", "bug", "falha", "quebrou", "não funciona", "travou", 
    "lento", "devagar", "congelou", "parou", "crashed", "desligou", "reiniciou",
    "vírus", "malware", "hack", "senha", "login", "acesso negado",
    
    # Equipamentos
    "telefone", "ramal", "headset", "microfone", "scanner", "projetor",
    "tv", "tela", "display", "equipamento", "device", "dispositivo"
]

def eh_problema_tecnico(texto):
    """Verifica se o texto contém palavras relacionadas a problemas técnicos"""
    texto_lower = texto.lower()
    return any(palavra in texto_lower for palavra in PALAVRAS_TECNICAS)

# --- Nova função para criar um ticket usando o n8n ---
def criar_ticket_no_n8n(descricao_problema, usuario="Usuário"):
    """Esta função envia os dados para o webhook do n8n."""
    try:
        # O n8n espera receber os dados em formato JSON
        dados_para_n8n = {
            "descricao": descricao_problema,
            "usuario": usuario,
            "timestamp": datetime.now().isoformat(),
            "tipo": "suporte_tecnico"
        }
        
        logger.info(f"📋 Criando ticket para: {usuario} - {descricao_problema[:50]}...")
        
        # Faz a chamada POST para a URL do n8n
        resposta_n8n = requests.post(
            N8N_WEBHOOK_URL, 
            json=dados_para_n8n, 
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        # Verifica se a chamada para o n8n foi bem-sucedida
        if resposta_n8n.status_code == 200:
            logger.info("✅ Ticket criado com sucesso via n8n.")
            return True
        else:
            logger.error(f"🚨 Erro ao chamar o n8n: Status {resposta_n8n.status_code} - {resposta_n8n.text}")
            return False
            
    except requests.exceptions.Timeout:
        logger.error("🚨 Timeout ao chamar o n8n")
        return False
    except Exception as e:
        logger.error(f"🚨 Erro na função criar_ticket_no_n8n: {e}")
        return False

# --- Função para conversar com a IA ---
def conversar_com_ia(pergunta, usuario="Usuário"):
    """Conversa com o Gemini"""
    if not cliente_ia:
        return "Desculpe, o serviço de IA não está disponível no momento. Tente novamente mais tarde."
    
    try:
        # Monta o prompt completo
        prompt_completo = f"""{PROMPT_PROSPER}

Usuário: {usuario}
Pergunta: {pergunta}

Responda de forma útil e amigável:"""
        
        # Gera a resposta
        response = cliente_ia.generate_content(prompt_completo)
        
        if response.text:
            logger.info(f"✅ Resposta gerada pela IA para {usuario}")
            return response.text
        else:
            logger.error("🚨 IA retornou resposta vazia")
            return "Desculpe, não consegui gerar uma resposta adequada. Tente reformular sua pergunta."
            
    except Exception as e:
        logger.error(f"🚨 Erro ao comunicar com o Gemini: {e}")
        return "Desculpe, estou com dificuldades técnicas no momento. Tente novamente em alguns instantes."

# --- Endpoints ---

@aplicacao.route('/')
def home():
    return jsonify({
        "message": "Backend Prosper funcionando!",
        "status": "online",
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "ia_disponivel": cliente_ia is not None,
            "n8n_url": N8N_WEBHOOK_URL,
            "gemini_configured": GEMINI_API_KEY is not None
        }
    })

@aplicacao.route('/health')
def health():
    health_status = {
        "status": "healthy",
        "service": "Prosper Backend",
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "gemini_api": cliente_ia is not None,
            "environment": {
                "n8n_webhook": N8N_WEBHOOK_URL is not None,
                "gemini_key": GEMINI_API_KEY is not None
            }
        }
    }
    
    # Se algum serviço estiver indisponível, marca como degraded
    if not all([cliente_ia, N8N_WEBHOOK_URL, GEMINI_API_KEY]):
        health_status["status"] = "degraded"
    
    return jsonify(health_status)

# --- Endpoint principal (compatível com Typebot e n8n) ---
@aplicacao.route('/api/webhook', methods=['POST', 'OPTIONS'])
def webhook():
    """Endpoint principal para integração com Typebot e n8n"""
    
    # Lidar com preflight CORS
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"erro": "Dados não fornecidos"}), 400
        
        # Suporte para diferentes formatos de entrada
        descricao = data.get('descricao') or data.get('pergunta') or data.get('message') or ''
        usuario = data.get('usuario') or data.get('user') or data.get('name') or 'Usuário'
        
        if not descricao:
            return jsonify({
                "erro": "Descrição/pergunta é obrigatória",
                "resposta": "Por favor, me diga como posso ajudá-lo!"
            }), 400
        
        logger.info(f"🔗 Webhook recebido de {usuario}: {descricao[:100]}...")
        
        # Verifica se é um problema técnico
        if eh_problema_tecnico(descricao):
            sucesso_ticket = criar_ticket_no_n8n(descricao, usuario)
            
            if sucesso_ticket:
                resposta = f"Entendido, {usuario}! 🎫 Identifiquei que você tem um problema técnico. Criei um chamado para nossa equipe de TI. Eles entrarão em contato em breve para resolver sua questão."
                tipo = "ticket_criado"
            else:
                resposta = f"Olá, {usuario}! Identifiquei seu problema técnico, mas houve uma falha ao criar o chamado no sistema. Por favor, entre em contato diretamente com o suporte de TI ou tente novamente em alguns minutos."
                tipo = "erro_ticket"
        else:
            # Conversa normal com a IA
            resposta = conversar_com_ia(descricao, usuario)
            tipo = "resposta_ia"
        
        return jsonify({
            "resposta": resposta,
            "usuario": usuario,
            "tipo": tipo,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"🚨 Erro no webhook: {e}")
        return jsonify({
            "erro": "Erro interno do servidor",
            "resposta": "Desculpe, ocorreu um erro interno. Nossa equipe foi notificada e está trabalhando na correção."
        }), 500

# --- Endpoint adicional para compatibilidade ---
@aplicacao.route('/api/ask-local-ai', methods=['GET', 'POST'])
def perguntar_ia_local():
    """Endpoint alternativo para compatibilidade"""
    if not cliente_ia:
        return jsonify({
            "erro": "O cliente de IA não foi inicializado.",
            "resposta": "Serviço de IA temporariamente indisponível."
        }), 500

    # Pega a pergunta do request (GET ou POST)
    if request.method == 'GET':
        pergunta_usuario = request.args.get('pergunta')
        usuario = request.args.get('usuario', 'Usuário')
    else:
        data = request.get_json()
        pergunta_usuario = data.get('pergunta', '') if data else ''
        usuario = data.get('usuario', 'Usuário') if data else 'Usuário'

    if not pergunta_usuario:
        return jsonify({
            "erro": "O parâmetro 'pergunta' é obrigatório.",
            "resposta": "Por favor, faça sua pergunta!"
        }), 400

    logger.info(f"📝 Pergunta recebida de {usuario}: {pergunta_usuario}")

    # Verifica se é um problema técnico
    if eh_problema_tecnico(pergunta_usuario):
        sucesso_ticket = criar_ticket_no_n8n(pergunta_usuario, usuario)
        
        if sucesso_ticket:
            resposta = f"Entendido, {usuario}! 🎫 Abri um chamado para o seu problema técnico. A equipe de TI entrará em contato em breve para resolver a questão."
            tipo = "ticket_criado"
        else:
            resposta = "Entendi seu problema técnico, mas não consegui criar o chamado no sistema no momento. Por favor, tente novamente mais tarde ou entre em contato diretamente com o suporte."
            tipo = "erro_ticket"
    else:
        # Conversa com a IA
        resposta = conversar_com_ia(pergunta_usuario, usuario)
        tipo = "resposta_ia"
        
    return jsonify({
        "resposta": resposta,
        "tipo": tipo,
        "timestamp": datetime.now().isoformat()
    })

# --- Endpoint para testar conexão com n8n ---
@aplicacao.route('/api/test-n8n', methods=['GET'])
def testar_n8n():
    """Testa se o n8n está funcionando"""
    try:
        sucesso = criar_ticket_no_n8n("Teste de conexão automático", "Sistema de Monitoramento")
        
        if sucesso:
            return jsonify({
                "status": "success",
                "message": "Conexão com n8n funcionando perfeitamente!",
                "n8n_url": N8N_WEBHOOK_URL,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Erro ao conectar com n8n - verifique a URL e configurações",
                "n8n_url": N8N_WEBHOOK_URL,
                "timestamp": datetime.now().isoformat()
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao testar n8n: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

# --- Endpoint para testar IA ---
@aplicacao.route('/api/test-ai', methods=['GET'])
def testar_ia():
    """Testa se a IA está funcionando"""
    if not cliente_ia:
        return jsonify({
            "status": "error",
            "message": "IA não configurada - verifique GEMINI_API_KEY",
            "timestamp": datetime.now().isoformat()
        }), 500
    
    try:
        resposta = conversar_com_ia("Olá, você está funcionando?", "Sistema de Teste")
        return jsonify({
            "status": "success",
            "message": "IA funcionando perfeitamente!",
            "test_response": resposta,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao testar IA: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

# Ponto de entrada da aplicação
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"🚀 Iniciando Prosper Backend na porta {port}")
    logger.info(f"🔧 Debug mode: {debug}")
    logger.info(f"🤖 IA disponível: {cliente_ia is not None}")
    logger.info(f"🔗 N8N URL: {N8N_WEBHOOK_URL}")
    
    aplicacao.run(host='0.0.0.0', port=port, debug=debug)
