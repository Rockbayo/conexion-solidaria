#!/usr/bin/env bash
set -o errexit

echo "=== [1/3] Instalando dependencias de Python (Flask + SQLAlchemy 5FN + ReportLab + Gunicorn) ==="
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "=== [2/3] Compilando Frontend Angular (Standalone + SSR + PWA Service Worker) ==="
cd frontend
npm install
npm run build
cd ..

echo "=== [3/3] Inicializando Esquema Relacional 5FN (32 Tablas) y Semillas de Sabana Norte ==="
cd backend
python -c "from app import create_app, inicializar_esquema_con_respaldo; app = create_app(); inicializar_esquema_con_respaldo(app)"
cd ..
echo "=== Build de Conexión Solidaria completado con éxito ==="

