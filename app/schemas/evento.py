from datetime import datetime
from pydantic import BaseModel, Field


class EventoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100, description="Nome do evento")
    data_inicio: datetime = Field(..., description="Data e hora de início do evento")
    local: str = Field(..., min_length=1, max_length=200, description="Local de realização")
    capacidade_total: int = Field(..., gt=0, description="Capacidade total de assentos")


class EventoCreate(EventoBase):
    pass


class EventoUpdate(BaseModel):
    nome: str | None = Field(None, min_length=1, max_length=100)
    data_inicio: datetime | None = None
    local: str | None = Field(None, min_length=1, max_length=200)
    capacidade_total: int | None = Field(None, gt=0)


class EventoResponse(EventoBase):
    id: int

    class Config:
        from_attributes = True
