# Documento 08: CU08 - Dashboard OSAL y Métricas de Impacto (5FN)

**Caso de Uso:** CU08 - Dashboard OSAL  
**Módulos de Base de Datos Involucrados:** Transacciones (`donaciones_economicas`, `donaciones_especie`), Voluntariado y Asignaciones (`voluntarios`, `postulaciones_voluntariado`, `asignaciones_actividades`) y Catálogo de Causas (`campanas`, `necesidades_campana`).

---

## 1. Descripción Funcional

El módulo **CU08** consolida las métricas operativas de las fundaciones de la Sabana Norte mediante agregaciones SQL (`SUM`, `COUNT`) sobre las tablas normalizadas en 5FN:
- **Recaudo Económico Total vs. Meta Global** (`donaciones_economicas.monto` y `campanas.meta_economica`).
- **Voluntarios Activos y Horas Comprometidas** (`voluntarios` y `asignaciones_actividades.horas_comprometidas`).
- **Estado de Entregas en Especie** (`RECIBIDO`, `EN_BODEGA`, `ENTREGADO`).
- **Avance porcentual por cada campaña rural**.

---

## 2. Ruta de la API (Backend Flask)

Blueprint registrado en `backend/app/blueprints/dashboard.py`:

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/dashboard/osal` | Retorna el objeto `kpis`, el desglose `logistica_especie` y la lista `campanas_desempeno`. |

---

## 3. Componente UI (Frontend Angular)

- **`DashboardOsalComponent` (`src/app/features/dashboard/dashboard-osal.component.ts`)**:
  - Presenta tarjetas KPI de alto contraste y barras de progreso detalladas por campaña.

