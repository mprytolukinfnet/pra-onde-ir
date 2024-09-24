import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título do Projeto
st.title("Plataforma de Recomendação de Hospedagens Sustentáveis")

# Descrição do Problema de Negócio e Objetivos
st.header("Descrição do Problema de Negócio")
st.write("""
Com o crescente interesse por turismo sustentável e experiências únicas, há uma demanda por ferramentas que ajudem os viajantes a encontrar hospedagens que estejam alinhadas com práticas sustentáveis e que ofereçam uma experiência autêntica.
Este projeto visa desenvolver uma aplicação que sugira hospedagens do Airbnb que estejam em conformidade com os critérios de sustentabilidade do ODS 11.
""")

st.header("Objetivos do Projeto")
st.write("""
- Coletar e analisar dados de hospedagens do Airbnb.
- Desenvolver um sistema de recomendação que considere fatores como proximidade a áreas naturais e práticas sustentáveis.
- Criar uma aplicação web intuitiva para apresentar essas recomendações aos usuários.
""")

# Realizar Upload de Arquivo CSV
st.header("Upload de Arquivo CSV para incrementar a base de dados")
uploaded_file = st.file_uploader("Faça o upload do arquivo CSV com dados extraídos do AirBnb", type="csv")

# Amostra dos Dados
st.header("Visualizar os Dados")

@st.cache_data
def load_data(uploaded_file):
    default_data = pd.read_csv('../data/airbnb_data.csv', dtype={'Listing ID': 'string'})
    full_data = default_data
    # Merge uploaded data
    if uploaded_file:
        new_data = pd.read_csv(uploaded_file, dtype={'Listing ID': 'string'})
        print(new_data)
        full_data = pd.concat([default_data, new_data]).drop_duplicates(subset='Listing ID', keep='first')

    return full_data

# Carregar os dados
data = load_data(uploaded_file)

filtered_data = None

regions = sorted(data['Region'].unique())
types = sorted(data['Room Type'].unique())

selected_regions = st.multiselect(
    "Estados",
    regions,
    ["Rio de Janeiro"],
)

st.write("Tipos de Hospedagem:")
# st.checkbox("Selecionar/Desselecionar todos", value=True, key=f'all_types', on_change=select_all_types)
selected_types = [type_ for type_ in types if st.checkbox(type_, value=True, key=f'type_{type_}')]

st.write("Avaliação da Hospedagem")
rating_range = st.slider("Rating das acomodaçõçes:", 1, 5, [1,5])

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

# Dados da plataforma Airbnb
st.header("Dados da plataforma Airbnb")

@st.cache_data
def load_statistics(file_name):
    return pd.read_csv(f'../data/{file_name}')

# Listagem dos arquivos CSV e seus respectivos títulos
data_files = {
    'Listagens do Airbnb': 'airbnb_listings.csv',
    'Lucro Líquido Anual do Airbnb': 'airbnb_annual_net_income.csv',
    'Usuários do Airbnb': 'airbnb_users.csv',
    'Receita Anual do Airbnb': 'airbnb_annual_revenue.csv',
    'Reservas do Airbnb': 'airbnb_bookings.csv',
    'Volume de Reservas do Airbnb': 'airbnb_booking_volume.csv',
}


# Dropdown para selecionar qual série temporal visualizar
option = st.selectbox("Selecione a série temporal que deseja visualizar:", list(data_files.keys()))

# Carregar os dados do arquivo CSV selecionado
df_statistics = load_statistics(data_files[option])

# Plotar o gráfico de linha
st.write(f"Gráfico de {option}:")

# Certifique-se de que o DataFrame tem as colunas "Year" e "Value"
if 'Year' in df_statistics.columns and len(df_statistics.columns) > 1:
    # Supondo que a coluna "Year" contenha os anos e a outra coluna contenha os valores
    plt.figure(figsize=(10, 6))
    plt.plot(df_statistics['Year'], df_statistics[df_statistics.columns[1]], marker='o')
    plt.title(f'{option} ao longo dos anos')
    plt.xlabel('Ano')
    plt.ylabel(df_statistics.columns[1])
    plt.grid(True)

    # Exibir o gráfico no Streamlit
    st.pyplot(plt)
else:
    st.write("Formato inesperado nos dados.")

# Links Úteis
st.header("Links Úteis")
st.markdown("[Airbnb - Hospedagens](https://www.airbnb.com/)")
st.markdown("[ODS 11 - Cidades e Comunidades Sustentáveis](https://sdgs.un.org/goals/goal11)")
st.markdown("[OpenStreetMap](https://www.openstreetmap.org/)")
st.markdown("[Projeto referência](https://nyc-venue-search.streamlit.app/)")
st.markdown("[Fonte de Dados da plataforma Airbnb](https://www.businessofapps.com/data/airbnb-statistics/)")