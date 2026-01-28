import streamlit as st
import requests
import os
from datetime import datetime
import pandas as pd
from io import BytesIO

API_URL = os.getenv("API_URL", "http://fastAPI_devices:8000")

st.markdown("# 📱 Lista de Dispositivos")

hora_atual = datetime.now().hour
if 6 <= hora_atual <= 17:
    st.image("images/IOT_dia.png")
else:
    st.image("images/IOT_noite.png")

st.subheader("Lista de dispositivos")

def fetch_all_devices():
    all_devices = []
    offset = 0
    limit = 50
    while True:
        resp = requests.get(f"{API_URL}/devices/", params={"offset": offset, "limit": limit})
        if resp.status_code != 200:
            break
        batch = resp.json()
        if not batch:
            break
        all_devices.extend(batch)
        if len(batch) < limit:
            break
        offset += limit
    return all_devices

dispositivos = fetch_all_devices()

if dispositivos:
    st.dataframe(dispositivos)

    buffer = BytesIO()
    df = pd.DataFrame(dispositivos)
    df.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)

    st.download_button(
        label="Exportar para Excel",
        data=buffer,
        file_name="dispositivos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Nenhum dispositivo encontrado")