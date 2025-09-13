import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

def check_required_enviroments():
    # Check if all the required environment variable are defined
    for environment in ["OPENAI_API_KEY", "GOOGLE_API_KEY", "PDF_PATH", "DATABASE_URL", "PG_VECTOR_COLLECTION_NAME"]:
        if not os.getenv(environment):
            raise ValueError(f"A variável de ambiente {environment} não está definida")

# Get the PDF path
def get_document():
    current_directory = Path(__file__).parent.parent
    PDF_PATH = os.getenv("PDF_PATH")
    pdf_path = current_directory / PDF_PATH
    if not pdf_path.exists():
        raise FileNotFoundError(f"O arquivo {pdf_path} não foi encontrado")
    return pdf_path

def split_document(pdf_path):
    # Split the document into chunks
    docs = PyPDFLoader(pdf_path).load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150)
    document_chunks = splitter.split_documents(docs)

    # Enrich the chunks with the metadata
    enriched_chunks = [
        Document(
            page_content=chunk.page_content,
            metadata={k: v for k, v in chunk.metadata.items() if v not in ("", None)}
        ) 
        for chunk in document_chunks
    ]

    # Create the ids
    ids = [f"doc-{i}" for i in range(len(enriched_chunks))]
    return enriched_chunks, ids

def create_embeddings():
    # Create the embeddings
    embeddings = OpenAIEmbeddings(
        model=os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small")
    )
    return embeddings

def save_to_database(enriched_chunks, ids, embeddings):
    # Save the chunks to the database
    PGVector.from_documents(
        enriched_chunks, 
        ids, 
        embeddings, 
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME")
    )


def ingest_pdf():
    check_required_enviroments()
    pdf_path = get_document()
    enriched_chunks, ids = split_document(pdf_path)
    embeddings = create_embeddings()
    save_to_database(enriched_chunks, ids, embeddings)

if __name__ == "__main__":
    ingest_pdf()