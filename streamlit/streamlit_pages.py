import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://fastAPI_devices:8000")

# PÁGINAS
home_page = st.Page("home_page.py", title="Lista de Dispositivos", icon="📱")
pagina_cadastro = st.Page("pagina_cadastro.py", title="Cadastro", icon="📃")
pagina_ajustes = st.Page("pagina_ajustes.py", title="Ajustes", icon="🔧")

pg = st.navigation([home_page, pagina_cadastro, pagina_ajustes])

try:
    resp = requests.get(f"{API_URL}/devices/count", params={"min_uptime": 60})
    if resp.status_code == 200:
        count = resp.json().get("count", 0)
        st.sidebar.metric("Dispositivos com uptime > 60", count)
except Exception:
    pass

pg.run()