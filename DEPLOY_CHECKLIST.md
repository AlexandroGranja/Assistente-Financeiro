# ✅ Checklist de Deploy - Assistente Financeiro WhatsApp

## 🎯 Arquivos Criados

### ✅ Fluxo n8n
- `n8n-assistente-financeiro-whatsapp.json` - Fluxo completo para importar no n8n
- `CONFIGURACAO_N8N.md` - Guia detalhado de configuração
- `exemplo-webhook-whatsapp.json` - Exemplos de payloads para teste

### ✅ Scripts e Configuração
- `run.sh` - Script de inicialização da aplicação
- `teste-n8n-webhook.py` - Script para testar o webhook
- `Dockerfile` - Atualizado para usar Python 3.11 e run.sh
- `requirements.txt` - Dependências atualizadas e compatíveis

### ✅ Documentação
- `README.md` - Documentação completa do projeto
- `DEPLOY_CHECKLIST.md` - Este checklist

## 🚀 Próximos Passos

### 1. Corrigir Deploy no Railway
```bash
# 1. Faça commit dos novos arquivos
git add .
git commit -m "Fix: Adicionar run.sh e corrigir Dockerfile"
git push origin main

# 2. O Railway fará redeploy automaticamente
# 3. Verifique se não há mais erros de build
```

### 2. Configurar n8n
```bash
# 1. Importe o arquivo JSON no n8n
# 2. Configure as variáveis de ambiente:
API_BASE_URL=https://seu-projeto.railway.app
WHATSAPP_ACCESS_TOKEN=seu_token_aqui
WHATSAPP_PHONE_ID=seu_phone_id_aqui

# 3. Ative o fluxo
# 4. Copie a URL do webhook
```

### 3. Configurar WhatsApp Business API
```bash
# 1. Acesse Meta for Developers
# 2. Configure webhook com URL do n8n
# 3. Selecione evento 'messages'
# 4. Teste a verificação do webhook
```

### 4. Testar Sistema Completo
```bash
# 1. Execute o script de teste (após configurar URL)
python3 teste-n8n-webhook.py

# 2. Teste via WhatsApp real
# 3. Monitore logs no n8n e Railway
```

## 🔧 Variáveis de Ambiente

### Railway (Backend)
```env
GEMINI_API_KEY=sua_chave_gemini
DATABASE_URL=postgresql://... (opcional)
PORT=8080
```

### n8n (Automação)
```env
API_BASE_URL=https://seu-projeto.railway.app
WHATSAPP_ACCESS_TOKEN=token_do_meta
WHATSAPP_PHONE_ID=id_do_telefone
```

## 📋 Comandos de Teste

Após configurar tudo, teste estes comandos via WhatsApp:

1. `ajuda` - Deve retornar menu de ajuda
2. `Café 15.50 alimentação` - Deve registrar gasto
3. `#dia` - Deve mostrar gastos do dia
4. `#mes` - Deve mostrar gastos do mês
5. `#conselho` - Deve gerar conselho com IA

## 🐛 Possíveis Problemas e Soluções

### ❌ Build falha no Railway
**Problema**: `chmod: cannot access 'run.sh': No such file or directory`
**Solução**: ✅ Já corrigido - arquivo `run.sh` criado

### ❌ n8n não recebe webhooks
**Problema**: WhatsApp não envia mensagens para n8n
**Solução**: 
1. Verificar URL do webhook
2. Confirmar token de verificação
3. Testar com `teste-n8n-webhook.py`

### ❌ API não responde
**Problema**: n8n não consegue chamar backend
**Solução**:
1. Verificar `API_BASE_URL` no n8n
2. Confirmar se Railway está rodando
3. Testar endpoints diretamente

### ❌ Gemini não gera conselhos
**Problema**: Erro na geração de conselhos
**Solução**:
1. Verificar `GEMINI_API_KEY`
2. Confirmar quota da API
3. Testar com poucos gastos primeiro

## 🎯 Ordem de Execução

1. ✅ **Deploy Backend** (Railway)
2. ⏳ **Configurar n8n** (Importar fluxo)
3. ⏳ **Configurar WhatsApp** (Meta for Developers)
4. ⏳ **Testar Sistema** (Scripts + manual)
5. ⏳ **Monitorar Logs** (n8n + Railway)

## 📊 Métricas de Sucesso

- ✅ Build do Railway sem erros
- ✅ n8n recebe webhooks do WhatsApp
- ✅ Backend processa requisições
- ✅ Respostas chegam no WhatsApp
- ✅ Dados são salvos no banco
- ✅ IA gera conselhos relevantes

---

**🚀 Seu assistente financeiro está quase pronto!**

Siga este checklist passo a passo e você terá um sistema completo funcionando.