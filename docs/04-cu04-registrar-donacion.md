# Documento 04: CU04 - Registrar Donación y Subida de Comprobante (5FN)

**Caso de Uso:** CU04 - Registrar Donación  
**Módulo de Base de Datos Principal:** Transacciones (`donantes`, `aportes_transaccionales`, `donaciones_economicas`, `donaciones_especie`, `unidades_medida`, `metodos_pago`, `recibos_tributarios`, `trazabilidad_entregas`)

---

## 1. Descripción Funcional

El flujo **CU04** permite a cualquier Donante Solidario (Persona Natural o Empresa) reportar un aporte a una campaña rural de la Sabana Norte y adjuntar su comprobante. El sistema soporta dos especializaciones disjuntas normalizadas en Quinta Forma Normal (5FN):
1. **Modalidad Económica (`donaciones_economicas`):** Registra monto en COP, método de pago (`metodos_pago`), referencia bancaria, incrementa automáticamente `campanas.monto_recaudado` y emite su consecutivo en `recibos_tributarios`.
2. **Modalidad en Especie (`donaciones_especie`):** Registra artículos donados, cantidad, unidad de medida (`unidades_medida`) e inicializa su historial logístico en `trazabilidad_entregas` con estado `RECIBIDO`.

---

## 2. Rutas de la API (Backend Flask)

Blueprint registrado en `backend/app/blueprints/donaciones.py`:

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/donaciones` | Lista los aportes transaccionales con su detalle económico o en especie, recibo tributario y trazabilidad. |
| `POST` | `/api/donaciones` | Registra el aporte en `aportes_transaccionales`, persiste el registro especializado (`donaciones_economicas` o `donaciones_especie`) y audita la transacción. |

---

## 3. Componentes UI y Manejo de Errores Humano (Frontend Angular)

- **`RegistrarDonacionComponent` (`src/app/features/donaciones/registrar-donacion.component.ts`)**:
  - Incluye conmutador accesible entre Donación Económica y Donación en Especie, carga de comprobante y persistencia continua en caché local.
  - Ante pérdida de conectividad rural (`err.status === 0`), muestra literalmente el mensaje humano: *"Tu conexión parece inestable. Hemos guardado tu donación para enviarla en cuanto recuperes la señal"*.
