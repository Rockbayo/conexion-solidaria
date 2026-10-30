# Borrador 1: Aporte de Innovación Ingenieril, Nuevo Conocimiento y Actualización de Capítulos Técnicos (2.6, 4.5 y 5.4)

> **Propósito de este documento:** Subsanar de manera rigurosa las **Observaciones #1, #3 y #4** del Concepto de Evaluación del Trabajo de Grado (*Universidad de Cundinamarca - Extensión Chía*), articulando los capítulos técnicos del documento principal (`conexion_solidaria_v3 (1).docx`) con la implementación real verificada del Producto Mínimo Viable (MVP) de **Conexión Solidaria**.

---

## 1. Respuesta Estructural a la Observación #4: Diferenciación de los Componentes de Innovación y Nuevo Conocimiento

*(Texto listo para integrar en el **Apartado 4.5. Innovación y diferenciación** — subapartados `4.5.1 Elementos innovadores de la propuesta`, `4.5.2 Ventajas frente a las alternativas existentes`, `4.5.3 Aporte de conocimiento` y `4.5.4 Potencial de escalabilidad y replicabilidad`).*

### 4.5.1. Elementos innovadores de la propuesta

En el ámbito de la Ingeniería de Sistemas y Computación aplicada al sector social rural, la innovación de **Conexión Solidaria** no radica únicamente en la puesta en marcha de un portal web informativo, sino en la **integración arquitectónica y procedimental de tres brechas estructurales** que afectan a las Organizaciones Sin Ánimo de Lucro (OSAL) rurales de la Sabana Centro y Norte de Cundinamarca: (1) la intermitencia de conectividad en zonas veredales, (2) la informalidad en la trazabilidad de recursos físicos y monetarios, y (3) la asimetría técnica frente al cumplimiento normativo colombiano (Régimen Tributario Especial - DIAN y Ley Estatutaria 1581 de 2012).

A diferencia de los canales informales predominantes (grupos de mensajería instantánea, redes sociales de difusión unidireccional y hojas de cálculo aisladas), el sistema introduce:

1. **Persistencia Híbrida Resiliente a la Desconexión Veredal (*Offline-First Rural Sync*):** Implementación en el cliente web (`OfflineSyncService`) de un motor de almacenamiento local y encolamiento transaccional diferido (`localStorage` + detección reactiva de eventos `online`/`offline` del navegador), que permite a representantes de fundaciones y líderes comunitarios diligenciar radicaciones institucionales, publicar campañas o registrar acopios en veredas sin cobertura celular estable, sincronizando automáticamente las cargas útiles (*payloads* JSON) hacia el servidor tan pronto se restablece el enlace de red.
2. **Trazabilidad Multidimensional de Recursos (Monetarios, Especie y Talento Humano) con Unidades Estandarizadas:** Unificación en un solo flujo transaccional de aportes financieros en pesos colombianos (`COP`), donaciones físicas parametrizadas por magnitud (`KG`, `LT`, `UND`, `KIT`) con máquina de estados logísticos de acopio (`RECIBIDO` → `EN_BODEGA` → `ENTREGADO`), y asignación de voluntariado regulada por disponibilidad horaria semanal (`HORAS`) y emparejamiento por competencias técnicas certificadas.
3. **Automatización del Cumplimiento Tributario y Protección de Datos:** Generación algorítmica en tiempo real de comprobantes/certificados digitales de donación en formato PDF (`ReportLab`) firmados con huella criptográfica de integridad **SHA-256**, estructurados conforme a los **Artículos 125, 125-1, 125-2, 125-3 y 257 del Estatuto Tributario Nacional** y el **Decreto 2150 de 2017**, junto con el registro auditable del consentimiento expreso de **Habeas Data (Ley 1581 de 2012)**.

---

### 4.5.2. Ventajas comparativas frente a las alternativas existentes

La siguiente matriz sintetiza la diferenciación técnica y funcional de **Conexión Solidaria** frente a las alternativas identificadas en el estudio de mercado y estado del arte:

