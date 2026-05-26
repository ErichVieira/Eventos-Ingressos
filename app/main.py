from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.routers import eventos, ingressos

# Criação da aplicação FastAPI
app = FastAPI(
    title="API de Eventos e Ingressos",
    description="API REST para gerenciamento de eventos e ingressos de entrada",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# Registro dos routers
app.include_router(eventos.router)
app.include_router(ingressos.router)


@app.get("/", tags=["root"])
def raiz():
    return {
        "mensagem": "Bem-vindo à API de Eventos e Ingressos",
        "versao": "1.0.0",
        "documentacao": "/docs",
        "endpoints": {
            "eventos": "/eventos",
            "ingressos": "/ingressos",
        }
    }


@app.get("/saude", tags=["root"])
def verificar_saude():
    return {"status": "operacional"}


@app.exception_handler(Exception)
async def manipulador_excecao_global(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detalhe": "Erro interno do servidor"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
