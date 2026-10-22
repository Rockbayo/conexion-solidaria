# Manual Técnico y de Usuario Consolidado — Conexión Solidaria (MVP)

**Proyecto de Grado de Ingeniería:** Conexión Solidaria  
**Cobertura Geográfica:** Zonas Rurales de la Sabana Norte de Cundinamarca  
**Arquitectura:** Monolito Modular (Flask + SQLAlchemy MySQL 5FN + Angular Standalone SSR/PWA + Leaflet.js)

---

## 1. Índice de Documentación por Módulo y Caso de Uso (`/docs`)

1. [00 - Arquitectura Base del Monorepo y Modelo 5FN](./00-arquitectura-y-estructura-base.md)
2. [01 - CU01: Autenticación con JWT y Enrutamiento Protegido](./01-cu01-autenticacion-jwt.md)
3. [02 - CU02: Registro de OSAL con Formulario Wizard y Documentos Legales](./02-cu02-registro-osal-wizard.md)
4. [03 - CU03: Publicar Necesidad y Catálogo de Causas](./03-cu03-publicar-necesidad.md)
5. [04 - CU04: Registrar Donación (Económica y Especie) con Comprobante](./04-cu04-registrar-donacion.md)
6. [05 - CU05: Postulación a Voluntariado y Asignaciones](./05-cu05-postulacion-voluntariado.md)
7. [06 - CU06: Mapa Georreferenciado con Leaflet.js en Sabana Norte](./06-cu06-mapa-georreferenciado-leaflet.md)
8. [07 - CU07: Certificados Tributarios Descargables en PDF](./07-cu07-certificados-tributarios-pdf.md)
9. [08 - CU08: Dashboard OSAL (Métricas Operativas)](./08-cu08-dashboard-osal.md)
10. [09 - CU09: Trazabilidad Logística de Donaciones en Especie](./09-cu09-trazabilidad-logistica.md)
11. [10 - CU10: Perfil de Habilidades del Voluntario](./10-cu10-perfil-habilidades.md)

---

## 2. Guía de Despliegue y Ejecución Local (Manual Técnico)

### 2.1 Requisitos Previos
- **Python:** 3.12+
- **Base de Datos:** MySQL 8.0+ (Base de datos creada como `conexion_solidaria_db`)
- **Node.js / Angular CLI:** Node 22+ y Angular CLI 21+

### 2.2 Levantar el Backend (Flask + SQLAlchemy MySQL 5FN)
```powershell
cd backend
.\.venv\Scripts\activate
# Configurar DATABASE_URL en archivo .env basándose en .env.example
flask init-db      # Crea las 32 tablas 5FN y pobla los catálogos de la Sabana Norte
python run.py      # Inicia el servidor RESTful en http://localhost:5000
```

### 2.3 Levantar el Frontend (Angular Standalone + SSR + PWA)
```powershell
cd frontend
npm start          # Inicia el servidor de desarrollo en http://localhost:4200
# Para compilar en modo producción con Service Worker Offline-First y SSR:
npm run build
```

---

## 3. Guía Rápida de Operación (Manual de Usuario Rural)

- **Cuentas Demostrativas Preconfiguradas (Contraseña: `Solidaria2026*`):**
  - **Representante OSAL (Cogua):** `osal@sabananorte.org`
  - **Donante Solidario (Tabio):** `donante@conexion.org`
  - **Voluntaria Rural:** `voluntario@conexion.org`
- **Resiliencia en Zonas sin Señal:** Todos los formularios (Wizard de OSAL, Campañas, Donaciones y Voluntariado) guardan automáticamente un borrador local en el dispositivo y muestran alertas humanas de alto contraste (WCAG 2.2) cuando la conexión rural es inestable.
