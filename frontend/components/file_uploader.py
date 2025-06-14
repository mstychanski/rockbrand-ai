import streamlit as st
import os
import sys

DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))
BACKEND_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend'))


def render():
    st.header("Dodaj plik do bazy wiedzy (RAG)")
    uploaded_file = st.file_uploader("Wgraj plik tekstowy (.txt)", type=["txt"])
    if uploaded_file is not None:
        save_path = os.path.join(DATA_PATH, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Plik {uploaded_file.name} został zapisany w {save_path}")
        # Przebuduj bazę wektorową po wgraniu pliku
        with st.spinner("Przebudowywanie bazy wektorowej..."):
            result = os.system(f'python "{os.path.join(BACKEND_PATH, 'vectorstore.py')}"')
        if result == 0:
            st.success("Baza wektorowa została przebudowana.")
        else:
            st.error("Błąd podczas przebudowy bazy wektorowej.")
