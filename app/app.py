import streamlit as st

st.sidebar.title("Pra Onde Ir?")

pages = {
    "Hospedagens": [
        st.Page("pages/find_listings.py", title="Busca Hospedagens"),
        st.Page("pages/airbnb_data.py", title="Dados da Plataforma Airbnb"),
    ],
    "Informações": [
        st.Page("pages/project_info.py", title="Sobre o projeto"),
    ],
}

pg = st.navigation(pages)
pg.run()