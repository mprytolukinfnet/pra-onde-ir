import streamlit as st
from streamlit_carousel import carousel
import httpx

from services.query_vectors import search_similar_listings
from services.controllers import change_query, select_next_listing, get_data, get_description_and_pictures, select_best_listing

# Title
st.title("Busca Hospedagens")

# Initialize session state
state = st.session_state

if '_query' not in state:
    state._query = ''
if 'description_complete' not in state:
    state.description_complete = False

NUM_SIMILAR_LISTINGS = 5

try:
    data = get_data()
    data["Listing ID"] = data["Listing ID"].astype(int)
    prompt_col1, prompt_col2 = st.columns([8, 2])
    with prompt_col1:
        st.text_area(
            "Descreva o que você quer numa hospedagem:",
            placeholder="E.g., Quero uma casa com cachoeira",
            value=state._query,
            key='query',
            on_change=change_query,
        )
    with prompt_col2:
        for _ in range(3):
            st.text("")
        st.button(label="Buscar hospedagem!", on_click=lambda:select_next_listing(NUM_SIMILAR_LISTINGS))

    if state.query:
        with st.spinner("Carregando sua resposta..."):
            if 'similar_listings' not in state:
                state.similar_listings = search_similar_listings(state.query, n=NUM_SIMILAR_LISTINGS)

            if state.similar_listings:
                select_best_listing(data, NUM_SIMILAR_LISTINGS)

                st.subheader(state.best_listing['Name'])
                st.markdown(f"[Veja no Airbnb](https://www.airbnb.com.br/rooms/{state.best_listing['Listing ID']})", unsafe_allow_html=True)

                col1, col2 = st.columns([3, 2])
                img_placeholders = {
                    "cover_placeholder": col1.empty(),
                    "carousel_placeholder": col1.empty(),
                    "carousel_container": col1.empty()
                }
                text_placeholder = col2.empty()

                if not state.description_complete or 'pictures' not in state:
                    get_description_and_pictures(text_placeholder, img_placeholders)

                if 'pictures' in state:
                    img_placeholders['cover_placeholder'].image(state.pictures[0], use_column_width=True)
                    carousel_items = [dict(title="", text="", img=pic) for pic in state.pictures[1:]]
                    img_placeholders['carousel_placeholder'].write("### Outras fotos:")
                    img_placeholders['carousel_container'].empty()
                    with img_placeholders['carousel_container'].container():
                        carousel(items=carousel_items, key=f"carousel_sync")

                if 'descriptive_text' in state:
                    text_placeholder.write(state.descriptive_text)
                else:
                    text_placeholder.write("Carregando descrição personalizada...")
            else:
                st.warning("Nenhuma hospedagem similar encontrada. Tente refinar sua consulta.")
except httpx.ConnectError:
    st.error("Não foi possível recuperar os dados da API")
