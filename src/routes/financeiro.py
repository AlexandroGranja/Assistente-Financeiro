{
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "a4b1c2d3-e4f5-g6h7-i8j9-k0l1m2n3o4p5",
        "options": {}
      },
      "id": "def70352-c9af-40a2-992a-bf2fc8279fba",
      "name": "1. Recebe do WhatsApp",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        -380,
        160
      ]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $('1. Recebe do WhatsApp').item.json.body.data.key.remoteJid }}",
              "operation": "endsWith",
              "value2": "@s.whatsapp.net"
            }
          ]
        }
      },
      "id": "2d426452-72f7-4d97-84f3-10465799d51c",
      "name": "2. É Contato Individual?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [
        -140,
        160
      ]
    },
    {
      "parameters": {
        "url": "https://assistente-financeiro-production.up.railway.app/api/financeiro/registrar_gasto",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "descricao",
              "value": "={{ $('4. Extrai JSON da Resposta').item.json.descricao }}"
            },
            {
              "name": "valor",
              "value": "={{ $('4. Extrai JSON da Resposta').item.json.valor }}"
            },
            {
              "name": "categoria",
              "value": "={{ $('4. Extrai JSON da Resposta').item.json.categoria }}"
            },
            {
              "name": "user_id",
              "value": "={{ $('1. Recebe do WhatsApp').item.json.body.data.key.remoteJid.split('@')[0] }}"
            }
          ]
        },
        "options": {}
      },
      "id": "5bddf751-3948-490d-aafe-cd8cd551ebb7",
      "name": "5. Envia para o Backend",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [
        580,
        60
      ]
    },
    {
      "parameters": {
        "resource": "messages-api",
        "instanceName": "teste",
        "remoteJid": "={{ $('1. Recebe do WhatsApp').item.json.body.data.key.remoteJid }}",
        "messageText": "={{ $('5. Envia para o Backend').item.json.message }}",
        "options_message": {}
      },
      "id": "67b12c85-b9b0-4bfd-a5fb-edf14d56c66e",
      "name": "6. Envia Resposta (WhatsApp)",
      "type": "n8n-nodes-evolution-api.evolutionApi",
      "typeVersion": 1,
      "position": [
        820,
        60
      ],
      "credentials": {
        "evolutionApi": {
          "id": "SoqZJgqidLMClr2b",
          "name": "Evolution account"
        }
      }
    },
    {
      "parameters": {
        "model": "gemini-1.5-flash",
        "prompt": "Analise a frase a seguir e retorne APENAS um objeto JSON com as chaves \"descricao\", \"valor\" e \"categoria\".\n- \"descricao\": Um resumo do gasto.\n- \"valor\": O custo numérico, usando ponto como separador decimal.\n- \"categoria\": Uma das seguintes: Alimentação, Transporte, Lazer, Moradia, Saúde, Educação, Outros.\n\nFrase: \"{{ $('1. Recebe do WhatsApp').item.json.body.data.message.conversation || $('1. Recebe do WhatsApp').item.json.body.data.message.extendedTextMessage.text }}\"",
        "options": {}
      },
      "id": "a9a3f9e2-5c96-41f3-80b1-3e4e6b12c47d",
      "name": "3. Processa com IA",
      "type": "n8n-nodes-base.googleGemini",
      "typeVersion": 1,
      "position": [
        100,
        60
      ],
      "credentials": {
        "googleApi": {
          "id": "YOUR_CREDENTIAL_ID",
          "name": "Google AI Credentials"
        }
      }
    },
    {
      "parameters": {
        "mode": "json",
        "json": "={{ $json.text.match(/\\{.*\\}/s)[0] }}",
        "options": {}
      },
      "id": "9d9e6f2b-8a1c-4b5d-9f3e-7c8d9a0b1c2d",
      "name": "4. Extrai JSON da Resposta",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [
        340,
        60
      ]
    }
  ],
  "connections": {
    "1. Recebe do WhatsApp": {
      "main": [
        [
          {
            "node": "2. É Contato Individual?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "2. É Contato Individual?": {
      "main": [
        [
          {
            "node": "3. Processa com IA",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "3. Processa com IA": {
      "main": [
        [
          {
            "node": "4. Extrai JSON da Resposta",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "4. Extrai JSON da Resposta": {
      "main": [
        [
          {
            "node": "5. Envia para o Backend",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "5. Envia para o Backend": {
      "main": [
        [
          {
            "node": "6. Envia Resposta (WhatsApp)",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
