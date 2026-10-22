import os
import click
from flask import Flask, jsonify
from sqlalchemy.exc import OperationalError
from app.config import Config
from app.extensions import db, migrate, jwt, cors
import app.models  # noqa: F401 - Registra las 32 tablas relacionales en SQLAlchemy
from app.blueprints.auth import auth_bp
from app.blueprints.catalogos import catalogos_bp
from app.blueprints.osal import osal_bp
from app.blueprints.campanas import campanas_bp
from app.blueprints.donaciones import donaciones_bp
from app.blueprints.voluntariado import voluntariado_bp
from app.blueprints.mapa import mapa_bp
from app.blueprints.dashboard import dashboard_bp


def inicializar_esquema_con_respaldo(app: Flask) -> None:
    """
    Inicializa y pobla las 32 tablas 5FN en MySQL.
    Si el servidor MySQL local no está levantado aún, realiza un fallback relacional
    automático para que el entorno no falle al arrancar.
    """
    from app.seed import seed_initial_data

    with app.app_context():
        try:
            db.create_all()
            seed_initial_data()
        except OperationalError:
            fallback_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "conexion_solidaria_5fn.db")
            app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.abspath(fallback_path)}"
            db.engine.dispose()
            db.create_all()
            seed_initial_data()
            print(
                "[AVISO] No se detectó servidor MySQL activo en localhost:3306. "
                "Operando sobre motor relacional local de respaldo con las 32 tablas 5FN inicializadas."
            )


def create_app(config_class=Config):
    """Application Factory del Monolito Modular Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Registrar Blueprints modulares (10 Casos de Uso)
    app.register_blueprint(auth_bp)
    app.register_blueprint(catalogos_bp)
    app.register_blueprint(osal_bp)
    app.register_blueprint(campanas_bp)
    app.register_blueprint(donaciones_bp)
    app.register_blueprint(voluntariado_bp)
    app.register_blueprint(mapa_bp)
    app.register_blueprint(dashboard_bp)

    @app.cli.command("init-db")
    def init_db_command():
        """Crea las 32 tablas 5FN y carga el catálogo inicial de Sabana Norte."""
        inicializar_esquema_con_respaldo(app)
        click.echo("Base de datos 5FN (32 tablas) inicializada y poblada con éxito.")

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "ok",
            "proyecto": "Conexión Solidaria - Sabana Norte de Cundinamarca",
            "arquitectura": "Monolito Modular (Flask + SQLAlchemy MySQL 5FN)",
            "tablas_registradas": len(db.metadata.tables)
        }), 200

    return app
