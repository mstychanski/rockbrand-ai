import streamlit as st
from backend.promo_engine import generate_campaign

def render():
    st.header("🎤 Generator kampanii promocyjnej")

    band_name = st.text_input("Nazwa zespołu", "The Electric Owls")
    genre = st.text_input("Gatunek muzyczny", "Indie Rock")
    event = st.text_input("Wydarzenie", "Premiera nowego singla 1 lipca")

    if st.button("Wygeneruj kampanię"):
        with st.spinner("Generuję..."):
            result = generate_campaign({
                "band_name": band_name,
                "genre": genre,
                "event": event
            })
            st.subheader("Prompt:")
            st.code(result["prompt"], language="text")

            st.subheader("Wynik AI:")
            st.markdown(result["ai_output"])