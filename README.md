# Projeto: Pra Onde Ir

**Teste de Performance (TP) 02**

**Disciplina:** Projeto de Bloco: Ciência de Dados Aplicada

**Aluno:** Miguel Belardinelli Prytoluk

**Data:** 23/09/2024

## Descrição do Projeto

Este projeto tem como objetivo o desenvolvimento de uma aplicação que sugere ideias de viagem, levando em consideração práticas de turismo sustentável. A aplicação é construída utilizando dados de hospedagens da plataforma Airbnb, com foco em promover escolhas conscientes e que atendam ao ODS 11: Cidades e Comunidades Sustentáveis.

## Estrutura do Projeto

A estrutura de diretórios do projeto reflete as diferentes fases do ciclo de vida do TDSP (Team Data Science Process) e CRISP-DM (Cross-Industry Standard Process for Data Mining). Abaixo está a descrição dos diretórios e arquivos principais:

### Diretórios

- **app**: Diretório contendo a aplicação demo desenvolvida em Streamlit.
  - **config**: Configurações da aplicação.
  - **model**: Modelos utilizados para previsão e recomendação de destinos.
  - **services**: Serviços auxiliares para processamento de dados.
  - **airbnb_data.csv**: Amostra dos dados de hospedagens extraídos da plataforma Airbnb.
  - **app.py**: Arquivo principal da aplicação Streamlit.
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

3. Executar a aplicação demo
  ```bash
    cd app
    streamlit run app.py 
  ```

4. (OPCIONAL) Reexecutar a raspagem de dados da plataforma Airbnb -> o arquivo `airbnb_data.csv` é gerado diretamente na pasta `data`
  ```bash
    cd scraper
    python3 fetch.py 
  ```
