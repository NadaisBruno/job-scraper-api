# Este modulo tem como funcao pedir JSON à API para usar no streamlit

import streamlit as st
import requests
from scraper import extract_data


# app title
st.title("Job Offers Dashboard")

# o url vem de duas partes: o endereco onde o uvicorn/FastAPI esta a correr e a rota que foi criada
# em api.py(@app.get("/job_offers")
api_url = "http://127.0.0.1:8000/job_offers"


st.subheader("Scrape new job offers")
scrape_keyword = st.text_input("Enter the job you want")
scrape_city = st.text_input("Enter a city")
run_scraper = st.button("Find job offers")
# se o botao run_scraper foi clicado
if run_scraper:
    # se os campos nao foram preenchidos parar o programa
    if not scrape_keyword or not scrape_city:
        st.warning("You must enter a value")
        st.stop()
    with st.spinner("Wait a moment..."):
        # senao correr a def extract_data do modulo scraper.py
        job_metrics = extract_data(scrape_keyword, scrape_city)
    st.success("Done")


    with st.container(border=True):
        st.markdown('''
        :blue[**Scraping Summary**]
        ''')

        st.write("Job: ", job_metrics["Vaga"], "| City: ", job_metrics["City"])

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # label=texto visivel no ui // value=valor real vindo do dicionario
            st.metric("Offers found", value=job_metrics["Offers_found"])

        with col2:
            st.metric("Offers repeated", value=job_metrics["Offers_repeated"])

        with col3:
            st.metric("New offers", value=job_metrics["New_offers"])

        with col4:
            st.metric("Invalid offers", value=job_metrics["Invalid_offers"])

##


st.subheader("Filter saved job offers")
# criamos um dicionário com os filtros disponiveis
filtros = {
    "title": "Insert a title",
    "company": "Insert a company",
    "localization": "Insert the location"
}

# criamos um dicionário vazio para guardar os filtros que o utilizador preencheu
# serve para enviar filtros à API
filtros_api = {}

#
for chave, valor in filtros.items():
    # linha de codigo que cria uma caixa de texto no streamlit para cada filtro
    user_input = st.text_input(valor)
    if user_input:
        # dentro do dicionário filtros_api cria uma entrada com o nome da chave atual e guarda o texto
        # que o utilizador escreveu
        filtros_api[chave] = user_input

# inserir paginacao no streamlit com uma barra lateral(st.sidebar)
page = st.sidebar.number_input("Insert the page", min_value=1, value=1)
limit = st.sidebar.number_input("Insert the limit", min_value=1, max_value=50, value=10)

# adicionar page e limit ao dicionario filtros_api criando uma chave com o nome textual "page" e "limit" e
# guarda la o valor da variavel page
filtros_api["page"] = page
filtros_api["limit"] = limit

# request
# Docs = https://requests.readthedocs.io/en/latest/user/quickstart/?utm_source=chatgpt.com
response = requests.get(api_url, params=filtros_api, timeout=5)
if response.status_code == 404:
    st.info("No saved job offers found for these filters")
    st.stop()
elif response.status_code != 200:
    st.error("API unavailable")
    st.stop()

# pega no JSON devolvido pela API e transforma em dados Python
data = response.json()

# criamos uma tabela no streamlit para visualizar as ofertas de trabalho
st.dataframe(data)
