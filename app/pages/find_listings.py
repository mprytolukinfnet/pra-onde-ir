import streamlit as st
import pandas as pd
import httpx
import asyncio
import json

with open('config/cfg.json') as config_file:
    config = json.load(config_file)
    
api_url = config['api_url']

# Título do Projeto
st.title("Busca Hospedagens")

# Função assíncrona para fazer o POST
async def post_data_async(df_clean):
    async with httpx.AsyncClient() as client:
        url = f"{api_url}/append_listings/"
        response = await client.post(url, json=df_clean)
        return response

# Função assíncrona para fazer o GET
async def get_data_async():
    async with httpx.AsyncClient() as client:
        url = f"{api_url}/get_listings/"
        response = await client.get(url)
        full_data = pd.DataFrame(response.json())
        return full_data

# Função para rodar tarefas assíncronas dentro do Streamlit
def run_async_task(coroutine):
    return asyncio.run(coroutine)

# Realizar Upload de Arquivo CSV
st.header("Upload de Arquivo CSV para incrementar a base de dados")
uploaded_file = st.file_uploader("Faça o upload do arquivo CSV com dados extraídos do AirBnb", type="csv")
data = None

# Verificar se um arquivo foi carregado
if uploaded_file:
    # Ler o arquivo CSV
    df_split = pd.read_csv(uploaded_file, dtype={'Listing ID': 'string'})
    df_clean = df_split.where(pd.notnull(df_split), '').to_dict(orient='split')

    try:
        # Executar a função assíncrona para enviar os dados (POST)
        post_response = run_async_task(post_data_async(df_clean))

        # Checar o resultado do POST
        if post_response.status_code == 200:
            st.success("Dados adicionados com sucesso!")
        else:
            st.error(f"Erro ao adicionar dados: {post_response.status_code}")
    except httpx.ConnectError:
        st.error("Não foi possível carregar os dados pela API")

# Carregar os dados após o upload ou sempre que solicitado
st.header("Visualizar os Dados")
try:
    data = run_async_task(get_data_async())
    filtered_data = None

    regions = sorted(data['Region'].unique())
    types = sorted(data['Room Type'].unique())

    selected_regions = st.multiselect(
        "Estados",
        regions,
        ["Rio de Janeiro"],
    )

    st.write("Tipos de Hospedagem:")
    selected_types = st.multiselect(
        "Tipos de Hospedagem",
        types,
        types,
    )

    st.write("Avaliação da Hospedagem")
    rating_range = st.slider("Rating das acomodaçõçes:", 1., 5., [1.,5.])

    # Aplicar filtros se houver seleções
    if selected_regions and selected_types:
        filtered_data = data[(data['Region'].isin(selected_regions)) &
                            (data['Room Type'].isin(selected_types)) &
                            (data['Rating'] >= rating_range[0]) &
                            (data['Rating'] <= rating_range[1])]
        st.write("Dados filtrados:")
        st.dataframe(filtered_data)
    else:
        st.write("Selecione pelo menos uma região e um tipo de hospedagem para visualizar os dados.")

    # Baixar dados
    st.header("Baixar Dados")
    if filtered_data is not None:
        st.download_button(
            label="Baixar CSV",
            data=filtered_data.to_csv(index=False),
            file_name="hospedagens.csv",
            mime="text/csv"
        )
    else:
        st.write("Selecione pelo menos uma região e um tipo de hospedagem para baixar os dados.")
except httpx.ConnectError:
    st.error("Não foi possível recuperar os dados da API")