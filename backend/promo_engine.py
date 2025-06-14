from backend.openrouter_client import ask_llm
from jinja2 import Template
from backend.vectorstore import get_band_context

PROMO_TEMPLATE = Template("""
Zespół: {{ band_name }}
Styl: {{ genre }}
Nadchodzące wydarzenie: {{ event }}

Kontekst zespołu i wydarzenia:
{{ rag_context }}

Wygeneruj:
- 3 propozycje postów na social media (IG/FB)
- propozycję notki prasowej
- krótki teaser e-mailowy do fanów

Użyj stylu pasującego do zespołu i wydarzenia. Uwzględnij klimat i emocje.
""")

def generate_campaign(request: dict) -> dict:
    band_name = request.get("band_name", "Nieznany Zespół")
    genre = request.get("genre", "rock alternatywny")
    event = request.get("event", "premiera singla")
    # Pobierz kontekst z RAG
    rag_context = get_band_context(band_name=band_name, event=event)
    prompt = PROMO_TEMPLATE.render(
        band_name=band_name,
        genre=genre,
        event=event,
        rag_context=rag_context
    )
    response = ask_llm(prompt)
    return {"prompt": prompt, "ai_output": response}

# Plik: frontend/streamlit_app.py (skrót)
import streamlit as st
from components import promo_planner, merch_designer, calendar_timeline

st.title("RockBrand AI")

tab1, tab2, tab3 = st.tabs(["🎤 Kampanie", "👕 Merch", "🗓 Timeline"])

with tab1:
    promo_planner.render()

with tab2:
    merch_designer.render()

with tab3:
    calendar_timeline.render()
