from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Puedes cambiar esta URL por PostgreSQL o MySQL fácilmente:
# Ejemplo Postgres: "postgresql://usuario:password@localhost:5432/taskflow"
SQLALCHEMY_DATABASE_URL = "sqlite:///./taskflow.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Necesario solo para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()