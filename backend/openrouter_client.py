import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Use Streamlit secrets for API key and model
API_KEY = st.secrets["API_KEY"]
MODEL = st.secrets["MODEL"]

client = OpenAI(api_key=API_KEY)

def ask_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR contacting OpenAI API] {e}"
