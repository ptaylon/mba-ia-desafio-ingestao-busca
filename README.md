# Desafio MBA Engenharia de Software com IA - Full Cycle

Sistema de ingestão e busca semântica com LangChain e PostgreSQL + pgVector.

## Configuração

### 1. Instalação do ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuração das variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Configurações do banco de dados
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/vectordb
PG_VECTOR_COLLECTION_NAME=documentos

# Caminho para o PDF
PDF_PATH=document.pdf

# OpenAI (opcional - escolha entre OpenAI ou Google)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_EMBEDDINGS_MODEL=text-embedding-3-small
OPENAI_LLM_MODEL=gpt-4o-mini

# Google Gemini (opcional - escolha entre OpenAI ou Google)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_LLM_MODEL=gemini-2.0-flash-exp
```

### 3. Execução

1. **Subir o banco de dados:**
```bash
docker compose up -d
```

2. **Executar ingestão do PDF:**
```bash
python src/ingest.py
```

3. **Rodar o chat:**
```bash
python src/chat.py
```

## Uso

Após executar o chat, você pode fazer perguntas sobre o conteúdo do PDF. O sistema irá:
- Buscar informações relevantes no banco vetorial
- Responder baseado apenas no contexto do documento
- Indicar quando não tem informações suficientes

Para sair do chat, digite `sair`, `exit` ou `quit`.