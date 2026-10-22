# Documento 00: Arquitectura Base del Monorepo y Modelo Relacional 5FN

**Proyecto de Grado:** Conexión Solidaria  
**Alcance Territorial:** Zonas Rurales de la Sabana Norte de Cundinamarca (Chía, Cajicá, Zipaquirá, Tabio, Tenjo, Cogua, Gachancipá, Sopó, Tocancipá, Nemocón, Subachoque)  
**Patrón Arquitectónico:** Monolito Modular (Sin microservicios puros, sin Kubernetes, sin bases de datos NoSQL)

---

## 1. Estructura del Monorepo

El repositorio Git está estructurado en tres directorios raíz que separan claramente las responsabilidades técnicas y documentales:

```text
conexion-solidaria/
├── backend/                  # API RESTful Modular en Python (Flask + SQLAlchemy)
│   ├── app/
│   │   ├── models/           # 32 Modelos ORM normalizados en 5FN (snake_case)
│   │   ├── blueprints/       # Módulos de negocio desacoplados por Caso de Uso
│   │   ├── config.py         # Configuración de conexión MySQL y JWT
│   │   ├── extensions.py     # Instancias de SQLAlchemy, Migrate, JWT y CORS
│   │   └── __init__.py       # Application Factory (create_app)
│   ├── requirements.txt      # Dependencias estables del servidor
│   ├── .env.example          # Plantilla de variables de entorno MySQL
│   └── run.py                # Punto de entrada WSGI/Desarrollo
├── frontend/                 # Aplicación Angular (Standalone, SSR, Fetch API, PWA)
│   ├── src/
│   │   ├── app/              # Componentes Standalone, Servicios Offline-First y Rutas
│   │   └── styles.css        # Sistema de diseño accesible WCAG 2.2 (Alto Contraste Rural)
│   ├── ngsw-config.json      # Configuración del Service Worker (Caché Offline-First)
│   └── package.json          # Dependencias de Angular, PWA y Leaflet.js
└── docs/                     # Documentación Continua (Base de Manual Técnico y de Usuario)
    └── 00-arquitectura-y-estructura-base.md
```

---

## 2. Configuración del Backend (Flask + MySQL 5FN)

### 2.1 Conexión Relacional a MySQL
La capa de persistencia se gestiona en `backend/app/config.py` utilizando **SQLAlchemy** sobre el conector puro **PyMySQL**:
- **URI de Conexión:** `mysql+pymysql://<usuario>:<password>@<host>:3306/conexion_solidaria_db`
- **Resiliencia de Pool:** Se habilita `pool_pre_ping=True` y `pool_recycle=280` para evitar desconexiones o cierres prematuros de sockets TCP con el servidor MySQL.

### 2.2 Modelo de Datos en Quinta Forma Normal (5FN - 32 Tablas)
En `backend/app/models/__init__.py` se implementan las **32 tablas relacionales** distribuidas en **7 módulos**, eliminando redundancias de proyección-unión y garantizando integridad referencial estricta mediante llaves foráneas (`ForeignKey`):

1. **Módulo de Seguridad (4 tablas):**
   - `usuarios`, `roles`, `usuarios_roles`, `logs_auditoria`.
2. **Módulo de Geolocalización (4 tablas):**
   - `paises`, `departamentos`, `municipios`, `direcciones`.
3. **Módulo de Perfiles (5 tablas):**
   - `tipos_documento`, `personas`, `documentos_identidad`, `fundaciones_osal`, `documentos_legales_osal`.
4. **Módulo de Voluntariado (4 tablas):**
   - `voluntarios`, `categorias_habilidades`, `habilidades`, `perfil_habilidades_voluntario`.
5. **Módulo de Catálogo de Causas (5 tablas):**
   - `ods_objetivos`, `categorias_causas`, `campanas`, `tipos_necesidad`, `necesidades_campana`.
6. **Módulo de Transacciones (8 tablas):**
   - `donantes`, `unidades_medida`, `metodos_pago`, `aportes_transaccionales`, `donaciones_economicas`, `donaciones_especie`, `trazabilidad_entregas`, `recibos_tributarios`.
7. **Módulo de Asignaciones (2 tablas):**
   - `postulaciones_voluntariado`, `asignaciones_actividades`.

### 2.3 Endpoint Base de Verificación
- **Ruta:** `GET /api/health`
- **Propósito:** Verificar el estado operativo del monolito y confirmar el registro en memoria de las 32 tablas del metadato de SQLAlchemy.

---

## 3. Configuración del Frontend (Angular + SSR + Fetch API + PWA)

### 3.1 Arquitectura Angular Moderna
- **Standalone Components:** Todos los componentes prescinden de `NgModule`, reduciendo la sobrecarga de paquetes en conexiones móviles rurales (3G/2G).
- **Server-Side Rendering (SSR):** Habilitado mediante `@angular/ssr` para acelerar el *First Contentful Paint (FCP)* en dispositivos de gama media/baja.
- **Fetch API:** Configurado en `app.config.ts` mediante `provideHttpClient(withFetch())`.

### 3.2 Estrategia Resiliente Offline-First (PWA)
- **Service Worker (`@angular/pwa`):** Configurado con grupos de activos (`assetGroups`) en modo `prefetch` y grupos de datos (`dataGroups`) para cachear catálogos y mapas de la Sabana Norte.
- **Persistencia Local de Formularios:** Ante intermitencia de red, los formularios almacenan el borrador o la transacción en cola local (`localStorage` / cola de sincronización) y presentan mensajes humanos contextualizados bajo lineamientos **WCAG 2.2 (Alto Contraste)**.

