import os
import logging
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Import the data generation script
from scripts.setup_mock_data import generate_all_mock_data

logger = logging.getLogger(__name__)

# Constants
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PDF_PATH = DATA_DIR / "knowledge_base.pdf"

def get_vector_store():
    # 1. Ensure all mock data exists
    if not PDF_PATH.exists() or not (DATA_DIR / "customers.json").exists():
        logger.warning("Mock Data missing. Running generation script...")
        generate_all_mock_data()
    
    # 2. Setup Embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # 3. Ingest (In-memory/Simulated for this exercise)
    # Note: iterating directly to loading for simplicity in this stateless example
    
    loader = PyPDFLoader(str(PDF_PATH))
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)
    
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings,
        collection_name="support_kb"
    )
    
    return vectorstore
