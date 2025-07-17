# 🚀 Guia Rápido de Configuração

## ⚡ Configuração em 5 Minutos

### 1. Preparar o Ambiente
```bash
cd agente_financeiro_whatsapp
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar API do Gemini
```bash
cp .env.example .env
# Editar .env e adicionar sua GEMINI_API_KEY
```

### 3. Iniciar o Servidor
```bash
python src/main.py
```

### 4. Testar Localmente
```bash
curl -X POST http://localhost:5000/api/financeiro/processar_mensagem \
  -H "Content-Type: application/json" \
  -d '{"message": "Almoço 25.50 alimentação"}'
```

## 🔗 Configuração n8n

### Workflow Básico:
1. **Webhook** → Recebe do WhatsApp
2. **HTTP Request** → Envia para `http://seu-servidor:5000/api/financeiro/processar_mensagem`
3. **HTTP Request** → Envia resposta de volta ao WhatsApp

### Endpoints Principais:
- `POST /api/financeiro/processar_mensagem` - Processa mensagens
- `POST /api/financeiro/gerar_conselho` - Gera conselhos
- `GET /api/financeiro/relatorio` - Relatório completo

## 📱 Como Usar

### Registrar Gastos:
```
Almoço 25.50 alimentação
Gasolina 80 transporte
Cinema 30.00 lazer
```

### Comandos:
- `total` - Ver total gasto
- `conselho` - Receber dicas de economia
- `ajuda` - Ver instruções

## 🔧 Troubleshooting Rápido

### Erro numpy/pandas:
```bash
pip install --upgrade numpy pandas
```

### API Gemini não funciona:
- Verificar se GEMINI_API_KEY está no .env
- Testar API key no Google AI Studio

### Servidor não responde:
- Verificar se está rodando: `ps aux | grep python`
- Verificar logs: `tail -f server.log`

## 📞 Suporte

Para dúvidas, consulte o README.md completo ou entre em contato.

