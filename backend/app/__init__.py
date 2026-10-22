import os
from flask import Flask, jsonify
from app.config import Config
from app.extensions import db, migrate, jwt, cors
import app.models  # noqa: F401 - Registra las 32 tablas relacionales en SQLAlchemy
from app.blueprints.auth import auth_bp
from app.blueprints.catalogos import catalogos_bp
from app.blueprints.osal import osal_bp
from app.blueprints.campanas import campanas_bp
from app.blueprints.donaciones import donaciones_bp
from app.blueprints.voluntariado import voluntariado_bp


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

    # Registrar Blueprints modulares
    app.register_blueprint(auth_bp)
    app.register_blueprint(catalogos_bp)
    app.register_blueprint(osal_bp)
    app.register_blueprint(campanas_bp)
    app.register_blueprint(donaciones_bp)
    app.register_blueprint(voluntariado_bp)

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "ok",
            "proyecto": "Conexión Solidaria - Sabana Norte de Cundinamarca",
            "arquitectura": "Monolito Modular (Flask + SQLAlchemy MySQL 5FN)",
            "tablas_registradas": len(db.metadata.tables)
        }), 200

    return app