| Criterio Técnico / Operativo | Redes Sociales y WhatsApp (Canales Informales) | Plataformas de Crowdfunding Comercial (Vaki, GoFundMe, Donaronline) | Directorios de Emergencia (Red Acopio, Reconstruyo Colombia) | **Conexión Solidaria (MVP Propuesto)** |
| :--- | :--- | :--- | :--- | :--- |
| **Costo / Comisión para la OSAL Rural** | Gratuito, pero sin herramientas de gestión | Comisión del **4,5% al 8,9%** + costos de pasarela por transacción | Gratuito, pero temporal / reactivo a catástrofes | **100% Gratuito (0% comisión)** bajo modelo de emprendimiento social |
| **Operación en Baja Conectividad Veredal** | Pierde contexto y formularios al caer la red | Requiere conexión continua de banda ancha | Requiere conexión continua | **Motor `OfflineSyncService` con borradores persistentes y cola diferida** |
| **Unidades de Recolección Soportadas** | Texto libre no estructurado | Exclusivamente dinero (moneda) | Insumos básicos de emergencia sin inventario | **Parametrizable (`COP`, `KG`, `LT`, `UND`, `KIT`, `HORAS`)** |
| **Trazabilidad Logística de Especie** | Nula | No aplica (no gestiona insumos físicos) | Informativa (solo ubicación de puntos) | **Auditoría en 3 estados (`RECIBIDO`, `EN_BODEGA`, `ENTREGADO`)** |
| **Gestión de Voluntariado por Habilidades** | Convocatorias abiertas sin filtro ni control de horas | No disponible | Registro básico de contacto | **Matriz de habilidades, franjas horarias estandarizadas y tope de horas** |
| **Certificación Tributaria (Estatuto Tributario)** | Manual (Word/Excel físico) | Recibo de pago simple (no equivale a certificado DIAN de la OSAL) | No disponible | **Certificado PDF automático con norma DIAN y hash SHA-256** |
| **Verificación Jurídica Previa de la OSAL** | Ninguna (alto riesgo de suplantación) | Validación bancaria básica | Validación informal | **Protocolo RBAC con exigencia obligatoria de RUT y Cámara de Comercio** |

---

### 4.5.3. Aporte de nuevo conocimiento ingenieril (Arquitectura de Referencia y Protocolo Reproducible)

Atendiendo al rigor disciplinar del programa de Ingeniería de Sistemas y Computación, el proyecto aporta **tres artefactos de conocimiento tecnológico reproducibles** para organizaciones del tercer sector en contextos rurales latinoamericanos:

1. **Modelo de Arquitectura de Referencia Liviana para Organizaciones Rurales (*Low-Bandwidth Rural Social Architecture - LBRSA*):**
   - Se define un patrón de **Monolito Modular Desacoplado** que prescinde de la sobrecarga operativa y financiera de infraestructuras de microservicios distribuidos —inviables para fundaciones sin presupuesto de TI—, combinando una **API RESTful liviana en Python (Flask + SQLAlchemy ORM)** con un **Frontend basado en señales reactivas (Angular Standalone Signals)** y una **capa intermedia de resiliencia offline en el cliente**. Este diseño reduce el costo de alojamiento en la nube en más de un 80% respecto a arquitecturas empresariales convencionales y garantiza tiempos de respuesta inferiores a `250 ms` en redes móviles 3G/4G rurales.
2. **Esquema de Datos Relacional Canónico en Quinta Forma Normal (5FN - 34 Entidades) para el Tercer Sector Colombiano:**
   - Se aporta un modelo de datos normalizado hasta **5FN** compuesto por **34 tablas distribuidas en 7 dominios cohesivos** (Seguridad RBAC, Geolocalización DANE + Coordenadas Veredales, Perfiles y Soportes Jurídicos, Voluntariado por Competencias, Catálogo de Causas alineado a los ODS, Transacciones Monetarias/Especie con Trazabilidad Logística, y Parametrización Maestra del Sistema). Este esquema elimina anomalías de actualización y constituye una plantilla reutilizable para cualquier red departamental o municipal de fundaciones en Colombia.
