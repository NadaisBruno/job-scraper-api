from fastapi import FastAPI, HTTPException, Query
from database import JobOffer, Session
from schema import JobOfferResponse

app = FastAPI()


@app.get("/job_offers", response_model=list[JobOfferResponse])
def list_job_offers(title: str = None, localization: str = None, company: str = None, page: int = Query(default=1, ge=1)
                    , limit: int = Query(default=10, ge=1, le=50)):
    # ligacao a db
    db = Session()
    # consulta a classe JobOffer em database.py
    query = db.query(JobOffer)
    if title:
        # EXEMPLO:
        # %python% contem python em qualquer lugar
        # python% comeca por python
        # %python acaba em python
        # python procura exatamente python
        query = query.filter(JobOffer.title.ilike(f"%{title}%"))  # ilike()=lower()
    if localization:
        query = query.filter(JobOffer.localization.ilike(f"%{localization}%"))
    if company:
        query = query.filter(JobOffer.company.ilike(f"%{company}%"))


    # permite mostrar apenas a pagina pedida pelo utilizar/ignora ofertas de paginas anteriores
    offset = (page - 1) * limit
    # aplicamos paginacao a query e executa-a com os filtros aplicados
    offers = query.offset(offset).limit(limit).all()

    if not offers:
        raise HTTPException(status_code=404, detail="Oferta não encontrada")

    return offers
