# Documento 03: CU03 - Publicar Necesidad y Catálogo de Causas (5FN)

**Caso de Uso:** CU03 - Publicar Necesidad  
**Módulo de Base de Datos Principal:** Catálogo de Causas (`ods_objetivos`, `categorias_causas`, `campanas`, `tipos_necesidad`, `necesidades_campana`)

---

## 1. Descripción Funcional

El módulo **CU03** permite a las Organizaciones Sin Ánimo de Lucro (OSAL) publicar campañas solidarias alineadas con los **Objetivos de Desarrollo Sostenible (ODS)** y desglosar cada requerimiento según las tres modalidades normalizadas en `tipos_necesidad`:
- **`ECONOMICA`**: Recursos monetarios para financiar infraestructura o compras veredales.
- **`ESPECIE`**: Insumos agrícolas, alimentos no perecederos, semillas nativas o herramientas.
- **`TIEMPO_VOLUNTARIADO`**: Horas de trabajo comunitario o capacitación técnica.

---

## 2. Rutas de la API (Backend Flask)

Blueprint registrado en `backend/app/blueprints/campanas.py` bajo `/api/campanas`:

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/campanas` | Retorna las campañas activas cruzando en 5FN `campanas`, `fundaciones_osal`, `direcciones`, `municipios`, `categorias_causas`, `ods_objetivos`, `necesidades_campana` y `tipos_necesidad`. |
| `POST` | `/api/campanas` | Crea un registro en `campanas`, inserta múltiples ítems hijos en `necesidades_campana` y deja registro en `logs_auditoria`. |

---

## 3. Componentes UI (Frontend Angular)

- **`PublicarNecesidadComponent` (`src/app/features/campanas/publicar-necesidad.component.ts`)**:
  - Presenta las campañas en **Tarjetas (Cards)** limpias con barras de progreso de alto contraste, etiquetas de municipio/vereda y enlaces directos para donar o postularse como voluntario.
  - Incluye el formulario dinámico para que la OSAL agregue múltiples necesidades con respaldo **Offline-First** automático.

