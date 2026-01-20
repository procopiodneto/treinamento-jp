import streamlit as st

# PÁGINAS
home_page = st.Page("home_page.py", title="Lista de Dispositivos", icon="📱")
pagina_cadastro = st.Page("pagina_cadastro.py", title="Cadastro", icon="📃")
pagina_ajustes = st.Page("pagina_ajustes.py", title="Ajustes", icon="🔧")

pg = st.navigation([home_page, pagina_cadastro, pagina_ajustes])

pg.run()