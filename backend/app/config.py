import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración base del Monolito Modular Flask para Conexión Solidaria."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-conexion-solidaria")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-conexion-solidaria")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    # Conexión estrictamente relacional a MySQL mediante PyMySQL y SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost:3306/conexion_solidaria_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # Límite de 10 MB para soportes/documentos rurales