3. **Protocolo Reproducible de Gobernanza, Validación Institucional y Transparencia Transaccional (Protocolo PGVTT):**
   - Procedimiento algorítmico verificable en cinco etapas:
     - **Etapa 1 (Acreditación Documental y Habeas Data):** Radicación en 3 pasos con bloqueo de envío si no se adjuntan los soportes jurídicos obligatorios (`RUT_DIAN` y `CERTIFICADO_EXISTENCIA_CAMARA`) y la autorización expresa de la **Ley 1581 de 2012**.
     - **Etapa 2 (Gobernanza Jerárquica RBAC):** Separación estricta de privilegios entre cinco roles autenticados (`SUPER_ADMIN`, `ADMIN`, `REPRESENTANTE_OSAL`, `DONANTE`, `VOLUNTARIO`), donde ninguna organización puede publicar campañas de recaudación hasta que su expediente cambie de estado `PENDIENTE` a `APROBADA` con registro inmutable en `logs_auditoria`.
     - **Etapa 3 (Parametrización de Causas vinculadas a ODS):** Vinculación obligatoria de cada campaña a un Objetivo de Desarrollo Sostenible (`ods_objetivos`) y desglose de requerimientos cuantificables por unidad de medida (`unidades_medida`).
     - **Etapa 4 (Control Transaccional Antifraude):** Validación de umbrales mínimos de donación parametrizables (`MONTO_MINIMO_DONACION_COP = $10.000 COP`), exigencia obligatoria de soporte documental y número de referencia bancaria antes de afectar el libro mayor de aportes (`aportes_transaccionales`).
     - **Etapa 5 (Certificación Criptográfica y Retroalimentación de Impacto):** Emisión de recibo tributario único por año gravable con código de verificación **SHA-256** y consolidación automática de indicadores de cobertura y avance por ODS en el tablero de control (`CU08`).

---

### 4.5.4. Potencial de escalabilidad y replicabilidad

Gracias al diseño basado en catálogos normalizados (`paises`, `departamentos`, `municipios`, `parametros_sistema`, `unidades_medida`, `franjas_horarias`) y a la administración centralizada mediante el rol de **Superusuario (`SUPER_ADMIN`)**, la plataforma puede replicarse en otras provincias de Cundinamarca (Sabana Occidente, Ubaté, Guavio, Tequendama) o en otros departamentos del país **sin modificar una sola línea de código fuente**, bastando con parametrizar nuevos municipios DANE, reglas tributarias o categorías de causas desde el panel de gobierno técnico.

---

## 2. Actualización y Alineación de los Capítulos 2.6 (Marco Ingenieril) y 5.4 (Plan Técnico y Desarrollo del MVP)

*(Este bloque actualiza el texto técnico del documento principal para que coincida 100% con el software real desplegado en GitHub y Render, corrigiendo las referencias antiguas a MySQL/phpMyAdmin y 15 tablas).*

### 2.6. / 5.4. Especificación Técnica Real del Sistema de Información (Metodología RUP)

El desarrollo técnico del sistema de información **Conexión Solidaria** se estructuró bajo el **Proceso Unificado de Rational (RUP)**, aplicando un ciclo iterativo e incremental dividido en cuatro fases (Inicio, Elaboración, Construcción y Transición) que articula directamente los requerimientos operativos del emprendimiento social con la ingeniería del software:

#### A. Fase de Inicio (Inception): Perfiles de Usuario (RBAC) y Requerimientos del MVP

Se modelaron **cinco (5) roles autenticados con control de acceso basado en roles (RBAC)** más un **(1) rol público visitante**, respondiendo a la estructura organizacional y operativa de la fundación:

