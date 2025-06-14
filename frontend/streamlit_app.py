import streamlit as st
from components import promo_planner, merch_designer, calendar_timeline
from components import file_uploader

st.title("RockBrand AI")

tab1, tab2, tab3, tab4 = st.tabs(["🎤 Kampanie", "👕 Merch", "🗓 Timeline", "📁 Upload plików"])

with tab1:
    promo_planner.render()

with tab2:
    merch_designer.render()

with tab3:
    calendar_timeline.render()

with tab4:
    file_uploader.render()
