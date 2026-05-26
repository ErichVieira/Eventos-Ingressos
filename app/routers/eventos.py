from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.schemas.evento import EventoCreate, EventoUpdate, EventoResponse

router = APIRouter(
    prefix="/eventos",
    tags=["eventos"],
    responses={404: {"description": "Evento não encontrado"}},
)

# Armazenamento em memória (simulando um banco de dados)
eventos_db = {}
evento_id_counter = 1


@router.get("/", response_model=list[EventoResponse])
def listar_eventos():
    return list(eventos_db.values())


@router.get("/{evento_id}", response_model=EventoResponse)
def obter_evento(evento_id: int):
    if evento_id not in eventos_db:
        raise HTTPException(
            status_code=404,
            detail=f"Evento com ID {evento_id} não encontrado"
        )
    return eventos_db[evento_id]


@router.post("/", response_model=EventoResponse, status_code=201)
def criar_evento(evento: EventoCreate):
    global evento_id_counter
    novo_id = evento_id_counter
    evento_id_counter += 1
    
    novo_evento = {
        "id": novo_id,
        **evento.model_dump()
    }
    eventos_db[novo_id] = novo_evento
    
    return novo_evento


@router.put("/{evento_id}", response_model=EventoResponse)
def atualizar_evento(evento_id: int, evento_atualizado: EventoUpdate):
    if evento_id not in eventos_db:
        raise HTTPException(
            status_code=404,
            detail=f"Evento com ID {evento_id} não encontrado"
        )
    
    evento_existente = eventos_db[evento_id]
    dados_atualizacao = evento_atualizado.model_dump(exclude_unset=True)
    evento_existente.update(dados_atualizacao)
    
    return evento_existente


@router.delete("/{evento_id}", status_code=204)
def deletar_evento(evento_id: int):
    if evento_id not in eventos_db:
        raise HTTPException(
            status_code=404,
            detail=f"Evento com ID {evento_id} não encontrado"
        )
    
    del eventos_db[evento_id]
