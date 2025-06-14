import streamlit as st
from backend.promo_engine import generate_campaign
import json

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
            # Zapisz wynik do session_state, aby był dostępny w calendar_timeline
            st.session_state["promo_result"] = result

            st.subheader("Prompt:")
            st.code(result["prompt"], language="text")

            st.subheader("Wynik AI:")
            ai_output = result["ai_output"]
            # Spróbuj sparsować JSON z postami
            posts = []
            press_note = ""
            teaser = ""
            try:
                start = ai_output.find("[")
                end = ai_output.find("]")
                if start != -1 and end != -1:
                    posts_json = ai_output[start:end+1]
                    posts = json.loads(posts_json)
                
                # Wyciągnij notkę prasową i teaser
                press_idx = ai_output.lower().find("notka prasowa")
                teaser_idx = ai_output.lower().find("teaser")
                if press_idx != -1 and teaser_idx != -1:
                    press_note = ai_output[press_idx:teaser_idx].strip()
                    teaser = ai_output[teaser_idx:].strip()
            except Exception as e:
                st.warning(f"Nie udało się sparsować JSON z postami: {e}")
            if posts:
                st.markdown("### Propozycje postów:")
                for post in posts:
                    st.write(f"📅 {post['date']}: {post['content']}")
            if press_note:
                st.markdown("### Notka prasowa:")
                st.write(press_note)
            if teaser:
                st.markdown("### Teaser e-mailowy:")
                st.write(teaser)
            if not posts and not press_note and not teaser:
                st.markdown(ai_output)