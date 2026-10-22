from app import create_app
from app.extensions import db
from app.seed import seed_initial_data

app = create_app()


@app.cli.command("init-db")
def init_db_command():
    """Crea las 32 tablas 5FN en MySQL y carga el catálogo inicial de Sabana Norte."""
    db.create_all()
    seed_initial_data()
    print("Base de datos 5FN (32 tablas) inicializada y poblada con éxito.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
