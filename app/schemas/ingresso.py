from pydantic import BaseModel, Field


class IngressoBase(BaseModel):
    evento_id: int = Field(..., gt=0, description="ID do evento ao qual pertence")
    preco: float = Field(..., gt=0, le=10000, description="Preço do ingresso em Reais")
    tipo_assento: str = Field(..., min_length=1, max_length=50, description="Categoria de assento")
    disponivel: bool = Field(default=True, description="Se está disponível para compra")


class IngressoCreate(IngressoBase):
    pass


class IngressoUpdate(BaseModel):
    evento_id: int | None = Field(None, gt=0)
    preco: float | None = Field(None, gt=0, le=10000)
    tipo_assento: str | None = Field(None, min_length=1, max_length=50)
    disponivel: bool | None = None


class IngressoResponse(IngressoBase):
    id: int

    class Config:
        from_attributes = True
