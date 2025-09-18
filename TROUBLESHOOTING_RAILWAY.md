# 🚨 Guia de Solução de Problemas - Railway

## Problema Identificado: Conexão com PostgreSQL

### ❌ Erro nos Logs:
```
psycopg2.OperationalError: connection to server at "postgres.railway.internal" 
(fd12:f7a9:a3ad:0:a000:15:4143:97df), port 5432 failed: Connection timed out
```

## 🔧 Soluções Passo a Passo

### 1. Verificar se PostgreSQL está provisionado

**No painel do Railway:**
1. Acesse seu projeto
2. Verifique se há um serviço PostgreSQL ativo
3. Se não houver, clique em **"New"** → **"Database"** → **"PostgreSQL"**

### 2. Verificar Variáveis de Ambiente

**Variáveis necessárias:**
```bash
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=sua-chave-secreta-aleatoria
PORT=8080  # Opcional, Railway define automaticamente
```

**Como verificar:**
1. No Railway, vá em **"Variables"** ou **"Settings"**
2. Confirme se `DATABASE_URL` está presente
3. Se não estiver, o PostgreSQL não foi conectado corretamente

### 3. Conectar PostgreSQL ao seu serviço

**Se o PostgreSQL existe mas não está conectado:**
1. No seu serviço principal, vá em **"Settings"**
2. Procure por **"Service Variables"** ou **"Connect"**
3. Conecte o PostgreSQL ao seu serviço
4. O Railway criará automaticamente a `DATABASE_URL`

### 4. Testar Configuração Localmente

Execute o script de verificação:
```bash
python check_railway_config.py
```

### 5. Verificar Logs Detalhados

**Logs importantes para procurar:**
```bash
# Sucesso
✅ Banco de dados conectado e tabelas criadas com sucesso!

# Falha
❌ ERRO ao conectar com o banco de dados: [erro]
DATABASE_URL configurada: True/False
```

## 🚀 Comandos de Deploy

### Deploy Manual
```bash
# Fazer commit das alterações
git add .
git commit -m "fix: melhorar tratamento de erro de conexão DB"
git push origin main

# Railway fará deploy automaticamente
```

### Verificar Status
```bash
# Ver logs em tempo real
railway logs

# Verificar serviços
railway status
```

## 🔍 Debugging Adicional

### 1. Verificar se o PostgreSQL está rodando
No Railway, vá no serviço PostgreSQL e verifique:
- Status: **"Active"**
- Logs sem erros críticos

### 2. Testar conexão direta
```python
# Script de teste rápido
import os
from sqlalchemy import create_engine

url = os.environ.get('DATABASE_URL')
if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

engine = create_engine(url)
with engine.connect() as conn:
    print("✅ Conexão OK!")
```

### 3. Verificar configuração de rede
- Certifique-se que o PostgreSQL e a aplicação estão no mesmo projeto
- Verifique se não há configurações de firewall bloqueando

## 📋 Checklist de Verificação

- [ ] PostgreSQL provisionado no Railway
- [ ] DATABASE_URL presente nas variáveis de ambiente
- [ ] PostgreSQL conectado ao serviço principal
- [ ] Logs mostram tentativa de conexão
- [ ] Código tem tratamento de erro adequado
- [ ] Deploy mais recente foi feito após correções

## 🆘 Se Nada Funcionar

1. **Recriar PostgreSQL:**
   - Delete o serviço PostgreSQL atual
   - Crie um novo PostgreSQL
   - Reconecte ao serviço principal

2. **Verificar região:**
   - Certifique-se que todos os serviços estão na mesma região

3. **Contatar suporte Railway:**
   - Se problema persistir, pode ser issue de infraestrutura

## 📞 Próximos Passos

Após implementar as correções:
1. Faça deploy das alterações
2. Monitore os logs
3. Teste a aplicação
4. Verifique se as tabelas foram criadas no PostgreSQL