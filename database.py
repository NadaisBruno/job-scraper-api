from sqlalchemy import create_engine  # serve para gerir a conexao entre o python e a db
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker

# criamos a ligacao ao ficheiro jobs.db
engine = create_engine("sqlite:///jobs.db")

# classe pai de todos os modelos
Base = declarative_base()

# Comunicar com a base de dados
Session = sessionmaker(bind=engine)


class JobOffer(Base):
    __tablename__ = "joboffers"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
    localization = Column(String, index=True, nullable=False)
    date = Column(String, index=True, nullable=False)
    link = Column(String, nullable=False, unique=True)
    company = Column(String, index=True, nullable=False)


# def que serve para verificar se a oferta de trabalho é repetida
def job_exist(link):
    # ligacao a db
    db = Session()
    # procurar na tabela JobOffer uma vaga com este link
    # seleciona(select) JobOffer onde(where) o campo JobOffer seja igual ao link recebido
    query = select(JobOffer).where(JobOffer.link == link)
    # executar a consulta na db
    resultado = db.execute(query)
    # scalars=extrai os objectos JobOffer do resultado
    # first=vai buscar o primeiro ou None se nao existir
    job = resultado.scalars().first()
    if job:
        vaga_exist = True
    else:
        vaga_exist = False

    db.close()

    return vaga_exist


job_exist("/15416533/mid-python-developer-presencial-lisboa/")


# Cria a tabela no engine
Base.metadata.create_all(engine)
