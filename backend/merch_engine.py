from backend.openrouter_client import ask_llm
from jinja2 import Template
from backend.vectorstore import get_band_context

MERCH_TEMPLATE = Template("""
Zespół: {{ band_name }}
Styl merchu: {{ style }}
Produkt: {{ product }}

Kontekst zespołu:
{{ rag_context }}

Wygeneruj:
- Opis produktu do sklepu
- 2 propozycje haseł promocyjnych
- Krótki prompt graficzny do Midjourney

Użyj stylu i klimatu pasującego do zespołu.
""")

# Generator merchu i promptów graficznych
def generate_merch_items(request: dict) -> dict:
    band_name = request.get("band_name", "Nieznany Zespół")
    style = request.get("style", "rock")
    product = request.get("product", "T-shirt")
    rag_context = get_band_context(band_name=band_name, event=product)
    prompt = MERCH_TEMPLATE.render(
        band_name=band_name,
        style=style,
        product=product,
        rag_context=rag_context
    )
    response = ask_llm(prompt)
    return {"prompt": prompt, "ai_output": response}
