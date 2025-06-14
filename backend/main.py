from fastapi import FastAPI
from backend import promo_engine, merch_engine

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/generate-promo")
def generate_promo(request: dict):
    return promo_engine.generate_campaign(request)

@app.post("/generate-merch")
def generate_merch(request: dict):
    return merch_engine.generate_merch_items(request)
