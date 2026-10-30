from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import engine, Base
from app.api.v1.task_router import router as task_router

# Crear las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow API",
    description="API REST para la gestión y organización de tareas académicas en Android.",
    version="1.0.0"
)

# Configuración CORS para permitir peticiones desde la app Android
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(task_router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
def root():
    return {
        "app": "TaskFlow API",
        "mensaje": "Organiza tus tareas y mantén tus entregas al día",
        "status": "online"
    }