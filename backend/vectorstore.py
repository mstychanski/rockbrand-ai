import os
import glob
from typing import List
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
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
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vectordb = FAISS.from_documents(split_docs, embeddings)
    vectordb.save_local(VECTOR_DB_PATH)
    print(f"Vectorstore saved to {VECTOR_DB_PATH}")

def load_vectorstore():
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(VECTOR_DB_PATH, embeddings)

# Budowa i obsługa bazy wektorowej (RAG)

def get_band_context(band_name: str, event: str) -> str:
    vectordb = load_vectorstore()
    query = f"{band_name} {event}"
    results = vectordb.similarity_search(query, k=3)
    context = "\n---\n".join([doc.page_content for doc in results])
    return context if context else f"Brak dodatkowego kontekstu dla zespołu {band_name} i wydarzenia {event}."

if __name__ == "__main__":
    build_vectorstore()