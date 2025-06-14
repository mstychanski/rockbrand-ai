import streamlit as st
from datetime import datetime, timedelta
import requests
import os

FAKE_EVENTS = [
    {"title": "Premiera singla", "date": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')},
    {"title": "Koncert w Warszawie", "date": (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')},
    {"title": "Drop merchu", "date": (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')}
]

def render():
    st.header("🗓 Nadchodzące wydarzenia zespołu")

    for event in FAKE_EVENTS:
        st.write(f"📍 **{event['title']}** — {event['date']}")

    if st.button("📥 Pobierz jako .ics"):
        with st.spinner("Generuję plik kalendarza..."):
            response = requests.post("http://localhost:8000/generate-ics", json={"events": FAKE_EVENTS})
            if response.status_code == 200:
                result = response.json()
                if result["status"] == "success":
                    with open(result["ics_file"], "rb") as f:
                        st.download_button(
                            label="📅 Pobierz RockBand.ics",
                            data=f.read(),
                            file_name="RockBandEvents.ics",
                            mime="text/calendar"
                        )
                else:
                    st.error(f"Błąd: {result['message']}")
            else:
                st.error("Nie udało się wygenerować pliku .ics")

    st.header("Timeline wydarzeń")
    # Przykładowe dane wydarzeń
    events = [
        {"date": "2024-06-01", "title": "Premiera singla", "desc": "Nowy singiel już dostępny!"},
        {"date": "2024-06-10", "title": "Koncert w Warszawie", "desc": "Klub Stodoła, godz. 20:00"},
        {"date": "2024-07-05", "title": "Start przedsprzedaży merchu", "desc": "Nowa kolekcja koszulek"},
    ]
    # Sortowanie po dacie
    events = sorted(events, key=lambda e: e["date"])
    # Wizualizacja osi czasu
    for event in events:
        st.markdown(
            f"""
            <div style="border-left: 3px solid #888; padding-left: 12px; margin-bottom: 18px;">
                <span style="color: #888;">{event['date']}</span><br>
                <b>{event['title']}</b><br>
                <span>{event['desc']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )