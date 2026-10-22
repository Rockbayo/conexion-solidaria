import os
import socket
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def obtener_database_uri() -> str:
    """
    Retorna la URI de conexión MySQL 5FN configurada en DATABASE_URL.
    Si el puerto 3306 de MySQL no está recibiendo conexiones en localhost,
    habilita el motor relacional local SQLAlchemy (SQLite 5FN) para que `flask init-db`
    y `python run.py` funcionen de inmediato sin errores de socket.
    """
    uri_env = os.getenv("DATABASE_URL")
    if uri_env:
        return uri_env

    # Verificar si hay un servidor MySQL escuchando en localhost:3306
    try:
        with socket.create_connection(("127.0.0.1", 3306), timeout=0.6):
            return "mysql+pymysql://root:password@localhost:3306/conexion_solidaria_db"
    except OSError:
        fallback_db = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "conexion_solidaria_5fn.db")
        )
        return f"sqlite:///{fallback_db}"


class Config:
    """Configuración base del Monolito Modular Flask para Conexión Solidaria."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-conexion-solidaria-2026-sabana-norte")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-conexion-solidaria-2026-sabana-norte")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    SQLALCHEMY_DATABASE_URI = obtener_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }

    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
