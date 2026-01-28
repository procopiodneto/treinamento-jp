import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://fastAPI_devices:8000")

st.markdown("# 🔧 Ajuste de Dispositivos")

st.subheader("Cadastro de dispositivos")

#ENCONTRAR DISPOSITIVO
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

devices = fetch_all_devices()

if not devices:
    st.info("Nenhum dispositivo cadastrado")
    st.stop()

#SELECIONAR DISPOSITIVO PARA EXIBIR
busca = st.text_input("Buscar dispositivo por nome", "")

device_map = {}
for d in devices:
    chave = f"{d['id']} - {d['nome']}"
    if busca.strip() == "" or busca.strip().lower() in d['nome'].lower():
        device_map[chave] = d

if not device_map:
    st.warning("Nenhum dispositivo encontrado com esse filtro")
    st.stop()

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