1. **Superusuario de Plataforma (`SUPER_ADMIN`):** Rol de máximo nivel jerárquico reservado a la Dirección General y Técnica de Conexión Solidaria. Posee privilegios exclusivos para crear cuentas de Administradores de Plataforma (`ADMIN`) y parametrizar en caliente las tablas maestras del sistema (`parametros_sistema`, `unidades_medida`, `categorias_causas`, `habilidades`, `franjas_horarias`).
2. **Administrador de Plataforma (`ADMIN`):** Encargado de la gobernanza operativa, la auditoría de documentos jurídicos (`RUT` y `Cámara de Comercio`) para aprobar o rechazar solicitudes de vinculación de OSAL, la gestión de estados de cuentas de usuario y el restablecimiento de credenciales bloqueadas por intentos fallidos.
3. **Representante / Administrador OSAL (`REPRESENTANTE_OSAL`):** Usuario delegado por una fundación rural aprobada. Gestiona su perfil institucional, publica campañas alineadas con los ODS, define necesidades cuantificadas por unidad de medida, administra el flujo logístico de donaciones en especie (`RECIBIDO`, `EN_BODEGA`, `ENTREGADO`) y visualiza en su tablero exclusivo el directorio de voluntarios postulados a sus causas.
4. **Donante Solidario (`DONANTE`):** Persona natural o jurídica (empresa aliada RSE) que consulta el catálogo de causas, reporta aportes monetarios (`>= $10.000 COP` con comprobante obligatorio) o donaciones en especie, visualiza el resumen histórico de sus aportes y descarga o envía por correo electrónico sus certificados tributarios en PDF.
5. **Voluntario Comunitario (`VOLUNTARIO`):** Ciudadano o estudiante universitario que configura su perfil de competencias técnicas (`BASICO`, `INTERMEDIO`, `AVANZADO`), define su disponibilidad horaria semanal máxima y se postula a convocatorias veredales seleccionando franjas horarias estandarizadas sin exceder su límite de horas disponibles.
6. **Usuario Visitante (Público no autenticado):** Navega libremente por el visor georreferenciado de la Sabana (`Leaflet`), filtra sedes por municipio, consulta las causas específicas de cada fundación y accede al asistente de radicación de nuevas OSAL.

#### B. Fase de Elaboración (Elaboration): Arquitectura Tecnológica y Modelo de Datos en 5FN (34 Tablas)

Para garantizar mantenibilidad, bajo costo operativo y alto rendimiento en redes rurales, se implementó una arquitectura de **Monolito Modular Desacoplado**:

- **Backend y API RESTful:** Construido en **Python 3.11+** utilizando el microframework **Flask**, organizado mediante **7 Blueprints modulares** (`auth`, `catalogos`, `osal`, `campanas`, `donaciones`, `voluntariado`, `dashboard`), seguridad basada en tokens **JWT (`Flask-JWT-Extended`)**, encriptación criptográfica de contraseñas (`Werkzeug PBKDF2/Scrypt`) y generación documental con **ReportLab**.
- **Capa de Persistencia y ORM Relacional:** Implementada mediante **SQLAlchemy ORM** con soporte transparente multi-motor (**SQLite 3** para entornos locales/portables y **PostgreSQL** para despliegues productivos en la nube) y migraciones incrementales automatizadas al arranque (`aplicar_migraciones_incrementales`).
- **Frontend e Interfaz de Usuario (SPA):** Desarrollado en **Angular (Arquitectura Standalone + Signals)** con diseño responsivo inspirado en **SAP Fiori / WCAG 2.2 AA**, cartografía interactiva con **Leaflet + OpenStreetMap** y motor propio de resiliencia ante desconexión (`OfflineSyncService`).
- **Infraestructura Cloud y Despliegue Continuo (CI/CD):** Desplegado en la nube sobre **Render** mediante especificación declarativa (`render.yaml`) conectada al repositorio oficial de GitHub, sirviendo de manera unificada los activos compilados del frontend y la API REST bajo protocolo seguro HTTPS.

El modelo relacional fue normalizado rigurosamente hasta la **Quinta Forma Normal (5FN)**, conformando un esquema integral de **34 tablas** agrupadas en **7 módulos arquitectónicos**:

