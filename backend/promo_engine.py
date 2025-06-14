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
- 10 propozycji postów na social media (IG/FB), każdy z sugerowaną datą publikacji,
- Zwróć wynik jako listę obiektów JSON: [{"date": "YYYY-MM-DD", "content": "..."}],
- Propozycję notki prasowej,
- Krótki teaser e-mailowy do fanów

Użyj stylu pasującego do zespołu i wydarzenia. Uwzględnij klimat i emocje.
""")

def generate_campaign(request: dict) -> dict:
    band_name = request.get("band_name", "Nieznany Zespół")
    genre = request.get("genre", "rock alternatywny")
    event = request.get("event", "premiera singla")

    rag_context = get_band_context(band_name=band_name, event=event)
    prompt = PROMO_TEMPLATE.render(
        band_name=band_name,
        genre=genre,
        event=event,
        rag_context=rag_context
    )
    response = ask_llm(prompt)
    return {"prompt": prompt, "ai_output": response}
