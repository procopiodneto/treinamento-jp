import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.markdown("# 📱 Lista de Dispositivos")
st.sidebar.markdown("# Lista de Dispositivos")

st.subheader("Lista de dispositivos")

chamado = requests.get(f"{API_URL}/devices/")

if chamado.status_code == 200:
    dispositivos = chamado.json()
    st.dataframe(dispositivos)
else:
    st.error("Erro ao buscar dispositivos")