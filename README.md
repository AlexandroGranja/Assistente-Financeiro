# 🤖 Agente Financeiro IA para WhatsApp

Um sistema inteligente de controle financeiro pessoal que funciona diretamente no WhatsApp, desenvolvido para automatizar o registro de gastos, calcular totais e fornecer conselhos personalizados de economia usando Google Gemini.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Funcionalidades](#funcionalidades)
3. [Arquitetura do Sistema](#arquitetura-do-sistema)
4. [Configuração e Instalação](#configuração-e-instalação)
5. [Integração com n8n](#integração-com-n8n)
6. [Configuração do Google Gemini](#configuração-do-google-gemini)
7. [Como Usar](#como-usar)
8. [Endpoints da API](#endpoints-da-api)
9. [Deploy e Produção](#deploy-e-produção)
10. [Troubleshooting](#troubleshooting)

## 🎯 Visão Geral

Este projeto implementa um agente de IA financeiro que opera através do WhatsApp, permitindo aos usuários registrar gastos de forma natural e receber insights inteligentes sobre seus hábitos de consumo. O sistema utiliza Flask como backend, pandas para manipulação de dados em Excel, e Google Gemini para geração de conselhos personalizados.

### Principais Benefícios

- **Simplicidade**: Registre gastos enviando mensagens simples no WhatsApp
- **Inteligência**: Receba conselhos personalizados baseados em seus padrões de gasto
- **Automação**: Integração completa com n8n para fluxos automatizados
- **Flexibilidade**: Sistema modular e facilmente extensível

## ⚡ Funcionalidades

### 📝 Registro de Gastos
- Formato natural: "Almoço 25.50 alimentação"
- Categorização automática
- Armazenamento em planilha Excel
- Validação de dados

### 💰 Comandos Disponíveis
- `total` - Visualizar total gasto
- `conselho` - Receber dicas de economia personalizadas
- `ajuda` - Exibir instruções de uso

### 🧠 Inteligência Artificial
- Análise de padrões de gasto
- Conselhos personalizados via Google Gemini
- Identificação de categorias com maior impacto
- Sugestões de metas financeiras

### 📊 Relatórios
- Resumo por categorias
- Análise de tendências
- Exportação de dados



## 🏗️ Arquitetura do Sistema

O sistema é composto por três camadas principais que trabalham em conjunto para fornecer uma experiência fluida e inteligente de controle financeiro.

### Camada de Comunicação (WhatsApp + n8n)

A camada de comunicação é responsável por receber mensagens do WhatsApp e encaminhá-las para o processamento. O n8n atua como orquestrador, capturando mensagens do WhatsApp Business API e enviando-as para os endpoints apropriados do sistema Flask.

**Fluxo de Comunicação:**
1. Usuário envia mensagem no WhatsApp
2. WhatsApp Business API recebe a mensagem
3. n8n captura via webhook
4. n8n processa e envia para Flask API
5. Flask processa e retorna resposta
6. n8n envia resposta de volta ao WhatsApp

### Camada de Processamento (Flask API)

O backend Flask é o cérebro do sistema, responsável por interpretar mensagens, gerenciar dados e coordenar com serviços externos. A arquitetura modular permite fácil manutenção e extensão.

**Componentes Principais:**
- **Parser de Mensagens**: Interpreta comandos e dados de gastos
- **Gerenciador de Dados**: Interface com planilha Excel
- **Integração IA**: Comunicação com Google Gemini
- **Sistema de Respostas**: Formatação de mensagens de retorno

### Camada de Dados (Excel + IA)

A persistência de dados utiliza planilhas Excel para simplicidade e compatibilidade, enquanto a inteligência artificial fornece insights avançados baseados nos dados coletados.

**Estrutura de Dados:**
- **Data**: Timestamp do gasto
- **Descrição**: Descrição livre do gasto
- **Valor**: Valor monetário
- **Categoria**: Classificação do tipo de gasto

### Fluxo de Dados Completo

```
WhatsApp → n8n → Flask API → Excel/Gemini → Flask API → n8n → WhatsApp
```

Este fluxo garante que todas as interações sejam processadas de forma consistente e que os dados sejam mantidos íntegros ao longo de todo o processo.

## 🛠️ Configuração e Instalação

### Pré-requisitos

Antes de iniciar a instalação, certifique-se de ter os seguintes componentes disponíveis em seu ambiente:

- **Python 3.11+**: Linguagem principal do projeto
- **n8n**: Plataforma de automação para integração WhatsApp
- **WhatsApp Business API**: Acesso à API oficial do WhatsApp
- **Google Gemini API**: Chave de acesso para serviços de IA
- **Git**: Para clonagem e versionamento do código

### Instalação Passo a Passo

#### 1. Clonagem e Preparação do Ambiente

```bash
# Clone o repositório (ou extraia os arquivos fornecidos)
cd /caminho/para/seu/projeto
cp -r agente_financeiro_whatsapp /seu/diretorio/destino
cd /seu/diretorio/destino/agente_financeiro_whatsapp

# Ative o ambiente virtual
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

#### 2. Configuração de Variáveis de Ambiente

Crie um arquivo `.env` baseado no exemplo fornecido:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
# Configurações do Google Gemini
GEMINI_API_KEY=sua_api_key_do_gemini_aqui

# Configurações do Flask
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_aqui
```

#### 3. Inicialização da Planilha

O sistema criará automaticamente a planilha `gastos.xlsx` na primeira execução. Para inicializar manualmente:

```bash
python -c "from src.excel_handler import initialize_excel; initialize_excel()"
```

#### 4. Teste Local

Execute o servidor Flask para verificar se tudo está funcionando:

```bash
python src/main.py
```

O servidor estará disponível em `http://localhost:5000`. Você pode testar os endpoints usando curl ou ferramentas similares.


## 🔗 Integração com n8n

O n8n é fundamental para conectar o WhatsApp ao sistema Flask. Esta seção detalha como configurar um workflow completo no n8n para automatizar todo o fluxo de comunicação.

### Configuração do Workflow n8n

#### 1. Webhook de Entrada (WhatsApp)

Configure um webhook no n8n para receber mensagens do WhatsApp Business API:

**Configurações do Webhook:**
- **URL**: `https://seu-n8n.com/webhook/whatsapp-financeiro`
- **Método**: POST
- **Autenticação**: Conforme sua configuração do WhatsApp Business

**Estrutura de Dados Esperada:**
```json
{
  "from": "5511999999999",
  "message": "Almoço 25.50 alimentação",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 2. Processamento de Mensagem

Adicione um nó HTTP Request para enviar a mensagem para o Flask:

**Configurações HTTP Request:**
- **URL**: `http://seu-servidor-flask:5000/api/financeiro/processar_mensagem`
- **Método**: POST
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
  "message": "{{ $json.message }}"
}
```

#### 3. Tratamento de Respostas

Configure condicionais para tratar diferentes tipos de resposta:

**Tipos de Resposta:**
- `help`: Mensagem de ajuda
- `total`: Resultado de totalização
- `expense_added`: Confirmação de gasto registrado
- `conselho`: Solicitação de conselho (requer chamada adicional)
- `error`: Mensagem de erro

#### 4. Geração de Conselhos

Para o comando "conselho", adicione uma chamada adicional:

**Configurações para Conselho:**
- **URL**: `http://seu-servidor-flask:5000/api/financeiro/gerar_conselho`
- **Método**: POST
- **Trigger**: Quando `type === 'conselho'`

#### 5. Envio de Resposta

Configure o nó final para enviar a resposta de volta ao WhatsApp:

**Configurações de Envio:**
- **Destinatário**: `{{ $json.from }}`
- **Mensagem**: `{{ $json.response }}`
- **Formato**: Texto (suporte a markdown)

### Exemplo de Workflow Completo

```json
{
  "nodes": [
    {
      "name": "WhatsApp Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "whatsapp-financeiro",
        "httpMethod": "POST"
      }
    },
    {
      "name": "Processar Mensagem",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:5000/api/financeiro/processar_mensagem",
        "method": "POST",
        "jsonParameters": true,
        "options": {
          "bodyContentType": "json"
        }
      }
    },
    {
      "name": "Verificar Tipo",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.type }}",
              "operation": "equal",
              "value2": "conselho"
            }
          ]
        }
      }
    },
    {
      "name": "Gerar Conselho",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:5000/api/financeiro/gerar_conselho",
        "method": "POST"
      }
    },
    {
      "name": "Enviar Resposta",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.whatsapp.com/send",
        "method": "POST"
      }
    }
  ]
}
```

### Configurações Avançadas

#### Rate Limiting

Implemente limitação de taxa para evitar spam:

```javascript
// Código JavaScript no n8n
const userId = $json.from;
const now = Date.now();
const lastMessage = $workflow.getStaticData('lastMessage') || {};

if (lastMessage[userId] && (now - lastMessage[userId]) < 2000) {
  return []; // Bloqueia mensagens muito frequentes
}

lastMessage[userId] = now;
$workflow.setStaticData('lastMessage', lastMessage);
return [$json];
```

#### Logging e Monitoramento

Configure logs para monitorar o uso:

```javascript
// Log de atividade
console.log(`Usuário ${$json.from} enviou: ${$json.message}`);

// Métricas básicas
const stats = $workflow.getStaticData('stats') || { total: 0, today: 0 };
stats.total++;
stats.today++;
$workflow.setStaticData('stats', stats);
```


## 🧠 Configuração do Google Gemini

O Google Gemini é responsável por gerar conselhos personalizados de economia baseados nos padrões de gasto do usuário. Esta seção detalha como obter e configurar a API key necessária.

### Obtendo a API Key do Google Gemini

#### 1. Acesso ao Google AI Studio

Acesse o Google AI Studio através do link oficial:
- **URL**: https://makersuite.google.com/app/apikey
- **Requisitos**: Conta Google ativa
- **Disponibilidade**: Verifique se o serviço está disponível em sua região

#### 2. Criação da API Key

No Google AI Studio, siga os seguintes passos:

1. **Login**: Faça login com sua conta Google
2. **Criar Projeto**: Se necessário, crie um novo projeto
3. **Gerar API Key**: Clique em "Create API Key"
4. **Configurar Limites**: Defina limites de uso conforme necessário
5. **Copiar Chave**: Salve a API key em local seguro

#### 3. Configuração no Sistema

Adicione a API key ao arquivo `.env`:

```env
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Importante**: Nunca compartilhe sua API key ou a inclua em repositórios públicos.

### Personalização dos Prompts

O sistema utiliza prompts estruturados para gerar conselhos relevantes. Você pode personalizar esses prompts editando o arquivo `src/routes/financeiro.py`:

#### Prompt Base para Conselhos

```python
prompt = f"""
Você é um consultor financeiro especializado em economia doméstica. Analise os seguintes gastos e forneça conselhos práticos e personalizados:

RESUMO DOS GASTOS:
Total gasto: R$ {total:.2f}

Gastos por categoria:
{categoria_detalhes}

Por favor, forneça:
1. Uma análise dos padrões de gasto
2. 3 dicas específicas de economia baseadas nos dados
3. Sugestões de metas financeiras realistas

Mantenha a resposta concisa (máximo 200 palavras) e use emojis para tornar mais amigável.
"""
```

#### Customizações Avançadas

Para personalizar ainda mais os conselhos, você pode:

**Adicionar Contexto Temporal:**
```python
# Análise por período
if len(expenses) > 30:
    prompt += "\nConsidere que estes são gastos dos últimos 30 dias."
```

**Incluir Metas Específicas:**
```python
# Metas baseadas em perfil
if total > 1000:
    prompt += "\nO usuário tem gastos elevados, foque em economia significativa."
else:
    prompt += "\nO usuário tem gastos moderados, sugira otimizações pontuais."
```

**Personalizar por Categoria:**
```python
# Foco em categorias específicas
maior_categoria = max(expense_summary.items(), key=lambda x: x[1])
prompt += f"\nDê atenção especial à categoria {maior_categoria[0]} que representa o maior gasto."
```

### Monitoramento de Uso da API

Implemente monitoramento para controlar o uso da API Gemini:

```python
import time
from datetime import datetime

class GeminiUsageTracker:
    def __init__(self):
        self.daily_requests = 0
        self.last_reset = datetime.now().date()
    
    def track_request(self):
        today = datetime.now().date()
        if today != self.last_reset:
            self.daily_requests = 0
            self.last_reset = today
        
        self.daily_requests += 1
        
        # Limite diário (ajuste conforme seu plano)
        if self.daily_requests > 100:
            raise Exception("Limite diário de requests atingido")
```

### Fallback para Indisponibilidade

O sistema inclui respostas de fallback caso a API do Gemini esteja indisponível:

```python
def generate_fallback_advice(total, categories):
    """Gera conselho básico sem usar IA"""
    maior_categoria = max(categories.items(), key=lambda x: x[1])
    
    return f"""
📊 *Análise dos seus gastos:*

💰 Total: R$ {total:.2f}
🏆 Maior categoria: {maior_categoria[0].title()}

💡 *Dicas de economia:*
1. 🍽️ Considere cozinhar mais em casa
2. 🚗 Avalie caronas ou transporte público
3. 📱 Revise assinaturas e serviços

🎯 *Meta sugerida:* Reduza 10% dos gastos no próximo mês!
    """
```

## 📱 Como Usar

Esta seção fornece um guia completo sobre como interagir com o agente financeiro através do WhatsApp, incluindo exemplos práticos e dicas de uso.

### Comandos Básicos

#### Registrar Gastos

Para registrar um gasto, envie uma mensagem no formato:
```
[descrição] [valor] [categoria]
```

**Exemplos Válidos:**
- `Almoço 25.50 alimentação`
- `Gasolina 80 transporte`
- `Cinema 30.00 lazer`
- `Farmácia 45.90 saúde`
- `Supermercado 120.75 alimentação`

**Formatos de Valor Aceitos:**
- `25.50` (com ponto decimal)
- `25,50` (com vírgula decimal)
- `25` (valor inteiro)

**Categorias Sugeridas:**
- `alimentação` - Refeições, supermercado, delivery
- `transporte` - Combustível, transporte público, Uber
- `lazer` - Cinema, restaurantes, viagens
- `saúde` - Farmácia, consultas, exames
- `educação` - Cursos, livros, material escolar
- `casa` - Contas, manutenção, móveis
- `roupas` - Vestuário e acessórios
- `outros` - Gastos diversos

#### Consultar Total

Para ver o total gasto, envie:
```
total
```

**Resposta Esperada:**
```
💰 Total gasto: R$ 1.247,50
```

#### Solicitar Conselhos

Para receber dicas personalizadas, envie:
```
conselho
```

**Exemplo de Resposta:**
```
📊 Análise dos seus gastos:

💰 Total: R$ 1.247,50
🏆 Maior categoria: Alimentação (45% dos gastos)

💡 Dicas personalizadas:
1. 🍽️ Seus gastos com alimentação estão altos. Considere cozinhar mais em casa - pode economizar até R$ 200/mês
2. 🚗 Transporte representa 25% dos gastos. Avalie caronas ou transporte público para trajetos regulares
3. 📱 Revise assinaturas de streaming e apps - pequenos valores somam muito ao longo do mês

🎯 Meta sugerida: Reduza 15% dos gastos com alimentação no próximo mês (economia de ~R$ 85)
```

#### Obter Ajuda

Para ver todas as opções disponíveis, envie:
```
ajuda
```

### Exemplos de Conversas Completas

#### Cenário 1: Primeiro Uso

**Usuário:** `ajuda`

**Bot:** 
```
🤖 Agente Financeiro IA

📝 Como registrar gastos:
Digite: [descrição] [valor] [categoria]
Exemplo: Almoço 25.50 alimentação

💰 Comandos disponíveis:
• total - Ver total gasto
• conselho - Receber dicas de economia
• ajuda - Ver esta mensagem

📊 Categorias sugeridas:
alimentação, transporte, lazer, saúde, educação, casa, roupas, outros
```

**Usuário:** `Café da manhã 12.50 alimentação`

**Bot:**
```
✅ Gasto registrado!
💸 Café da manhã: R$ 12,50
🏷️ Categoria: alimentação
```

#### Cenário 2: Uso Avançado

**Usuário:** `Uber 25.00 transporte`

**Bot:**
```
✅ Gasto registrado!
💸 Uber: R$ 25,00
🏷️ Categoria: transporte
```

**Usuário:** `total`

**Bot:**
```
💰 Total gasto: R$ 37,50
```

**Usuário:** `conselho`

**Bot:**
```
📊 Análise dos seus gastos:

💰 Total: R$ 37,50
🏆 Maior categoria: Transporte

💡 Dicas de economia:
1. 🚗 Para trajetos curtos, considere caminhar ou usar bicicleta
2. 🍽️ Continue controlando gastos com alimentação
3. 📊 Registre mais gastos para análises mais precisas

🎯 Meta sugerida: Mantenha o controle diário dos gastos!
```

### Dicas de Uso Eficiente

#### Consistência na Categorização

Mantenha consistência ao categorizar gastos:
- Use sempre as mesmas palavras para categorias similares
- Prefira categorias amplas a muito específicas
- Exemplo: use "alimentação" em vez de "comida", "food", "refeição"

#### Registro Imediato

Para melhor controle financeiro:
- Registre gastos imediatamente após realizá-los
- Use o WhatsApp como um "diário financeiro"
- Aproveite momentos de espera para registrar gastos pendentes

#### Análise Regular

Estabeleça uma rotina de análise:
- Consulte o total semanalmente
- Solicite conselhos mensalmente
- Use os insights para ajustar comportamentos

#### Categorias Personalizadas

Adapte as categorias ao seu estilo de vida:
- Profissionais autônomos: adicione "trabalho"
- Estudantes: use "educação" com frequência
- Famílias: considere "filhos" como categoria

### Limitações e Considerações

#### Formato de Mensagem

O sistema é sensível ao formato. Certifique-se de:
- Separar descrição, valor e categoria com espaços
- Usar pontos ou vírgulas para decimais
- Evitar caracteres especiais na descrição

#### Privacidade dos Dados

Lembre-se de que:
- Dados são armazenados localmente na planilha
- Mensagens são processadas pelo sistema
- Conselhos são gerados usando IA externa (Gemini)

#### Backup Regular

Recomenda-se:
- Fazer backup regular da planilha `gastos.xlsx`
- Exportar dados periodicamente
- Manter cópias de segurança em local seguro


## 🔌 Endpoints da API

O sistema Flask expõe uma API RESTful que pode ser integrada com diferentes plataformas além do WhatsApp. Esta seção documenta todos os endpoints disponíveis com exemplos práticos de uso.

### Base URL

```
http://localhost:5000/api/financeiro
```

Para produção, substitua `localhost:5000` pelo seu domínio e porta configurados.

### Autenticação

Atualmente, o sistema não implementa autenticação. Para uso em produção, considere adicionar:
- API Keys
- JWT Tokens
- OAuth 2.0
- Rate Limiting por IP

### Endpoints Disponíveis

#### 1. Processar Mensagem

**Endpoint:** `POST /processar_mensagem`

**Descrição:** Endpoint principal que processa mensagens de texto e executa ações baseadas no conteúdo.

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "message": "string"
}
```

**Exemplos de Requisição:**

**Registrar Gasto:**
```bash
curl -X POST http://localhost:5000/api/financeiro/processar_mensagem \
  -H "Content-Type: application/json" \
  -d '{"message": "Almoço 25.50 alimentação"}'
```

**Resposta:**
```json
{
  "response": "✅ Gasto registrado!\n💸 Almoço: R$ 25.50\n🏷️ Categoria: alimentação",
  "type": "expense_added",
  "data": {
    "descricao": "Almoço",
    "valor": 25.50,
    "categoria": "alimentação",
    "data": "2024-01-15"
  }
}
```

**Consultar Total:**
```bash
curl -X POST http://localhost:5000/api/financeiro/processar_mensagem \
  -H "Content-Type: application/json" \
  -d '{"message": "total"}'
```

**Resposta:**
```json
{
  "response": "💰 Total gasto: R$ 1.247.50",
  "type": "total"
}
```

**Solicitar Ajuda:**
```bash
curl -X POST http://localhost:5000/api/financeiro/processar_mensagem \
  -H "Content-Type: application/json" \
  -d '{"message": "ajuda"}'
```

**Resposta:**
```json
{
  "response": "🤖 *Agente Financeiro IA*\n\n📝 *Como registrar gastos:*\nDigite: [descrição] [valor] [categoria]\nExemplo: Almoço 25.50 alimentação\n\n💰 *Comandos disponíveis:*\n• `total` - Ver total gasto\n• `conselho` - Receber dicas de economia\n• `ajuda` - Ver esta mensagem\n\n📊 *Categorias sugeridas:*\nalimentação, transporte, lazer, saúde, educação, casa, roupas, outros",
  "type": "help"
}
```

**Códigos de Status:**
- `200`: Sucesso
- `400`: Mensagem vazia ou formato inválido
- `500`: Erro interno do servidor

#### 2. Gerar Conselho

**Endpoint:** `POST /gerar_conselho`

**Descrição:** Gera conselhos personalizados usando Google Gemini baseado nos gastos registrados.

**Headers:**
```
Content-Type: application/json
```

**Body:** Não requer body (usa dados da planilha)

**Exemplo de Requisição:**
```bash
curl -X POST http://localhost:5000/api/financeiro/gerar_conselho \
  -H "Content-Type: application/json"
```

**Resposta com Gemini Configurado:**
```json
{
  "response": "📊 *Análise dos seus gastos:*\n\n💰 Total: R$ 1.247,50\n🏆 Maior categoria: Alimentação (45% dos gastos)\n\n💡 *Dicas personalizadas:*\n1. 🍽️ Seus gastos com alimentação estão altos. Considere cozinhar mais em casa\n2. 🚗 Transporte representa 25% dos gastos. Avalie alternativas mais econômicas\n3. 📱 Revise assinaturas mensais que podem estar passando despercebidas\n\n🎯 *Meta sugerida:* Reduza 15% dos gastos com alimentação no próximo mês",
  "type": "advice"
}
```

**Resposta sem Gemini:**
```json
{
  "response": "⚠️ API do Gemini não configurada. Configure GEMINI_API_KEY no arquivo .env\n\n📊 *Análise dos seus gastos:*\n\n💰 Total: R$ 1.247,50\n🏆 Maior categoria: Alimentação\n\n💡 *Dicas de economia:*\n1. 🍽️ Considere cozinhar mais em casa\n2. 🚗 Avalie caronas ou transporte público\n3. 📱 Revise assinaturas e serviços\n\n🎯 *Meta sugerida:* Reduza 10% dos gastos no próximo mês!",
  "type": "advice"
}
```

**Códigos de Status:**
- `200`: Sucesso
- `500`: Erro interno do servidor

#### 3. Relatório Completo

**Endpoint:** `GET /relatorio`

**Descrição:** Retorna relatório completo com todos os gastos e estatísticas.

**Exemplo de Requisição:**
```bash
curl -X GET http://localhost:5000/api/financeiro/relatorio
```

**Resposta:**
```json
{
  "total": 1247.50,
  "expenses": [
    {
      "Data": "2024-01-15",
      "Descrição": "Almoço",
      "Valor": 25.50,
      "Categoria": "alimentação"
    },
    {
      "Data": "2024-01-15",
      "Descrição": "Gasolina",
      "Valor": 80.00,
      "Categoria": "transporte"
    }
  ],
  "categories": {
    "alimentação": [
      {
        "Data": "2024-01-15",
        "Descrição": "Almoço",
        "Valor": 25.50,
        "Categoria": "alimentação"
      }
    ],
    "transporte": [
      {
        "Data": "2024-01-15",
        "Descrição": "Gasolina",
        "Valor": 80.00,
        "Categoria": "transporte"
      }
    ]
  },
  "count": 2
}
```

**Códigos de Status:**
- `200`: Sucesso
- `500`: Erro interno do servidor

### Tratamento de Erros

Todos os endpoints retornam erros em formato JSON consistente:

```json
{
  "error": "Descrição do erro"
}
```

**Erros Comuns:**

**Formato de Mensagem Inválido:**
```json
{
  "error": "Formato inválido. Digite 'ajuda' para ver como usar."
}
```

**Erro de Parsing:**
```json
{
  "error": "Não foi possível interpretar o valor monetário"
}
```

**Erro de Planilha:**
```json
{
  "error": "Erro ao acessar planilha: [detalhes do erro]"
}
```

### Integração com Outras Plataformas

#### Telegram

```python
import requests

def send_to_financial_agent(message):
    response = requests.post(
        'http://localhost:5000/api/financeiro/processar_mensagem',
        json={'message': message}
    )
    return response.json()['response']

# Uso no bot Telegram
@bot.message_handler(commands=['gasto'])
def handle_expense(message):
    expense_text = message.text.replace('/gasto ', '')
    response = send_to_financial_agent(expense_text)
    bot.reply_to(message, response)
```

#### Discord

```javascript
// Bot Discord
client.on('messageCreate', async (message) => {
  if (message.content.startsWith('!gasto ')) {
    const expenseText = message.content.replace('!gasto ', '');
    
    const response = await fetch('http://localhost:5000/api/financeiro/processar_mensagem', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: expenseText })
    });
    
    const data = await response.json();
    message.reply(data.response);
  }
});
```

#### Slack

```python
from slack_bolt import App

app = App(token="xoxb-your-token")

@app.message("gasto")
def handle_expense(message, say):
    expense_text = message['text'].replace('gasto ', '')
    
    response = requests.post(
        'http://localhost:5000/api/financeiro/processar_mensagem',
        json={'message': expense_text}
    )
    
    say(response.json()['response'])
```

### Rate Limiting e Performance

Para uso em produção, considere implementar:

#### Rate Limiting por IP

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@financeiro_bp.route('/processar_mensagem', methods=['POST'])
@limiter.limit("10 per minute")
def processar_mensagem():
    # código existente
```

#### Cache de Respostas

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.memoize(timeout=300)  # 5 minutos
def get_cached_total():
    return get_total_expenses()
```

#### Monitoramento

```python
import time
import logging

@financeiro_bp.before_request
def log_request():
    g.start_time = time.time()

@financeiro_bp.after_request
def log_response(response):
    duration = time.time() - g.start_time
    logging.info(f"Request processed in {duration:.2f}s")
    return response
```


## 🚀 Deploy e Produção

Esta seção aborda como fazer o deploy do sistema em diferentes ambientes de produção, desde servidores simples até plataformas de nuvem modernas.

### Preparação para Produção

#### 1. Configurações de Segurança

**Variáveis de Ambiente:**
```env
# Produção
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_super_forte_aqui
GEMINI_API_KEY=sua_api_key_do_gemini

# Configurações de Banco (opcional)
DATABASE_URL=postgresql://user:pass@localhost/financeiro

# Configurações de Segurança
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
CORS_ORIGINS=https://seu-n8n.com
```

**Configuração HTTPS:**
```python
# src/main.py - Configurações de produção
if os.getenv('FLASK_ENV') == 'production':
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

#### 2. Otimizações de Performance

**Gunicorn Configuration (gunicorn.conf.py):**
```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
```

**Requirements para Produção:**
```txt
# requirements-prod.txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
pandas==2.3.1
openpyxl==3.1.2
google-generativeai==0.3.2
python-dotenv==1.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.7  # Para PostgreSQL
redis==4.6.0  # Para cache
flask-limiter==3.5.0  # Para rate limiting
```

### Deploy em VPS/Servidor Dedicado

#### 1. Configuração do Servidor

**Instalação de Dependências (Ubuntu/Debian):**
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e dependências
sudo apt install python3.11 python3.11-venv python3-pip nginx supervisor -y

# Instalar PostgreSQL (opcional)
sudo apt install postgresql postgresql-contrib -y
```

**Configuração do Usuário:**
```bash
# Criar usuário para a aplicação
sudo adduser financeiro-bot
sudo usermod -aG sudo financeiro-bot

# Configurar diretório da aplicação
sudo mkdir -p /opt/financeiro-bot
sudo chown financeiro-bot:financeiro-bot /opt/financeiro-bot
```

#### 2. Deploy da Aplicação

```bash
# Como usuário financeiro-bot
cd /opt/financeiro-bot

# Clonar/copiar código
git clone seu-repositorio.git .
# ou
scp -r agente_financeiro_whatsapp/* financeiro-bot@servidor:/opt/financeiro-bot/

# Configurar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements-prod.txt

# Configurar variáveis de ambiente
cp .env.example .env
nano .env  # Editar com valores de produção

# Testar aplicação
python src/main.py
```

#### 3. Configuração do Nginx

**Arquivo: `/etc/nginx/sites-available/financeiro-bot`**
```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Rate limiting
    location /api/ {
        limit_req zone=api burst=10 nodelay;
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Rate limiting configuration
http {
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/m;
}
```

**Ativar Site:**
```bash
sudo ln -s /etc/nginx/sites-available/financeiro-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 4. Configuração do Supervisor

**Arquivo: `/etc/supervisor/conf.d/financeiro-bot.conf`**
```ini
[program:financeiro-bot]
command=/opt/financeiro-bot/venv/bin/gunicorn -c gunicorn.conf.py src.main:app
directory=/opt/financeiro-bot
user=financeiro-bot
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/financeiro-bot.log
environment=PATH="/opt/financeiro-bot/venv/bin"
```

**Iniciar Serviço:**
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start financeiro-bot
sudo supervisorctl status
```

### Deploy em Plataformas de Nuvem

#### 1. Heroku

**Arquivo: `Procfile`**
```
web: gunicorn -c gunicorn.conf.py src.main:app
```

**Arquivo: `runtime.txt`**
```
python-3.11.0
```

**Deploy:**
```bash
# Instalar Heroku CLI
# Fazer login: heroku login

# Criar aplicação
heroku create seu-financeiro-bot

# Configurar variáveis
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=sua_chave_secreta
heroku config:set GEMINI_API_KEY=sua_api_key

# Deploy
git add .
git commit -m "Deploy para produção"
git push heroku main

# Verificar logs
heroku logs --tail
```

#### 2. DigitalOcean App Platform

**Arquivo: `.do/app.yaml`**
```yaml
name: financeiro-bot
services:
- name: web
  source_dir: /
  github:
    repo: seu-usuario/seu-repositorio
    branch: main
  run_command: gunicorn -c gunicorn.conf.py src.main:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: FLASK_ENV
    value: production
  - key: SECRET_KEY
    value: sua_chave_secreta
    type: SECRET
  - key: GEMINI_API_KEY
    value: sua_api_key
    type: SECRET
```

#### 3. AWS EC2 com Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

# Copiar código da aplicação
COPY . .

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expor porta
EXPOSE 5000

# Comando de inicialização
CMD ["gunicorn", "-c", "gunicorn.conf.py", "src.main:app"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./gastos.xlsx:/app/gastos.xlsx
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped
```

### Monitoramento e Logs

#### 1. Configuração de Logs

**Arquivo: `logging.conf`**
```ini
[loggers]
keys=root,financeiro

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[logger_financeiro]
level=DEBUG
handlers=fileHandler
qualname=financeiro
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('/var/log/financeiro-bot.log',)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

#### 2. Métricas e Alertas

**Monitoramento com Prometheus:**
```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Financeiro Bot', version='1.0.0')

# Métricas customizadas
expense_counter = Counter('expenses_total', 'Total de gastos registrados')
advice_counter = Counter('advice_requests_total', 'Total de conselhos solicitados')

@financeiro_bp.route('/processar_mensagem', methods=['POST'])
def processar_mensagem():
    # código existente...
    if expense_data:
        expense_counter.inc()
    # resto do código...
```

### Backup e Recuperação

#### 1. Backup Automático da Planilha

**Script: `backup.sh`**
```bash
#!/bin/bash

# Configurações
BACKUP_DIR="/opt/backups/financeiro-bot"
APP_DIR="/opt/financeiro-bot"
DATE=$(date +%Y%m%d_%H%M%S)

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Backup da planilha
cp $APP_DIR/gastos.xlsx $BACKUP_DIR/gastos_$DATE.xlsx

# Manter apenas últimos 30 backups
find $BACKUP_DIR -name "gastos_*.xlsx" -mtime +30 -delete

# Log
echo "$(date): Backup realizado - gastos_$DATE.xlsx" >> $BACKUP_DIR/backup.log
```

**Crontab para backup automático:**
```bash
# Backup diário às 2h da manhã
0 2 * * * /opt/financeiro-bot/backup.sh
```

#### 2. Sincronização com Cloud Storage

**Script para AWS S3:**
```bash
#!/bin/bash

# Upload para S3
aws s3 cp /opt/financeiro-bot/gastos.xlsx s3://seu-bucket/backups/gastos_$(date +%Y%m%d).xlsx

# Sincronizar logs
aws s3 sync /var/log/ s3://seu-bucket/logs/ --exclude "*" --include "financeiro-bot*"
```

## 🔧 Troubleshooting

Esta seção aborda problemas comuns e suas soluções, organizados por categoria para facilitar a resolução de issues.

### Problemas de Instalação

#### Erro: "numpy.dtype size changed"

**Sintoma:**
```
ValueError: numpy.dtype size changed, may indicate binary incompatibility
```

**Solução:**
```bash
# Atualizar numpy e pandas
pip install --upgrade numpy pandas

# Se persistir, reinstalar do zero
pip uninstall numpy pandas
pip install numpy pandas
```

#### Erro: "No module named 'openpyxl'"

**Sintoma:**
```
ModuleNotFoundError: No module named 'openpyxl'
```

**Solução:**
```bash
# Instalar openpyxl
pip install openpyxl

# Verificar instalação
python -c "import openpyxl; print('OK')"
```

#### Erro de Permissão na Planilha

**Sintoma:**
```
PermissionError: [Errno 13] Permission denied: 'gastos.xlsx'
```

**Solução:**
```bash
# Verificar permissões
ls -la gastos.xlsx

# Corrigir permissões
chmod 664 gastos.xlsx
chown usuario:grupo gastos.xlsx

# Se a planilha estiver aberta, feche-a
```

### Problemas de Configuração

#### API do Gemini Não Funciona

**Sintoma:**
```
⚠️ API do Gemini não configurada
```

**Verificações:**
1. **Arquivo .env existe?**
   ```bash
   ls -la .env
   ```

2. **API Key está correta?**
   ```bash
   grep GEMINI_API_KEY .env
   ```

3. **Testar API manualmente:**
   ```python
   import google.generativeai as genai
   genai.configure(api_key="sua_api_key")
   model = genai.GenerativeModel('gemini-pro')
   response = model.generate_content("Teste")
   print(response.text)
   ```

**Soluções:**
- Verificar se a API key está ativa no Google AI Studio
- Confirmar que não há caracteres extras na variável de ambiente
- Verificar limites de uso da API

#### Erro de CORS

**Sintoma:**
```
Access to fetch at 'http://localhost:5000' from origin 'https://n8n.com' has been blocked by CORS policy
```

**Solução:**
```python
# src/main.py
from flask_cors import CORS

# Configurar CORS específico
CORS(app, origins=['https://seu-n8n.com', 'https://outro-dominio.com'])

# Ou permitir todos (apenas desenvolvimento)
CORS(app, origins='*')
```

### Problemas de Dados

#### Planilha Corrompida

**Sintoma:**
```
BadZipFile: File is not a zip file
```

**Solução:**
```bash
# Backup da planilha corrompida
mv gastos.xlsx gastos_corrupted.xlsx

# Recriar planilha
python -c "from src.excel_handler import initialize_excel; initialize_excel()"

# Tentar recuperar dados manualmente se possível
```

#### Valores Não Reconhecidos

**Sintoma:** Gastos não são registrados corretamente

**Verificações:**
1. **Formato da mensagem:**
   ```
   Correto: "Almoço 25.50 alimentação"
   Incorreto: "Gastei 25,50 no almoço"
   ```

2. **Caracteres especiais:**
   ```python
   # Testar regex
   import re
   message = "Almoço 25.50 alimentação"
   pattern = r'^(.+?)\s+(\d+(?:[.,]\d{2})?)\s+(.+)$'
   match = re.match(pattern, message)
   print(match.groups() if match else "Não reconhecido")
   ```

**Soluções:**
- Melhorar regex de parsing
- Adicionar validação de entrada
- Implementar feedback de erro mais específico

### Problemas de Performance

#### Servidor Lento

**Sintomas:**
- Respostas demoram mais que 5 segundos
- Timeouts frequentes
- Alto uso de CPU/memória

**Diagnóstico:**
```bash
# Verificar uso de recursos
top -p $(pgrep -f "python src/main.py")

# Verificar logs
tail -f /var/log/financeiro-bot.log

# Testar endpoints
time curl -X POST http://localhost:5000/api/financeiro/processar_mensagem \
  -H "Content-Type: application/json" \
  -d '{"message": "total"}'
```

**Soluções:**
1. **Otimizar leitura da planilha:**
   ```python
   # Cache da planilha em memória
   import functools
   import time

   @functools.lru_cache(maxsize=1)
   def get_cached_expenses():
       return pd.read_excel(EXCEL_FILE)

   # Invalidar cache periodicamente
   def clear_cache():
       get_cached_expenses.cache_clear()
   ```

2. **Usar banco de dados:**
   ```python
   # Migrar para SQLite/PostgreSQL
   from sqlalchemy import create_engine
   import pandas as pd

   engine = create_engine('sqlite:///gastos.db')
   df.to_sql('gastos', engine, if_exists='append')
   ```

#### Problemas de Memória

**Sintoma:**
```
MemoryError: Unable to allocate array
```

**Soluções:**
```python
# Processar planilha em chunks
def read_expenses_chunked():
    chunks = pd.read_excel(EXCEL_FILE, chunksize=1000)
    return pd.concat(chunks, ignore_index=True)

# Limpar DataFrames não utilizados
import gc
df = None
gc.collect()
```

### Problemas de Integração

#### n8n Não Recebe Respostas

**Verificações:**
1. **Servidor Flask está rodando?**
   ```bash
   curl http://localhost:5000/api/financeiro/processar_mensagem
   ```

2. **n8n consegue acessar o servidor?**
   ```bash
   # No servidor do n8n
   curl http://ip-do-flask:5000/api/financeiro/processar_mensagem
   ```

3. **Firewall bloqueando?**
   ```bash
   # Verificar portas abertas
   netstat -tlnp | grep 5000
   
   # Abrir porta se necessário
   sudo ufw allow 5000
   ```

#### WhatsApp Business API Issues

**Problemas Comuns:**
- Webhook não recebe mensagens
- Mensagens não são enviadas
- Rate limiting atingido

**Soluções:**
1. **Verificar configuração do webhook:**
   ```bash
   # Testar webhook manualmente
   curl -X POST https://seu-n8n.com/webhook/whatsapp-financeiro \
     -H "Content-Type: application/json" \
     -d '{"from": "5511999999999", "message": "teste"}'
   ```

2. **Verificar logs do WhatsApp Business:**
   - Acessar painel do Facebook Developers
   - Verificar logs de webhook
   - Confirmar status da aplicação

### Logs e Debugging

#### Habilitar Debug Detalhado

```python
# src/main.py
import logging

if os.getenv('DEBUG') == 'true':
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

# Adicionar logs nas funções críticas
@financeiro_bp.route('/processar_mensagem', methods=['POST'])
def processar_mensagem():
    app.logger.debug(f"Mensagem recebida: {request.get_json()}")
    # resto do código...
```

#### Monitoramento em Tempo Real

```bash
# Logs do Flask
tail -f /var/log/financeiro-bot.log

# Logs do sistema
journalctl -u financeiro-bot -f

# Logs do Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Contato e Suporte

Para problemas não cobertos neste guia:

1. **Verificar Issues no GitHub:** [Link do repositório]
2. **Documentação oficial das dependências:**
   - [Flask Documentation](https://flask.palletsprojects.com/)
   - [Pandas Documentation](https://pandas.pydata.org/docs/)
   - [Google Gemini API](https://ai.google.dev/docs)
3. **Comunidade n8n:** [n8n Community](https://community.n8n.io/)

---

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor, leia o [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre nosso código de conduta e o processo para enviar pull requests.

## 📞 Suporte

Para suporte técnico ou dúvidas sobre implementação:
- **Email:** suporte@exemplo.com
- **Discord:** [Link do servidor]
- **Documentação:** [Link da documentação online]

---

**Desenvolvido com ❤️ pela equipe Manus AI**

#   A s s i s t e n t e - F i n a n c e i r o  
 