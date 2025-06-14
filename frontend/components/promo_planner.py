import streamlit as st
import requests

def render():
    st.header("🎤 Generator kampanii promocyjnej")

    band_name = st.text_input("Nazwa zespołu", "The Electric Owls")
    genre = st.text_input("Gatunek muzyczny", "Indie Rock")
    event = st.text_input("Wydarzenie", "Premiera nowego singla 1 lipca")

    if st.button("Wygeneruj kampanię"):
        with st.spinner("Generuję..."):
            response = requests.post("http://localhost:8000/generate-promo", json={
                "band_name": band_name,
                "genre": genre,
                "event": event
            })
            if response.status_code == 200:
                result = response.json()
                st.subheader("Prompt:")
                st.code(result["prompt"], language="text")

                st.subheader("Wynik AI:")
                st.markdown(result["ai_output"])
            else:
                st.error("Nie udało się wygenerować kampanii.")