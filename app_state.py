# backend/app_state.py

import os
import logging

import os
import logging
import chromadb

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq

# --------------------------------------------------
# Setup
# --------------------------------------------------
load_dotenv()
logging.basicConfig(level=logging.INFO)

_llm = None
_embeddings = None
_vector_store = None

# --------------------------------------------------
# Config
# --------------------------------------------------
PDF_PATH = os.getenv(
    "POLICY_PDF_PATH",
    "data/umbrella_corp_policies.pdf"
)




# --------------------------------------------------
# LLM
# --------------------------------------------------
def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGroq(model="llama-3.1-8b-instant")
        logging.info("✅ LLM initialized")
    return _llm


# --------------------------------------------------
# Embeddings
# --------------------------------------------------
def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        logging.info("✅ Embeddings initialized")
    return _embeddings


# --------------------------------------------------
# Vector Store (RAG)
# --------------------------------------------------
def get_vector_store():
    """
    Initialize vector store ONCE per process.
    Pure in-memory Chroma (Render free-tier safe).
    """
    global _vector_store

    if _vector_store is not None:
        return _vector_store

    if not os.path.isfile(PDF_PATH):
        raise FileNotFoundError(f"❌ Policy PDF not found at {PDF_PATH}")

    logging.info("📄 Building vector store from policy PDF (in-memory)")

    embedding_function = get_embeddings()

    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    splits = splitter.split_documents(docs)

    # 🔥 EXPLICIT IN-MEMORY CHROMA CLIENT
    client = chromadb.Client(
        settings=chromadb.Settings(
            anonymized_telemetry=False
        )
    )

    _vector_store = Chroma.from_documents(
        documents=splits,
        embedding=embedding_function,
        client=client,
        collection_name="policy_docs"
    )

    logging.info("✅ Vector store initialized (pure in-memory)")
    return _vector_store
