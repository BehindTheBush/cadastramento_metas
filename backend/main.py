from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
# Não criamos tabelas automaticamente mais, usamos Alembic
# from app.core.database import engine, Base
# Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Sistema de Cadastramento de Metas",
    description="API para gerenciamento de metas e objetivos",
    version="1.0.0",
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Sistema de Cadastramento de Metas - API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}


# Import routers
from app.api import auth, users

# Register routers
app.include_router(auth.router, prefix="/api/auth", tags=["autenticacao"])
app.include_router(users.router, prefix="/api/users", tags=["usuarios"])

# TODO: Add more routers as needed
# from app.api import objetivos, indicadores
# app.include_router(objetivos.router, prefix="/api/objetivos", tags=["objetivos"])
# app.include_router(indicadores.router, prefix="/api/indicadores", tags=["indicadores"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
