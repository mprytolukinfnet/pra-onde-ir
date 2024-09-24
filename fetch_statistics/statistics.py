import requests
from bs4 import BeautifulSoup
import csv

# URL da página (ou carregue o HTML localmente)
url = 'https://www.businessofapps.com/data/airbnb-statistics/'
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

# Fazendo a requisição HTTP para obter o HTML da página
response = requests.get(url, headers=headers)

# Parsing do HTML com BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Localizar todas as tabelas na página
tables = soup.find_all('table')

# Iterar sobre todas as tabelas encontradas
for table in tables:
    # Obter o nome da tabela pelo atributo aria-label
    table_name = table.get('aria-label')
    
    # Se a tabela tiver um nome válido
    if table_name and table_name != 'Airbnb overview':
        print(f"Extraindo dados da tabela: {table_name}")

        # Extrair cabeçalhos (th)
        headers = [th.get_text(strip=True) for th in table.find_all('th')]

        # Extrair linhas de dados (td)
        rows = []
        for row in table.find_all('tr')[1:]:  # Ignorando a linha de cabeçalho
            cols = [td.get_text(strip=True) for td in row.find_all('td')]
            rows.append(cols)

        # Salvar os dados da tabela em um arquivo CSV com o nome da tabela
        file_name = f"../data/{table_name.replace(' ', '_').lower()}.csv"
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Escrever cabeçalhos
            writer.writerows(rows)  # Escrever as linhas de dados

        print(f"Tabela '{table_name}' salva como {file_name}")
