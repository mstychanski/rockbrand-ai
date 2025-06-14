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

def build_vectorstore():
    documents = load_documents()
    # Zamień dokumenty na listę słowników {"filename": ..., "text": ...}
    doc_objs = []
    for doc in documents:
        doc_objs.append({"filename": getattr(doc, 'metadata', {}).get('source', ''), "text": doc.page_content})
    faiss_index = create_index(doc_objs)
    # Zapisz index i metadata do pliku (pickle)
    import pickle
    with open(VECTOR_DB_PATH, "wb") as f:
        pickle.dump(faiss_index, f)
    print(f"Vectorstore saved to {VECTOR_DB_PATH}")

def load_vectorstore():
    import pickle
    with open(VECTOR_DB_PATH, "rb") as f:
        faiss_index = pickle.load(f)
    return faiss_index

# Budowa i obsługa bazy wektorowej (RAG)

def get_band_context(band_name: str, event: str) -> str:
    faiss_index = load_vectorstore()
    query = f"{band_name} {event}"
    results = retrieve_docs(query, faiss_index, k=3)
    context = "\n---\n".join([doc["text"] for doc in results])
    return context if context else f"Brak dodatkowego kontekstu dla zespołu {band_name} i wydarzenia {event}."

if __name__ == "__main__":
    build_vectorstore()