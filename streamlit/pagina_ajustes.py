import streamlit as st
import requests

API_URL = "http://fastAPI_devices:8000"

st.markdown("# 🔧 Ajuste de Dispositivos")
st.sidebar.markdown("# Ajustes")

st.subheader("Cadastro de dispositivos")

#ENCONTRAR DISPOSITIVO
chamado_get = requests.get(f"{API_URL}/devices/")

if chamado_get.status_code != 200:
    st.error("Erro ao buscar dispositivos")
    st.stop()

devices = chamado_get.json()

if not devices:
    st.info("Nenhum dispositivo cadastrado")
    st.stop()

#SELECIONAR DISPOSITIVO PARA EXIBIR
device_map = {}

for d in devices:
    chave = f"{d['id']} - {d['nome']}"
    device_map[chave] = d

selecao_de_ajuste = st.selectbox(
    "Selecione um dispositivo",
    device_map.keys()
)

device = device_map[selecao_de_ajuste]

st.divider()

st.subheader("Dados atuais")

st.json(device)

#ATUALIZAÇÃO DO DISPOSITIVO
st.subheader("Atualizar dispositivo")

with st.form("update_device"):
    nome = st.text_input("Nome", value=device["nome"])
    uptime = st.number_input(
        "Uptime",
        min_value=0,
        value=device["uptime"],
        step=1
    )
    contrato = st.text_input("Contrato", value=device["contrato"])

    botao_atualizar = st.form_submit_button("Atualizar")

    if botao_atualizar:
        device_mod = {}
        
        if nome != device["nome"]:
            device_mod["nome"] = nome
        if uptime != device["uptime"]:
            device_mod["uptime"] = uptime
        if contrato != device["contrato"]:
            device_mod["contrato"] = contrato

        if not device_mod:
            st.warning("Nenhuma alteração detectada")
        else:
            chamado_patch = requests.patch(
                f"{API_URL}/devices/{device['id']}",
                json=device_mod
            )

            if chamado_patch.status_code == 200:
                st.success("Dispositivo atualizado com sucesso!")
                st.rerun()
            else:
                st.error(chamado_patch.text)

#APAGAR DISPOSITIVO
st.divider()
st.subheader("Deletar dispositivo")

if st.button("🗑️ Deletar dispositivo", type="primary"):
    chamado_delete = requests.delete(
        f"{API_URL}/devices/{device['id']}"
    )

    if chamado_delete.status_code == 200:
        st.success("Dispositivo deletado com sucesso!")
        st.rerun()
    else:
        st.error(chamado_delete.text)