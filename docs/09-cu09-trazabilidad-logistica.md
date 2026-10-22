# Documento 09: CU09 - Trazabilidad Logística de Donaciones en Especie (5FN)

**Caso de Uso:** CU09 - Trazabilidad Logística  
**Módulo de Base de Datos Principal:** Transacciones (`donaciones_especie`, `trazabilidad_entregas`, `unidades_medida`, `aportes_transaccionales`)

---

## 1. Descripción Funcional

El flujo **CU09** garantiza la transparencia en el manejo de insumos físicos donados para las zonas rurales de la Sabana Norte. Permite actualizar y auditar el ciclo de vida logístico en tres estados secuenciales:
1. **`RECIBIDO`**: Insumo reportado por el donante y recibido en el punto inicial.
2. **`EN_BODEGA`**: Acopio clasificado y almacenado en centro comunitario municipal.
3. **`ENTREGADO`**: Entrega final verificada en la vereda o sede rural de la OSAL.

Cada transición actualiza `donaciones_especie.estado_logistico_actual` e inserta una fila inmutable en `trazabilidad_entregas` con fecha UTC, ubicación y observación.

---

## 2. Ruta de la API (Backend Flask)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `PUT / POST` | `/api/donaciones/especie/<id>/trazabilidad` | Actualiza el estado (`RECIBIDO`, `EN_BODEGA`, `ENTREGADO`), registra el hito en `trazabilidad_entregas` y audita la operación en `logs_auditoria`. |

---

## 3. Componente UI (Frontend Angular)

- **`TrazabilidadLogisticaComponent` (`src/app/features/donaciones/trazabilidad-logistica.component.ts`)**:
  - Muestra cada donación en especie en una tarjeta de alto contraste con barra visual de 3 etapas (`1. RECIBIDO -> 2. EN BODEGA -> 3. ENTREGADO EN VEREDA`) y su bitácora completa de movimientos.