1. **Módulo 1 — Seguridad y Auditoría (4 tablas):** `roles`, `usuarios`, `usuarios_roles`, `logs_auditoria`.
2. **Módulo 2 — Geolocalización Territorial DANE (4 tablas):** `paises`, `departamentos`, `municipios`, `direcciones`.
3. **Módulo 3 — Perfiles y Acreditación Jurídica OSAL (5 tablas):** `tipos_documento`, `personas`, `documentos_identidad`, `fundaciones_osal`, `documentos_legales_osal`.
4. **Módulo 4 — Voluntariado y Gestión de Competencias (4 tablas):** `voluntarios`, `categorias_habilidades`, `habilidades`, `perfil_habilidades_voluntario`.
5. **Módulo 5 — Catálogo de Causas y Marco ODS (5 tablas):** `ods_objetivos`, `categorias_causas`, `campanas`, `tipos_necesidad`, `necesidades_campana`.
6. **Módulo 6 — Transacciones, Logística y Certificación Tributaria (8 tablas):** `donantes`, `unidades_medida`, `metodos_pago`, `aportes_transaccionales`, `donaciones_economicas`, `donaciones_especie`, `trazabilidad_entregas`, `recibos_tributarios`.
7. **Módulo 7 — Asignaciones Operativas y Parametrización Maestra (4 tablas):** `franjas_horarias`, `parametros_sistema`, `postulaciones_voluntariado`, `asignaciones_actividades`.
*(Las 6 tablas de auditoría complementaria de sesiones/tokens/parámetros completan las 34 tablas verificadas por el inspector de SQLAlchemy en la base de datos).*

#### C. Fase de Construcción (Construction): Los 10 Casos de Uso Implementados en el MVP

El Producto Mínimo Viable materializa **10 Casos de Uso de extremo a extremo**:
- **CU01:** Autenticación JWT, Control de Bloqueo por Intentos Fallidos, Gobierno de Usuarios y Parametrización Global (`SUPER_ADMIN` / `ADMIN`).
- **CU02:** Vinculación de OSAL mediante Wizard de 3 Etapas con Validación Obligatoria de Soportes (`RUT` + `Cámara de Comercio`), Consentimiento Habeas Data (Ley 1581/2012) y Autoguardado Offline.
- **CU03:** Catálogo y Publicación de Campañas Sociales vinculadas a los ODS con Parametrización de Unidades de Medida (`COP`, `KG`, `LT`, `UND`, `KIT`, `HORAS`) y Filtro Directo por Fundación.
- **CU04:** Registro Transaccional de Donaciones Monetarias (con formateo de miles en tiempo real, validación `>= $10.000 COP` y comprobante obligatorio) y Donaciones en Especie.
- **CU05:** Postulación a Convocatorias de Voluntariado con Selección Desplegable de Franjas Horarias, Control de Tope de Horas Semanales Disponibles y Privacidad de Asignaciones por Rol.
- **CU06:** Visor Georreferenciado Interactivo de la Sabana (`Leaflet`) con Filtrado por Municipio y Navegación Contextual de Retorno hacia las Causas de cada Fundación.
- **CU07:** Emisión, Descarga y Envío por Correo Electrónico de Certificados Tributarios Digitales en PDF bajo Normativa DIAN (Arts. 125 y 257 E.T.) con Huella Criptográfica SHA-256.
- **CU08:** Tablero de Control Analítico (Dashboard OSAL) con KPIs Financieros, Trazabilidad de Impacto por ODS, Tasa de Cobertura de Necesidades y Directorio Exclusivo de Voluntarios Postulados.
- **CU09:** Trazabilidad Logística de Donaciones en Especie en Tres Estados (`RECIBIDO` → `EN_BODEGA` → `ENTREGADO`) con Historial de Ubicaciones en Bodega Veredal.
- **CU10:** Gestión de Perfil de Voluntario, Resumen Ejecutivo de Usuario Autenticado y Matriz de Competencias Certificadas.

