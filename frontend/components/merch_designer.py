import streamlit as st
import requests

def render():
    st.header("👕 Generator merchu i opisów")

    band_name = st.text_input("Nazwa zespołu (merch)", "The Electric Owls")
    style = st.text_input("Styl merchu (np. retro grunge, cyberpunk)", "retro grunge")
    product = st.selectbox("Typ produktu", ["T-shirt", "Plakat", "Naklejka", "Bluza"])

    if st.button("Wygeneruj merch"):
        with st.spinner("Generuję..." ):
            response = requests.post("http://localhost:8000/generate-merch", json={
                "band_name": band_name,
                "style": style,
                "product": product
            })
            if response.status_code == 200:
                result = response.json()
                st.subheader("Opis AI:")
                st.markdown(result["ai_output"])
            else:
                st.error("Nie udało się wygenerować merchu.")
