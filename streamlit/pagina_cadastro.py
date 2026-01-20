import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.markdown("# 📃   Cadastro de Dispositivos")
st.sidebar.markdown("# Cadastro de Dispositivos")

st.subheader("Cadastro de dispositivos")

with st.form("create_device"):
    nome = st.text_input("Nome")
    uptime = st.number_input("Uptime", min_value=0, step=1)
    contrato = st.text_input("Contrato")
    submitted = st.form_submit_button("Salvar")

    if submitted:
        chamado_post = requests.post(
            f"{API_URL}/devices/",
            json={
                "nome": nome,
                "uptime": uptime,
                "contrato": contrato
            }
        )

        if chamado_post.status_code == 200:
            st.success("Dispositivo cadastrado!")
        else:
            st.error(chamado_post.text)
