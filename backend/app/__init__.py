import os
import click
from flask import Flask, jsonify, send_from_directory
from app.config import Config
from app.extensions import db, migrate, jwt, cors
import app.models  # noqa: F401
from app.blueprints.auth import auth_bp
from app.blueprints.catalogos import catalogos_bp
from app.blueprints.osal import osal_bp
from app.blueprints.campanas import campanas_bp
from app.blueprints.donaciones import donaciones_bp
from app.blueprints.voluntariado import voluntariado_bp
from app.blueprints.mapa import mapa_bp
from app.blueprints.dashboard import dashboard_bp


def inicializar_esquema_con_respaldo(app: Flask) -> None:
    """Crea las 32 tablas 5FN y pobla los catálogos iniciales de la Sabana Norte."""
    from app.seed import seed_initial_data

    with app.app_context():
        db.create_all()
        seed_initial_data()


def create_app(config_class=Config):
    """Application Factory del Monolito Modular Flask."""
    static_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist", "frontend", "browser")
    )

    app = Flask(__name__, static_folder=static_dir, static_url_path="")
    app.config.from_object(config_class)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(auth_bp)
    app.register_blueprint(catalogos_bp)
    app.register_blueprint(osal_bp)
    app.register_blueprint(campanas_bp)
    app.register_blueprint(donaciones_bp)
    app.register_blueprint(voluntariado_bp)
    app.register_blueprint(mapa_bp)
    app.register_blueprint(dashboard_bp)

    inicializar_esquema_con_respaldo(app)

    @app.cli.command("init-db")
    def init_db_command():
        """Crea las 32 tablas 5FN y carga el catálogo inicial de Sabana Norte."""
        inicializar_esquema_con_respaldo(app)
        click.echo(f"Base de datos 5FN (32 tablas) inicializada y poblada con éxito en: {app.config['SQLALCHEMY_DATABASE_URI']}")

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "ok",
            "proyecto": "Conexión Solidaria - Sabana Norte de Cundinamarca",
            "arquitectura": "Monolito Modular (Flask + SQLAlchemy MySQL 5FN)",
            "tablas_registradas": len(db.metadata.tables)
        }), 200

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_angular_pwa(path: str):
        """Sirve los archivos compilados de Angular PWA en despliegues unificados como Render."""
        if path.startswith("api/"):
            return jsonify({"error": "Endpoint no encontrado"}), 404
        if os.path.exists(static_dir):
            target_file = os.path.join(static_dir, path)
            if path and os.path.isfile(target_file):
                return send_from_directory(static_dir, path)
            for index_name in ("index.csr.html", "index.html"):
                if os.path.isfile(os.path.join(static_dir, index_name)):
                    return send_from_directory(static_dir, index_name)
        return jsonify({
            "status": "API Conexión Solidaria Activa",
            "endpoints": "/api/health"
        }), 200

    return app
