# Data Summary Report

## 1. **Resumo do Projeto**
Este relatório fornece uma visão geral das fontes de dados que serão utilizadas no projeto para sugerir ideias de viagem e oferecer recomendações personalizadas de hospedagem. O projeto se alinha ao Objetivo de Desenvolvimento Sustentável (ODS) 11: Cidades e Comunidades Sustentáveis.

## 2. **Fontes de Dados**

### 2.1 **Dados de Hospedagem**
- **Fonte:** Dados extraídos da plataforma Airbnb
- **Descrição:** Contém informações sobre as hospedagens disponíveis, incluindo localização, preço, tipo de acomodação, avaliações, descrição e lista de comodidades.
- **Uso:** Utilizado para gerar recomendações personalizadas de hospedagem com base nas preferências do usuário.
- **Campos Principais:**
  - `Region`: Região ou estado onde a hospedagem está localizada.
  - `Listing ID`: Identificação única da hospedagem.
  - `Name`: Nome da hospedagem.
  - `Room Type`: Tipo de acomodação (ex.: casa inteira, quarto privado).
  - `Person Capacity`: Número máximo de hóspedes na hospedagem.
  - `Price per Night (R$)`: Preço por noite em Reais.
  - `Rating`: Avaliação média da hospedagem.
  - `Reviews`: Número de avaliações.
  - `Latitude` e `Longitude`: Coordenadas geográficas da hospedagem.
  - `Badge`: Distintivos ou selos (ex.: Superhost, Preferido dos hóspedes).
  - `Description`: Descrição detalhada da hospedagem.
  - `Amenities`: Lista de comodidades disponíveis.
  - `Pictures`: URLs das imagens da hospedagem.

### 2.2 **Estatísticas da plataforma Airbnb**
- **Fonte:** Dados extraídos da página BusinessOfApps (https://www.businessofapps.com/data/airbnb-statistics/)
- **Descrição:** Os dados fornecem uma visão geral da evolução financeira e operacional da plataforma Airbnb, incluindo lucros, receitas, volume de reservas e crescimento de usuários ao longo dos anos. As informações cobrem aspectos como receita anual, número de reservas, valor bruto das reservas, número de listagens e usuários da plataforma.
- **Uso:** Estes dados são usados para entender o desempenho financeiro da Airbnb, analisar o crescimento da base de usuários e avaliar o impacto da plataforma no mercado de turismo e hospedagem. É utilizado na aplicação Streamlit.
- **Campos Principais:**
  - `Year`: Ano em que os dados foram coletados.
  - `Net income/loss ($mm)`: Lucro líquido ou prejuízo da Airbnb em milhões de dólares.
  - `Revenue ($bn)`: Receita anual da Airbnb em bilhões de dólares.
  - `Gross booking value ($bn)`: Valor bruto das reservas realizadas na plataforma, em bilhões de dólares.
  - `Bookings (mm)`: Número total de reservas realizadas na plataforma em milhões.
  - `Listings (mm)`: Número total de listagens de imóveis disponíveis na plataforma, em milhões.
  - `Users (mm)`: Número total de usuários da plataforma, em milhões.

## 3. **Objetivo de Uso dos Dados**
- **Personalização:** Utilizar os dados para fornecer recomendações personalizadas com base nas preferências dos usuários.
- **Visualização:** Mapear as localizações das hospedagens e suas proximidades com pontos de interesse.
- **Entendimento do Mercado:** Utilizar as estatísticas da plataforma Airbnb para entender melhor o mercado em que a aplicação está inserida.

## 4. **Considerações Finais**
Este relatório será continuamente atualizado conforme o progresso do projeto e a inclusão de novas fontes de dados.
