import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Dados da plataforma Airbnb
st.title("Dados da plataforma Airbnb")
@st.cache_data
def load_statistics(file_name):
    return pd.read_csv(f'data/{file_name}')

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