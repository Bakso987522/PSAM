from fastapi import FastAPI

from app.routers import alternatives, products, search, suggest, system

app = FastAPI(
    title="Agrolupa API",
    description="Backend API wyszukiwarki środków ochrony roślin (ŚOR)",
    version="1.3.0",
)

for module in (system, suggest, search, products, alternatives):
    app.include_router(module.router)