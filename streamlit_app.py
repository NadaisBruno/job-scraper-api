# Este modulo tem como funcao pedir JSON à API para usar no streamlit


import streamlit as st
import requests

# app title
st.title("Job Offers Dashboard")

# o url vem de duas partes: o endereco onde o uvicorn/FastAPI esta a correr e a rota que foi criada
# em api.py(@app.get("/job_offers")
api_url = "http://127.0.0.1:8000/job_offers"

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

# request
# Docs = https://requests.readthedocs.io/en/latest/user/quickstart/?utm_source=chatgpt.com
response = requests.get(api_url, params=filtros_api, timeout=5)
if response.status_code == 404:
    st.warning("Não há resultados para esse filtro")
    st.stop()
elif response.status_code != 200:
    st.error("API indisponivel")
    st.stop()

# pega no JSON devolvido pela API e transforma em dados Python
data = response.json()

# criamos uma tabela no streamlit para visualizar as ofertas de trabalho
st.dataframe(data)
