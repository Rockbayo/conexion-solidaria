# Documento 06: CU06 - Mapa Georreferenciado de la Sabana Norte (Leaflet.js + 5FN)

**Caso de Uso:** CU06 - Mapa Georreferenciado  
**Módulo de Base de Datos Principal:** Geolocalización (`paises`, `departamentos`, `municipios`, `direcciones`) + Perfiles (`fundaciones_osal`) + Catálogo de Causas (`campanas`)

---

## 1. Descripción Funcional

El módulo **CU06** integra **Leaflet.js** dentro de Angular (con carga segura en cliente mediante `isPlatformBrowser` para compatibilidad con Server-Side Rendering) y realiza el cruce relacional en Quinta Forma Normal entre:
- `fundaciones_osal` (Razón social, NIT, misión, estado de validación)
- `direcciones` (Vereda o sector rural, dirección física, indicaciones rurales, `latitud` y `longitud`)
- `municipios` (Chía, Cajicá, Zipaquirá, Tabio, Tenjo, Cogua, Sopó, Tocancipá, Gachancipá, Nemocón)

---

## 2. Ruta de la API (Backend Flask)

Blueprint registrado en `backend/app/blueprints/mapa.py`:

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/mapa/pines` | Ejecuta un `JOIN` relacional entre `fundaciones_osal`, `direcciones` y `municipios` (filtrable por `municipio_id`) y retorna las coordenadas y campañas activas. |

---

## 3. Componente UI (Frontend Angular)

- **`MapaSabanaComponent` (`src/app/features/mapa/mapa-sabana.component.ts`)**:
  - Renderiza el mapa interactivo centrado en la Sabana Norte de Cundinamarca (`lat: 4.965, lng: -74.01`) con marcadores circulares de alto contraste y *popups* informativos.
  - Incluye tarjetas laterales accesibles (alternativa textual conforme a WCAG 2.2) que al seleccionarse centran el mapa en la vereda correspondiente.

