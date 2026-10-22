# Documento 07: CU07 - Certificados Tributarios Descargables en PDF

**Caso de Uso:** CU07 - Certificados Tributarios  
**Módulo de Base de Datos Principal:** Transacciones (`donaciones_economicas`, `recibos_tributarios`, `aportes_transaccionales`, `donantes`, `metodos_pago`) + Perfiles (`fundaciones_osal`, `personas`, `documentos_identidad`)

---

## 1. Descripción Funcional

El módulo **CU07** expone la generación dinámica de un **Certificado de Donación Tributaria en formato PDF** utilizando el motor gráfico **ReportLab** en Flask. Cruza de manera estrictamente relacional:
- La entidad receptora (`fundaciones_osal`: NIT, razón social y estado de validación).
- El donante (`donantes` -> `personas` -> `documentos_identidad`).
- El detalle financiero (`donaciones_economicas` -> `metodos_pago` y `aportes_transaccionales`).
- El consecutivo fiscal y hash criptográfico SHA-256 (`recibos_tributarios`).

---

## 2. Ruta de la API (Backend Flask)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/donaciones/economicas/<id>/certificado-pdf` | Genera un flujo binario `application/pdf` con descarga directa (`Certificado_Tributario_CERT-YYYY-XXXXX.pdf`). |

---

## 3. Integración UI (Frontend Angular)

En `RegistrarDonacionComponent` (`src/app/features/donaciones/registrar-donacion.component.ts`), cada aporte económico muestra el botón de alto contraste **"📄 Descargar Certificado Tributario PDF"**, permitiendo obtener el soporte contable con un solo toque.
