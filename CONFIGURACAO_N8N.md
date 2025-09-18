# Configuração do Assistente Financeiro WhatsApp no n8n

## 📋 Pré-requisitos

1. **n8n instalado e configurado**
2. **WhatsApp Business API** (Meta/Facebook)
3. **Seu backend Flask rodando** (com as APIs já implementadas)
4. **Variáveis de ambiente configuradas no n8n**

## 🔧 Variáveis de Ambiente no n8n

Configure as seguintes variáveis no n8n (Settings > Environment Variables):

```
API_BASE_URL=http://seu-servidor.com:5000
WHATSAPP_ACCESS_TOKEN=seu_token_de_acesso_whatsapp
WHATSAPP_PHONE_ID=seu_phone_number_id
GEMINI_API_KEY=sua_chave_da_api_gemini
```

## 📥 Como Importar o Fluxo

1. Abra o n8n
2. Clique em **"Import from file"** ou **"+"** → **"Import from file"**
3. Selecione o arquivo `n8n-assistente-financeiro-whatsapp.json`
4. Clique em **"Import"**

## 🔗 Configuração do Webhook WhatsApp

1. **URL do Webhook**: Após importar, copie a URL do webhook do nó "WhatsApp Webhook"
   - Exemplo: `https://seu-n8n.com/webhook/whatsapp-webhook`

2. **Configurar no Meta for Developers**:
   - Vá para [developers.facebook.com](https://developers.facebook.com)
   - Acesse seu app WhatsApp Business
   - Em **Webhooks**, adicione a URL copiada
   - Selecione os eventos: `messages`

## 🎯 Como Funciona o Fluxo

### 1. **Recebimento da Mensagem**
- Webhook recebe mensagem do WhatsApp
- Verifica se é mensagem de texto
- Extrai dados: número, texto, timestamp

### 2. **Processamento do Comando**
- **Registro de Gasto**: "Almoço 25.50 alimentação"
- **Consulta Diária**: "#dia"
- **Consulta Mensal**: "#mes"  
- **Conselho Financeiro**: "#conselho"
- **Ajuda**: "ajuda" ou "help"

### 3. **Integração com sua API**
- Chama os endpoints apropriados:
  - `POST /api/financeiro/registrar_gasto`
  - `POST /api/financeiro/consultar_gastos`
  - `POST /api/financeiro/gerar_conselho`
  - `POST /api/financeiro/ajuda`

### 4. **Resposta ao Usuário**
- Processa resposta da API
- Envia mensagem de volta pelo WhatsApp

## 🔍 Endpoints Utilizados

| Comando | Endpoint | Parâmetros |
|---------|----------|------------|
| Registro | `/api/financeiro/registrar_gasto` | `user_id`, `descricao`, `valor`, `categoria` |
| Consulta | `/api/financeiro/consultar_gastos` | `user_id`, `periodo` |
| Conselho | `/api/financeiro/gerar_conselho` | `user_id` |
| Ajuda | `/api/financeiro/ajuda` | `user_id` |

## 📱 Exemplos de Uso

### Registrar Gasto
```
Usuário: "Café da manhã 15.00 alimentação"
Bot: "✅ Gasto 'Café da manhã' no valor de R$ 15,00 registrado com sucesso!"
```

### Consultar Gastos
```
Usuário: "#dia"
Bot: "Seu total de gastos hoje é de R$ 45,50."

Usuário: "#mes"  
Bot: "Seu total de gastos neste mês é de R$ 1.234,56."
```

### Obter Conselho
```
Usuário: "#conselho"
Bot: "Com base nos seus gastos, sugiro reduzir os gastos com alimentação..."
```

## ⚠️ Tratamento de Erros

O fluxo inclui tratamento de erros para:
- Falhas na API
- Mensagens mal formatadas
- Problemas de conectividade
- Erros do WhatsApp Business API

## 🔧 Customizações Possíveis

### Adicionar Novos Comandos
1. Edite o nó **"Processar Mensagem"**
2. Adicione nova condição no **"Verificar Tipo de Comando"**
3. Crie novo nó HTTP Request para seu endpoint
4. Conecte ao fluxo principal

### Modificar Formatação das Respostas
- Edite o nó **"Preparar Resposta WhatsApp"**
- Adicione emojis, formatação, etc.

### Adicionar Validações
- Edite o nó **"Processar Mensagem"**
- Adicione validações para valores, categorias, etc.

## 🚀 Testando o Fluxo

1. **Teste Manual no n8n**:
   - Clique em "Test workflow"
   - Use dados de exemplo

2. **Teste via WhatsApp**:
   - Envie mensagem para seu número business
   - Verifique logs no n8n

3. **Verificar Logs**:
   - Veja execuções em "Executions"
   - Analise erros se houver

## 📊 Monitoramento

- **Execuções**: Monitore execuções bem-sucedidas/falhadas
- **Logs**: Verifique logs detalhados de cada nó
- **Performance**: Monitore tempo de resposta

## 🔒 Segurança

- Use HTTPS para todos os endpoints
- Valide tokens de acesso
- Implemente rate limiting se necessário
- Monitore uso da API

## 📞 Suporte

Se tiver problemas:
1. Verifique as variáveis de ambiente
2. Teste cada endpoint individualmente
3. Verifique logs do n8n
4. Valide configuração do WhatsApp Business API