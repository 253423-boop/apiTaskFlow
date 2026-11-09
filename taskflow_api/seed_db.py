from datetime import datetime, timedelta
from app.core.config import SessionLocal, engine, Base
from app.models.user_model import UserModel
from app.models.task_model import TaskModel
from app.domain.enums import TaskStatus
from app.core.security import get_password_hash

def init_and_seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(UserModel).count() > 0:
            print("⚠️ La base de datos ya contiene datos.")
            return

        # Crear un usuario de prueba
        hashed_pw = get_password_hash("password123")
        user = UserModel(nombre="Test User", correo="test@example.com", hashed_password=hashed_pw)
        db.add(user)
        db.commit()
        db.refresh(user)

        now = datetime.now()

        # Tareas vinculadas al usuario
        tareas_prueba = [
            TaskModel(user_id=user.id, titulo="Reporte de Redes", materia="Redes", descripcion="Documentar topología y protocolos", fecha_entrega=now + timedelta(days=1), estado=TaskStatus.PENDIENTE, prioridad=3),
            TaskModel(user_id=user.id, titulo="Práctica de Estructura", materia="Estructura de Datos", descripcion="Implementar árboles binarios", fecha_entrega=now + timedelta(days=4), estado=TaskStatus.PENDIENTE, prioridad=2),
            TaskModel(user_id=user.id, titulo="Investigación UX", materia="Aplicaciones Web", descripcion="Análisis heurístico de usabilidad", fecha_entrega=now - timedelta(days=2), estado=TaskStatus.PENDIENTE, prioridad=1),
            TaskModel(user_id=user.id, titulo="Definir arquitectura", materia="Backend", descripcion=None, fecha_entrega=now - timedelta(days=5), estado=TaskStatus.COMPLETADA, prioridad=2)
        ]

        db.add_all(tareas_prueba)
        db.commit()
        print("✅ Archivo 'taskflow.db' creado y poblado con un usuario ('test@example.com', 'password123') y 4 tareas.")
    finally:
        db.close()

if __name__ == "__main__":
    init_and_seed_db()
