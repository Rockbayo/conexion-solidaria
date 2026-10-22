# Documento 12: Despliegue en la Nube con Render (Blueprint Unificado)

**Objetivo:** Desplegar el Monorepo de **Conexión Solidaria** (Backend Flask + Base de Datos Relacional 5FN + Frontend Angular PWA/SSR con diseño SAP Fiori Horizon) en **Render** para verificación en línea.

---

## 1. Arquitectura de Despliegue en Render

Para evitar problemas de CORS, certificados cruzados o costos de múltiples instancias, el proyecto incluye un **Render Blueprint (`render.yaml`)** y el script automatizado **`build.sh`**:

1. **Compilación de Angular PWA (`frontend/dist/frontend/browser`):** Durante el despliegue, Render instala paquetes Node, compila los componentes Standalone, genera el manifiesto del Service Worker (`ngsw.json`) y prerenderiza las rutas.
2. **Servidor WSGI de Producción (`gunicorn`):** Flask sirve bajo el mismo dominio tanto los endpoints RESTful (`/api/*`) como la aplicación progresiva compilada de Angular (`/`), mientras que `getApiBaseUrl()` en Angular detecta automáticamente si está corriendo en `localhost` o en el dominio `*.onrender.com`.
3. **Inicialización Automática de las 32 Tablas (5FN):** Al iniciar, si se configura la variable de entorno `DATABASE_URL` apuntando a un servidor MySQL externo, se conecta a él; de lo contrario, inicializa y pobla automáticamente las 32 tablas relacionales en el motor local con los municipios y cuentas de la Sabana Norte.

---

## 2. Pasos para Desplegar en Render

1. **Subir el Monorepo a GitHub / GitLab:**
   ```powershell
   cd C:\Users\ingor\conexion-solidaria
   git remote add origin https://github.com/<tu-usuario>/<tu-repositorio>.git
   git branch -M main
   git push -u origin main
   ```
2. **Crear el Servicio en Render:**
   - Ingresa a https://dashboard.render.com
   - Haz clic en **New +** -> **Blueprint** (o **Web Service**).
   - Conecta tu repositorio de GitHub: Render detectará automáticamente el archivo `render.yaml` en la raíz.
   - Si eliges **Web Service** manual, usa estos valores:
     - **Build Command:** `./build.sh`
     - **Start Command:** `cd backend && gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
3. **Verificación en vivo:**
   - Una vez finalizado el despliegue, abre la URL `https://conexion-solidaria.onrender.com` para navegar por la interfaz SAP Fiori y consulta `https://conexion-solidaria.onrender.com/api/health` para confirmar las 32 tablas activas.

