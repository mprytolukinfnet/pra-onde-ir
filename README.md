# Projeto: Pra Onde Ir?

**Teste de Performance (TP) 03**

**Disciplina:** Projeto de Bloco: Ciência de Dados Aplicada

**Aluno:** Miguel Belardinelli Prytoluk

**Data:** 21/10/2024

## Descrição do Projeto

Este projeto tem como objetivo o desenvolvimento de uma aplicação que sugere ideias de viagem, levando em consideração práticas de turismo sustentável. A aplicação é construída utilizando dados de hospedagens da plataforma Airbnb, com foco em promover escolhas conscientes e que atendam ao ODS 11: Cidades e Comunidades Sustentáveis.

## Estrutura do Projeto

A estrutura de diretórios do projeto reflete as diferentes fases do ciclo de vida do TDSP (Team Data Science Process) e CRISP-DM (Cross-Industry Standard Process for Data Mining). Abaixo está a descrição dos diretórios e arquivos principais:

### Diretórios

- **app**: Diretório contendo a aplicação demo desenvolvida em Streamlit.
  - **config**: Configurações da aplicação.
    - **cfg.json**: Arquivo de configurações da aplicação
  - **model**: Modelos utilizados para previsão e recomendação de destinos.
  - **services**: Serviços auxiliares para processamento de dados.
  - **pages**: Páginas da aplicação Streamlit.
  - **app.py**: Arquivo principal da aplicação Streamlit.
- **api**: Diretório contendo a API da aplicação, necessária para a execução
  - **api.py**: Arquivo principal da API da aplicação.
  - **DataFrameInput.py**: Modelo que representa o DataFrame de entrada para o Endpoint de adicionar hospedagens na API
  - **ListingResponse.py**: Modelo que representa a saída para o Endpoint de obter hospedagens da API
- **data**: Diretório contendo bases de dados utilizadas no projeto.
- **docs**: Diretório para documentação do projeto, dividido em duas seções:
  - **business docs**: Documentos relacionados ao negócio, como o Business Model Canvas e o Project Charter.
  - **data docs**: Documentos relacionados aos dados, como o Data Summary Report.
- **fetch_statistics**: Diretório contendo o código de scraping de estatísticas da plataforma Airbnb
  - **statistics.py**: Script para extrair estatísticas da plataforma Airbnb
- **scraper**: Diretório contendo o código de scraping para coleta de dados da plataforma Airbnb.
  - **AirbnbScraper.py**: Classe de scraping dos dados do Airbnb.
  - **fetch.py**: Script auxiliar para coleta de dados.
- **.gitignore**: Arquivo para excluir arquivos e diretórios desnecessários do controle de versão.
- **Dockerfile**: Arquivo para criação de um contêiner Docker, facilitando a implementação da aplicação.
- **requirements.txt**: Lista de bibliotecas e dependências necessárias para rodar a aplicação.

### Documentos

- **Business Model Canvas.md**: Documento descrevendo o modelo de negócio da aplicação.
- **Project Charter.md**: Documento que define o escopo, objetivos e stakeholders do projeto.
- **Data Summary Report.md**: Relatório com a descrição das fontes de dados utilizadas no projeto.

## Como Executar a Aplicação

### Requisitos

- Python 3.12+
- Bibliotecas listadas no `requirements.txt`

### Instruções

1. Criar Ambiente virtual e Ativar

  ```bash
    virtualenv .venv
    source .venv/bin/activate
  ```

2. Instalar Bibliotecas Necessárias

  ```bash
    pip install -r requirements.txt
  ```

3. Executar a API
  ```bash
    cd api
    uvicorn api:app --reload
  ```
  - É possível configurar o endereço que aplicação consulta a api no arquivo `/app/config/cfg.json`
  - Após a execução da API, é possível acessar a sua documentação em http://127.0.0.1:8000/docs (altere caso seja utilizada outra url)


4. Executar a aplicação Streamlit
  ```bash
    cd app
    streamlit run app.py 
  ```

5. (OPCIONAL) Reexecutar a raspagem de dados da plataforma Airbnb -> o arquivo `airbnb_data.csv` é gerado diretamente na pasta `data`
  ```bash
    cd scraper
    python3 fetch.py 
  ```
  - Recomendado utilizar um VPN para fazer a extração, pois o Airbnb pode bloquear o IP após múltiplas requisições.

6. (OPCIONAL) Reexecutar a raspagem das estatísticas da plataforma Airbnb -> os seguintes arquivos são gerados diretamente na pasta `data`:
- `airbnb_annual_net_income.csv`
- `airbnb_annual_revenue.csv`
- `airbnb_bookings.csv`
- `airbnb_booking_volume.csv`
- `airbnb_listings.csv`
- `airbnb_users.csv`

```bash
  cd fetch_statistics
  python3 statistics.py 
```