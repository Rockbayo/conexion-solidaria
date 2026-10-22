from app import create_app, inicializar_esquema_con_respaldo

app = create_app()

if __name__ == "__main__":
    inicializar_esquema_con_respaldo(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
