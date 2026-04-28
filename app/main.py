import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

# Add parent directory to sys.path to allow running as 'python app/main.py'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import health, medicine, auth
from app.utils.errors import global_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError
from app.utils.logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    await connect_to_mongo()
    yield
    # Shutdown logic
    await close_mongo_connection()

def create_app() -> FastAPI:
    application = FastAPI(
        title="AuraCare Backend API",
        description="""
A clean, production-ready backend for the AuraCare health management system.
Built with FastAPI, Motor (Async MongoDB), and Pydantic.
        """,
        version="1.0.0",
        contact={
            "name": "AuraCare Dev Team",
            "url": "http://localhost:3000",
        },
        lifespan=lifespan
    )

    # CORS Middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS_LIST,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Error Handling
    application.add_exception_handler(Exception, global_exception_handler)
    application.add_exception_handler(RequestValidationError, validation_exception_handler)

    @application.get("/")
    async def root():
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/docs")

    # Routes
    application.include_router(health.router, prefix="/api")
    application.include_router(medicine.router, prefix="/api")
    application.include_router(auth.router, prefix="/api")

    return application

app = create_app()

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {settings.APP_NAME} on port {settings.PORT}...")
    # Run with string import to support reload
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=True)
