import os
import glob
from typing import List
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from backend.embedder import create_index, retrieve_docs
import streamlit as st

DATA_PATH = "data"
VECTOR_DB_PATH = "data/faiss_index"

def load_documents() -> List[str]:
    paths = glob.glob(os.path.join(DATA_PATH, "**/*.txt"), recursive=True)
    docs = []
    for path in paths:
        loader = TextLoader(path)
        docs.extend(loader.load())
    return docs

# Budowa i obsługa bazy wektorowej (RAG)

# Utrzymuj index FAISS w pamięci (globalnie)
_faiss_index = None

def build_vectorstore():
    global _faiss_index
    documents = load_documents()
    # Zamień dokumenty na listę słowników {"filename": ..., "text": ...}
    doc_objs = []
    for doc in documents:
        doc_objs.append({"filename": getattr(doc, 'metadata', {}).get('source', ''), "text": doc.page_content})
    _faiss_index = create_index(doc_objs)
    print("Vectorstore built and stored in memory.")

def load_vectorstore():
    global _faiss_index
    if _faiss_index is None:
        build_vectorstore()
    return _faiss_index

def get_band_context(band_name: str, event: str) -> str:
    faiss_index = load_vectorstore()
    query = f"{band_name} {event}"
    results = retrieve_docs(query, faiss_index, k=3)
    context = "\n---\n".join([doc["text"] for doc in results])
    return context if context else f"Brak dodatkowego kontekstu dla zespołu {band_name} i wydarzenia {event}."

if __name__ == "__main__":
    build_vectorstore()