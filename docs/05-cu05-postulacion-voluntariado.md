# Documento 05: CU05 - Postulación a Voluntariado y Asignación de Actividades

**Caso de Uso:** CU05 - Postulación Voluntariado  
**Módulo de Base de Datos Principal:** Asignaciones (`postulaciones_voluntariado`, `asignaciones_actividades`) + Catálogo de Causas (`necesidades_campana`)

---

## 1. Descripción Funcional

El módulo **CU05** conecta a los voluntarios rurales con las labores específicas requeridas por las fundaciones OSAL de la Sabana Norte. Cuando el voluntario se postula:
1. Se valida la restricción de unicidad compuesta (`uq_voluntario_necesidad`) en `postulaciones_voluntariado`.
2. Se registra su motivación y disponibilidad horaria.
3. Se genera la orden operativa en `asignaciones_actividades` con las horas comprometidas y se actualiza el indicador de cobertura en `necesidades_campana.cantidad_cubierta`.

---

## 2. Rutas de la API (Backend Flask)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/voluntariado/labores` | Lista las necesidades comunitarias disponibles y las postulaciones/asignaciones activas. |
| `POST` | `/api/voluntariado/postular` | Registra la postulación en `postulaciones_voluntariado` y crea su actividad en `asignaciones_actividades`. |

---

## 3. Componente UI (Frontend Angular)

- **`PostulacionVoluntariadoComponent` (`src/app/features/voluntariado/postulacion-voluntariado.component.ts`)**:
  - Permite seleccionar la labor, indicar horario y horas de compromiso con respaldo **Offline-First** y visualizar las asignaciones confirmadas.

