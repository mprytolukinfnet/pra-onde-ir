import streamlit as st

st.sidebar.title("Pra Onde Ir?")
st.sidebar.image("app/st_pages/logo_infnet.png")

pages = {
    "Hospedagens": [
        st.Page("app/st_pages/find_listings.py", title="Busca Hospedagens"),
        st.Page("app/st_pages/airbnb_data.py", title="Dados da Plataforma Airbnb"),
    ],
    "Informações": [
        st.Page("app/st_pages/project_info.py", title="Sobre o projeto"),
    ],
}

pg = st.navigation(pages)
pg.run()