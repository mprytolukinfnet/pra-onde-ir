import streamlit as st

st.sidebar.title("Pra Onde Ir?")
st.sidebar.image("../data/logo_infnet.png")

pages = {
    "Hospedagens": [
        st.Page("st_pages/find_listings.py", title="Busca Hospedagens"),
        st.Page("st_pages/airbnb_data.py", title="Dados da Plataforma Airbnb"),
    ],
    "Informações": [
        st.Page("st_pages/project_info.py", title="Sobre o projeto"),
    ],
}

pg = st.navigation(pages)
pg.run()