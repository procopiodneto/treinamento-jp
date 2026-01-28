import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://fastAPI_devices:8000")

st.markdown("# 📃   Cadastro de Dispositivos")

st.subheader("Cadastro de dispositivos")

with st.form("create_device"):
    nome = st.text_input("Nome")
    uptime = st.number_input("Uptime", min_value=0, step=1)
    contrato = st.text_input("Contrato")
    submitted = st.form_submit_button("Salvar")

    if submitted:
        nome = nome.strip()
        contrato = contrato.strip()

        if not nome:
            st.error("O campo 'Nome' e obrigatorio.")
        elif not contrato:
            st.error("O campo 'Contrato' e obrigatorio.")
        else:
            chamado_post = requests.post(
                f"{API_URL}/devices/",
                json={
                    "nome": nome,
                    "uptime": uptime,
                    "contrato": contrato
                }
            )

            if chamado_post.status_code == 201:
                st.success("Dispositivo cadastrado!")
            elif chamado_post.status_code == 409:
                st.warning("Ja existe um dispositivo com esse nome!")
            else:
                st.error(chamado_post.text)
