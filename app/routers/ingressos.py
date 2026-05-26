from fastapi import APIRouter, HTTPException

from app.schemas.ingresso import IngressoCreate, IngressoUpdate, IngressoResponse
from app.routers.eventos import eventos_db

router = APIRouter(
    prefix="/ingressos",
    tags=["ingressos"],
    responses={404: {"description": "Ingresso não encontrado"}},
)

# Armazenamento em memória (simulando um banco de dados)
ingressos_db = {}
ingresso_id_counter = 1


@router.get("/", response_model=list[IngressoResponse])
def listar_ingressos():
    return list(ingressos_db.values())


@router.get("/{ingresso_id}", response_model=IngressoResponse)
def obter_ingresso(ingresso_id: int):
    if ingresso_id not in ingressos_db:
        raise HTTPException(
            status_code=404,
            detail=f"Ingresso com ID {ingresso_id} não encontrado"
        )
    return ingressos_db[ingresso_id]


@router.get("/eventos/{evento_id}/ingressos", response_model=list[IngressoResponse])
def listar_ingressos_por_evento(evento_id: int):
    if evento_id not in eventos_db:
        raise HTTPException(
            status_code=404,
            detail=f"Evento com ID {evento_id} não encontrado"
        )
    
    ingressos_evento = [
        ing for ing in ingressos_db.values()
        if ing["evento_id"] == evento_id
    ]
    return ingressos_evento


@router.post("/", response_model=IngressoResponse, status_code=201)
def criar_ingresso(ingresso: IngressoCreate):
    # Validar se o evento existe
    if ingresso.evento_id not in eventos_db:
        raise HTTPException(
            status_code=400,
            detail=f"Evento com ID {ingresso.evento_id} não existe"
        )
    
    global ingresso_id_counter
    novo_id = ingresso_id_counter
    ingresso_id_counter += 1
    
    novo_ingresso = {
        "id": novo_id,
        **ingresso.model_dump()
    }
    ingressos_db[novo_id] = novo_ingresso
    
    return novo_ingresso


@router.put("/{ingresso_id}", response_model=IngressoResponse)
def atualizar_ingresso(ingresso_id: int, ingresso_atualizado: IngressoUpdate):
    if ingresso_id not in ingressos_db:
        raise HTTPException(
            status_code=404,
            detail=f"Ingresso com ID {ingresso_id} não encontrado"
        )
    
    # Validar evento se for atualizado
    if ingresso_atualizado.evento_id is not None:
        if ingresso_atualizado.evento_id not in eventos_db:
            raise HTTPException(
                status_code=400,
                detail=f"Evento com ID {ingresso_atualizado.evento_id} não existe"
            )
    
    ingresso_existente = ingressos_db[ingresso_id]
    dados_atualizacao = ingresso_atualizado.model_dump(exclude_unset=True)
    ingresso_existente.update(dados_atualizacao)
    
    return ingresso_existente


@router.delete("/{ingresso_id}", status_code=204)
def deletar_ingresso(ingresso_id: int):
    if ingresso_id not in ingressos_db:
        raise HTTPException(
            status_code=404,
            detail=f"Ingresso com ID {ingresso_id} não encontrado"
        )
    
    del ingressos_db[ingresso_id]
