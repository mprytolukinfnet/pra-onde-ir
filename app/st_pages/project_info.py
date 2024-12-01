import streamlit as st

st.title("Sobre o Projeto")
st.markdown("""
Desenvolvido por **Miguel Belardinelli Prytoluk** no segundo semestre de 2024.\n
**Disciplina**: Projeto de Bloco: Ciência de Dados Aplicada\n
**Instituto Infnet**
""")
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

# Links Úteis
st.header("Links Úteis")
st.markdown("[Airbnb - Hospedagens](https://www.airbnb.com/)")
st.markdown("[ODS 11 - Cidades e Comunidades Sustentáveis](https://sdgs.un.org/goals/goal11)")
st.markdown("[Projeto referência](https://nyc-venue-search.streamlit.app/)")
st.markdown("[Fonte de Dados da plataforma Airbnb](https://www.businessofapps.com/data/airbnb-statistics/)")