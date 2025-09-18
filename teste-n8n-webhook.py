#!/usr/bin/env python3
"""
Script de teste para o webhook do n8n do Assistente Financeiro WhatsApp
Este script simula mensagens do WhatsApp para testar o fluxo completo.
"""

import json
import requests
import time
from datetime import datetime

# Configurações
N8N_WEBHOOK_URL = "https://seu-n8n.com/webhook/whatsapp-webhook"  # Substitua pela sua URL
PHONE_NUMBER = "5511999887766"  # Número de teste

def criar_payload_whatsapp(message_text, phone_number=PHONE_NUMBER):
    """Cria payload simulando webhook do WhatsApp Business API"""
    timestamp = str(int(time.time()))
    message_id = f"wamid.test_{timestamp}"
    
    return {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "123456789",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15551234567",
                                "phone_number_id": "987654321"
                            },
                            "contacts": [
                                {
                                    "profile": {
                                        "name": "Usuário Teste"
                                    },
                                    "wa_id": phone_number
                                }
                            ],
                            "messages": [
                                {
                                    "from": phone_number,
                                    "id": message_id,
                                    "timestamp": timestamp,
                                    "text": {
                                        "body": message_text
                                    },
                                    "type": "text"
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }

def enviar_teste(message_text, descricao_teste):
    """Envia uma mensagem de teste para o webhook"""
    print(f"\n🧪 TESTE: {descricao_teste}")
    print(f"📱 Mensagem: '{message_text}'")
    print(f"⏰ Timestamp: {datetime.now().strftime('%H:%M:%S')}")
    
    payload = criar_payload_whatsapp(message_text)
    
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"body": payload},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"✅ Status: {response.status_code}")
        if response.text:
            print(f"📋 Resposta: {response.text[:200]}...")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro: {str(e)}")
    
    print("-" * 60)
    time.sleep(2)  # Pausa entre testes

def main():
    """Executa bateria de testes"""
    print("=" * 60)
    print("🚀 INICIANDO TESTES DO FLUXO N8N")
    print("=" * 60)
    
    # Verificar se a URL está configurada
    if "seu-n8n.com" in N8N_WEBHOOK_URL:
        print("❌ ERRO: Configure a URL do webhook n8n na variável N8N_WEBHOOK_URL")
        return
    
    # Bateria de testes
    testes = [
        ("ajuda", "Comando de Ajuda"),
        ("Café da manhã 15.50 alimentação", "Registro de Gasto - Alimentação"),
        ("Uber 25.00 transporte", "Registro de Gasto - Transporte"),
        ("Cinema 30.00 lazer", "Registro de Gasto - Lazer"),
        ("#dia", "Consulta Gastos do Dia"),
        ("#mes", "Consulta Gastos do Mês"),
        ("#conselho", "Solicitação de Conselho Financeiro"),
        ("help", "Comando Help (alternativo)"),
        ("Compras supermercado 85.75 alimentação", "Gasto Maior - Supermercado"),
        ("Gasolina 120.00 transporte", "Gasto Alto - Combustível")
    ]
    
    for mensagem, descricao in testes:
        enviar_teste(mensagem, descricao)
    
    print("🎉 TESTES CONCLUÍDOS!")
    print("\n📊 PRÓXIMOS PASSOS:")
    print("1. Verifique os logs no n8n (Executions)")
    print("2. Confirme se as mensagens foram processadas")
    print("3. Teste manualmente via WhatsApp")
    print("4. Monitore o banco de dados para novos registros")

def teste_individual():
    """Permite teste de mensagem individual"""
    print("\n🔧 MODO TESTE INDIVIDUAL")
    print("Digite 'sair' para terminar\n")
    
    while True:
        mensagem = input("📱 Digite a mensagem para testar: ").strip()
        
        if mensagem.lower() in ['sair', 'exit', 'quit']:
            break
            
        if not mensagem:
            continue
            
        enviar_teste(mensagem, "Teste Individual")

if __name__ == "__main__":
    import sys
    
    print("🤖 TESTADOR DO FLUXO N8N - ASSISTENTE FINANCEIRO")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--individual":
        teste_individual()
    else:
        main()
        
    print("\n👋 Obrigado por usar o testador!")