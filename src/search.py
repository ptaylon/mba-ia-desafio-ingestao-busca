import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def check_required_environments():
    # Check if all the required environment variable are defined
    for environment in ["OPENAI_API_KEY", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME"]:
        if not os.getenv(environment):
            raise ValueError(f"A variável de ambiente {environment} não está definida")

def search_prompt(question=None):
    # Check if environment variables are configured
    check_required_environments()
    
    # Create OpenAI embeddings model instance
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small")
    )
    
    # Connect to PostgreSQL vector database
    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL")
    )
    
    # Search for documents similar to the question (top 10 results)
    results = vectorstore.similarity_search_with_score(question, k=10)
    
    # Extract page content from search results and join with newlines
    context = "\n".join([result[0].page_content for result in results])
    
    # Format the prompt template with context and question
    prompt = PROMPT_TEMPLATE.format(contexto=context, pergunta=question)
    
    return prompt