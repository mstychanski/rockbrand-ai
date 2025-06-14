import streamlit as st
from backend.merch_engine import generate_merch_items

def render():
    st.header("👕 Generator merchu i opisów")

    band_name = st.text_input("Nazwa zespołu (merch)", "The Electric Owls")
    style = st.text_input("Styl merchu (np. retro grunge, cyberpunk)", "retro grunge")
    product = st.selectbox("Typ produktu", ["T-shirt", "Plakat", "Naklejka", "Bluza"])

    if st.button("Wygeneruj merch"):
        with st.spinner("Generuję..." ):
            result = generate_merch_items({
                "band_name": band_name,
                "style": style,
                "product": product
            })
            st.subheader("Prompt:")
            st.code(result.get("prompt", ""), language="text")
            st.subheader("Opis AI:")
            st.markdown(result.get("ai_output", str(result)))
