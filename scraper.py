# Este modulo tem como funcao pedir HTML ao `net-empregos

import requests
from bs4 import BeautifulSoup
from database import JobOffer, Session, job_exist


def extract_data(keyword, city):
    url = f"https://www.net-empregos.com/pesquisa-empregos.asp?chaves={keyword}&cidade={city}&categoria=0&zona=0&tipo=0"
    try:  # try/except para falhas de pedido com temporizador de 10 segundos
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        print("Erro ao ceder site:", e)
        return

    # se der erro ao aceder o site...
    if response.status_code != 200:
        print("Erro ao aceder o site")
        return
    # se nao der erro(code 200) continua e extrai o HTML de data
    data = response.text

    # creating a BeautifulSoup object
    soup = BeautifulSoup(data, "html.parser")

    # abrimos uma ligacao a base de dados apos o beautiful soup
    db = Session()

    # encontramos todas as ofertas de emprego na página(neste caso a tag usada pelo ‘developer’ do site para cada oferta é div)
    offers = soup.find_all("div", class_="job-item media")
    # contador de vagas encontradas na pagina
    contador_vagas_encontradas = 0
    contador_vagas_repetidas = 0
    contador_vagas_novas = 0
    contador_vagas_invalidas = 0


    for offer in offers:
        # contador dentro do for e antes das verificacoes
        contador_vagas_encontradas += 1

        tag_a = offer.find("a")
        if not tag_a:
            contador_vagas_invalidas += 1
            continue

        # find the title of the job offer
        title = tag_a.text.lower()
        if not title:
            contador_vagas_invalidas += 1
            continue

        # find the link of the job offer
        # obter o link da oferta de forma segura
        # o link está guardado no atributo href da tag <a>
        # usamos .get("href") em vez de tag_a["href"]
        # porque .get("href") devolve None se o atributo href não existir,
        # evitando que o programa rebente com erro
        link = tag_a.get("href")
        if not link:
            contador_vagas_invalidas += 1
            continue

        # verify if this job offer already exists
        # if the link already exist we skip the job offer(link) with continue
        if job_exist(link):
            # contador de vagas repetidas
            contador_vagas_repetidas += 1
            continue

        # verify if the company icon already exists
        # if it does not exist we skip with continue the offer
        company_icon = offer.find(class_="flaticon-work")
        if not company_icon:
            contador_vagas_invalidas += 1
            continue
        # find the company of the job offer // usar strip para remover espacos extra que possam eventualmente aparecer
        company = company_icon.parent.text.strip().lower()

        # verify if the date icon already exists
        # if it does not exist we skip with continue
        date_icon = offer.find(class_="flaticon-calendar")
        if not date_icon:
            contador_vagas_invalidas += 1
            continue
        date = date_icon.parent.text.strip().lower()

        # verify if the localization icon already exist
        # if it does not exist we skip with continue
        localization_icon = offer.find(class_="flaticon-pin")
        if not localization_icon:
            contador_vagas_invalidas += 1
            continue
        localization = localization_icon.parent.text.strip().lower()

        # criamos a instancia job_offer
        new_job_offer = JobOffer(
            title=title,
            localization=localization,
            date=date,
            link=link,
            company=company
        )
        # adicionamos o objeto new_job_offer a db
        db.add(new_job_offer)
        # contador de vagas novas
        contador_vagas_novas += 1

    #
    db.commit()

    db.close()

    print(f"Vaga: {keyword} | Cidade: {city}")
    # mostrar total de vagas encontradas
    print("Total de vagas encontradas: ", contador_vagas_encontradas)
    # mostrar o total de repetidas
    print("Total de vagas repetidas: ", contador_vagas_repetidas)
    # mostrar o total de vagas novas
    print("Total de novas vagas: ", contador_vagas_novas)
    # mostrar o total de vagas invalidas
    print("Total de vagas inválidas: ", contador_vagas_invalidas)

    # criamos um dicionário para depois ser apresentado na ui do streamlit com as metricas dos contadores
    # poderia usar listas ou tuplas para agrupar varios valores, mas o ideal e um dicionário porque cada valor tem um nome(chave:valor) ficando bem mais intuitivo
    job_offers_metrics = {
        "Vaga": keyword,
        "City": city,
        "Offers_found": contador_vagas_encontradas,
        "Offers_repeated": contador_vagas_repetidas,
        "New_offers": contador_vagas_novas,
        "Invalid_offers": contador_vagas_invalidas
    }
    return job_offers_metrics
