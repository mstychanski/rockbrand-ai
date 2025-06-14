import streamlit as st
from backend.promo_engine import generate_campaign
import json

def render():
    st.header("🗓 Nadchodzące wydarzenia zespołu")

    st.markdown("Wygeneruj kampanię w zakładce 'Kampanie', aby zobaczyć posty na osi czasu.")

    # Przechowuj wynik AI w stanie sesji
    if "promo_result" not in st.session_state:
        st.session_state["promo_result"] = None

    # Przycisk do pobrania danych z kampanii
    if st.button("🔄 Załaduj posty z ostatniej kampanii"):
        # Załaduj ostatni wynik z promo_planner (jeśli był generowany)
        try:
            from backend.promo_engine import generate_campaign
            # Możesz tu pobrać dane z sesji lub innego źródła, jeśli są dostępne
            # Tu tylko przykład: pobierz z sesji promo_result
            pass
        except Exception as e:
            st.error(f"Błąd podczas ładowania postów: {e}")

    # Wyświetl posty jeśli są w stanie sesji
    if st.session_state["promo_result"]:
        ai_output = st.session_state["promo_result"]["ai_output"]
        posts = []
        try:
            start = ai_output.find("[")
            end = ai_output.find("]")
            if start != -1 and end != -1:
                posts_json = ai_output[start:end+1]
                posts = json.loads(posts_json)
        except Exception as e:
            st.warning(f"Nie udało się sparsować JSON z postami: {e}")
        if posts:
            st.markdown("### Propozycje postów:")
            for post in posts:
                st.write(f"📅 {post['date']}: {post['content']}")
        else:
            st.info("Brak postów do wyświetlenia. Wygeneruj kampanię w zakładce 'Kampanie'.")
    else:
        st.info("Brak danych do wyświetlenia. Wygeneruj kampanię w zakładce 'Kampanie'.")