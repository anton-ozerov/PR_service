import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config.logging import setup_logging
from app.middleware import DocsAuthMiddleware
from app.routers import auth_router, users_router, teams_router, pull_request_router, health_router


# Инициализация логирования
setup_logging()


app = FastAPI(
    title="Сервис назначения ревьюеров для Pull Request’ов",
    description="FastAPI приложение для PR",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# кастомные middleware
app.add_middleware(DocsAuthMiddleware)

# routers
app.include_router(auth_router, prefix="/auth")
app.include_router(users_router, prefix="/users")
app.include_router(teams_router, prefix="/team")
app.include_router(pull_request_router, prefix="/pullRequest")
app.include_router(health_router, prefix="/health")
print("test")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
