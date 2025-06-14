import os
import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Use environment variables for API key, base URL, and model
API_KEY = st.secrets["API_KEY"]
BASE_URL = st.secrets["BASE_URL"]
MODEL = st.secrets["MODEL"]

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def ask_llm(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8
    }
    try:
        response = httpx.post(BASE_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        content = response.json()
        return content["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR contacting OpenRouter API] {e}"
