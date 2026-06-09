from pydantic import BaseModel, ConfigDict


class JobOfferResponse(BaseModel):
    id: int
    title: str
    localization: str
    date: str
    link: str
    company: str

    # permite que o Pydantic converta objetos SqlAlchemy em JSON automaticamente
    model_config = ConfigDict(from_attributes=True)

