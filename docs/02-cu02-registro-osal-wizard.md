# Documento 02: CU02 - Registro de OSAL (Formulario Wizard y Documentos Legales)

**Caso de Uso:** CU02 - Registro de OSAL  
**Módulos de Base de Datos Involucrados:** Perfiles (`fundaciones_osal`, `documentos_legales_osal`, `personas`, `documentos_identidad`, `tipos_documento`), Geolocalización (`municipios`, `direcciones`) y Seguridad (`usuarios`, `roles`, `usuarios_roles`, `logs_auditoria`).

---

## 1. Descripción Funcional

Permite a una Organización Sin Ánimo de Lucro (OSAL) de las zonas rurales de la Sabana Norte de Cundinamarca inscribirse en la plataforma mediante un **Formulario Paso a Paso (Wizard de 3 etapas)** que evita la saturación cognitiva y protege la información frente a caídas de señal rural:
1. **Paso 1 (Datos Institucionales):** NIT, Razón Social, Sigla, Misión comunitaria, Teléfono y Fecha de constitución.
2. **Paso 2 (Georreferenciación Rural y Representante):** Selección de municipio de la Sabana Norte, vereda, dirección física, coordenadas (`latitud`, `longitud`) y datos del representante legal.
3. **Paso 3 (Soportes Legales):** Registro del RUT y Certificado de Existencia y Representación Legal, dejando la fundación en estado **`PENDIENTE`** de validación.

---

## 2. Rutas de la API (Backend Flask)

Blueprints registrados en `backend/app/blueprints/osal.py` y `backend/app/blueprints/catalogos.py`:

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/catalogos/general` | Retorna catálogos 5FN (municipios de Sabana Norte con coordenadas centrales, tipos de documento, ODS, categorías de causas, habilidades, etc.) cacheables por el Service Worker. |
| `POST` | `/api/osal/registro` | Ejecuta una transacción atómica sobre 7 tablas normalizadas en 5FN, dejando `fundaciones_osal.estado_validacion = 'PENDIENTE'` y los archivos en `documentos_legales_osal` con `estado_revision = 'EN_REVISION'`. |
| `GET` | `/api/osal` | Lista todas las fundaciones OSAL registradas junto con su municipio, vereda y conteo de soportes legales. |

---

## 3. Componentes UI y Resiliencia Offline-First (Angular)

- **`OfflineSyncService` (`src/app/core/services/offline-sync.service.ts`)**:
  - Almacena en caché local los catálogos maestros de la Sabana Norte y ofrece persistencia automática de borradores (`guardarBorradorFormulario` / `cargarBorradorFormulario`).
- **`RegistroOsalWizardComponent` (`src/app/features/osal/registro-osal-wizard.component.ts`)**:
  - Implementa el Wizard accesible de 3 pasos con indicadores claros de progreso (`Paso 1 de 3`) y guardado automático tras cada cambio. Si el envío falla por corte de señal (`err.status === 0`), despliega un mensaje humano informando que los datos quedaron resguardados localmente.
