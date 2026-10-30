# Borrador 2 (Anexo E): Matriz de Trazabilidad Integral, Requerimientos (RF/RNF), Matriz RBAC y Especificación de Casos de Uso RUP

> **Propósito de este documento:** Subsanar la **Observación #1** (*"definir una trazabilidad explícita del problema, objetivo general, objetivos específicos, actividades, indicadores y resultados. Si el propósito es presentar un MVP, el impacto social se debe presentar como una hipótesis por validar"*) y estructurar el **Anexo E (Requerimientos funcionales y no funcionales)** junto con los insumos para los apartados `2.6.4`, `3.7.2` y `5.4.1` del documento principal.

---

## 1. Matriz Maestra de Trazabilidad del Proyecto (Problema ↔ Objetivos ↔ Modelo Canvas ↔ Ingeniería del MVP ↔ Hipótesis de Impacto)

Esta matriz articula de extremo a extremo la formulación del emprendimiento social con la ingeniería del software:

| Eje del Problema Identificado (Cap. 1.3 y 3.5) | Objetivo Específico Asociado (Cap. 1.4.2) | Bloque del Modelo Canvas (Cap. 4.3) | Proceso Operativo del Servicio (Cap. 5.2) | Requerimientos del Sistema (RF / RNF) | Caso de Uso y Módulo MVP (Cap. 5.4) | Entidades 5FN Principales (BD) | Indicador Empírico de Validación de Hipótesis en el MVP (Cap. 5.5) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **P1. Desconfianza ciudadana e informalidad jurídica** en la captación de recursos por redes sociales. | **OE1 / OE3:** Identificar necesidades y definir arquitectura de validación institucional. | **Propuesta de Valor / Relaciones con Clientes:** Legitimidad y verificación oficial sin costo. | **5.2.2.** Registro, verificación documental DIAN/CCB y activación de OSAL. | `RF01`, `RF02`, `RF11`, `RNF04`, `RNF05` | **CU01** (Gobierno RBAC) y **CU02** (Wizard Vinculación OSAL + Habeas Data). | `usuarios`, `roles`, `fundaciones_osal`, `documentos_legales_osal`, `logs_auditoria` | **Indicador IV-01:** % de solicitudes OSAL radicadas con expediente legal completo (`RUT` + `Cámara de Comercio` + `Ley 1581`) y auditadas antes de publicar causas (**Meta MVP: 100%**). |
| **P2. Baja visibilidad geográfica** de las fundaciones que operan en veredas de la Sabana Centro y Norte. | **OE2 / OE3:** Estructurar canales de visibilidad territorial y prototipos UI/UX accesibles. | **Canales / Segmentos de Clientes:** Directorio georreferenciado regional. | **5.2.1 / 5.2.3.** Visibilización territorial y difusión de causas por municipio. | `RF03`, `RF04`, `RNF01`, `RNF02` | **CU06** (Visor Georreferenciado `Leaflet`) y **CU03** (Catálogo filtrado por fundación). | `municipios`, `direcciones`, `fundaciones_osal`, `campanas`, `ods_objetivos` | **Indicador IV-02:** Número de municipios y veredas georreferenciadas con navegación directa hacia el catálogo de causas de cada fundación (**Verificado: 10 municipios y 5 sedes piloto**). |
| **P3. Déficit de financiación y falta de control en donaciones en especie** (pérdida de trazabilidad en acopios). | **OE4:** Desarrollar el MVP mediante programación modular (Fase Construcción RUP). | **Actividades Clave / Propuesta de Valor:** Canalización sin comisiones y trazabilidad logística. | **5.2.5.** Gestión de donaciones monetarias, acopio en especie y emisión de certificados. | `RF05`, `RF06`, `RF07`, `RF08`, `RNF04` | **CU04** (Registro Donación), **CU07** (Certificado PDF DIAN) y **CU09** (Trazabilidad Logística). | `aportes_transaccionales`, `donaciones_economicas`, `donaciones_especie`, `trazabilidad_entregas`, `recibos_tributarios`, `unidades_medida` | **Indicador IV-03:** % de donaciones monetarias con soporte verificado y certificado tributario SHA-256 emitido (`100%`), y % de despachos en especie con estado logístico trazable (`RECIBIDO`/`EN_BODEGA`/`ENTREGADO`). |
| **P4. Desarticulación en el reclutamiento de voluntarios** (incompatibilidad de horarios y perfiles). | **OE4 / OE5:** Construir y validar el módulo de coordinación de talento humano voluntario. | **Recursos Clave / Aliados Clave:** Red de voluntariado universitario y ciudadano. | **5.2.4.** Perfilamiento por competencias, postulación y asignación horaria. | `RF09`, `RF10`, `RNF02`, `RNF04` | **CU05** (Postulación con franjas y tope de horas) y **CU10** (Perfil de Habilidades). | `voluntarios`, `habilidades`, `perfil_habilidades_voluntario`, `franjas_horarias`, `postulaciones_voluntariado`, `asignaciones_actividades` | **Indicador IV-04:** Tasa de asignación efectiva de horas de voluntariado respetando el límite de disponibilidad semanal del voluntario y privacidad por rol (**Meta MVP: 100% sin sobreasignación**). |
| **P5. Conectividad rural inestable y altos costos de licenciamiento TI** para las OSAL. | **OE5 / OE6:** Validar desempeño técnico en entorno rural y proyectar sostenibilidad financiera. | **Estructura de Costos / Fuentes de Ingresos:** Operación cloud de bajo costo financiada por aliados. | **5.2.6 / 5.2.7.** Soporte técnico, operación offline y gobierno parametrizable. | `RF12`, `RNF01`, `RNF03`, `RNF06` | **CU01** (Panel `SUPER_ADMIN`), **CU08** (Dashboard ODS) y `OfflineSyncService`. | `parametros_sistema`, `ods_objetivos`, `unidades_medida`, `franjas_horarias` | **Indicador IV-05:** Tiempo de respuesta API `< 250 ms`, cero pérdida de formularios ante corte de red (`localStorage`), y costo de infraestructura Cloud `< $65.000 COP/mes` por lote de fundaciones. |

---

## 2. Especificación Detallada de Requerimientos Funcionales (`RF01` – `RF12`)

| Código | Nombre del Requerimiento | Descripción Funcional y Regla de Negocio Verificable | Prioridad | Caso de Uso Asociado |
| :--- | :--- | :--- | :---: | :---: |
| **RF01** | **Autenticación JWT y Control de Bloqueo por Intentos** | El sistema debe autenticar usuarios mediante correo y contraseña encriptada, emitiendo un token JWT con sus roles y alcance institucional. Si un usuario acumula el número máximo de intentos fallidos parametrizado (`MAX_INTENTOS_LOGIN = 5`), la cuenta debe bloquearse automáticamente (`esta_activo = False`) y registrar el evento en `logs_auditoria`. | Alta | `CU01` |
| **RF02** | **Gobierno de Usuarios y Jerarquía de Superusuario** | El sistema debe proveer un panel administrativo donde `ADMIN` y `SUPER_ADMIN` puedan listar usuarios, activar/inactivar cuentas y restablecer contraseñas. Únicamente el rol `SUPER_ADMIN` está facultado para crear nuevos usuarios con rol `ADMIN`. | Alta | `CU01` |
| **RF03** | **Vinculación Estructurada de OSAL con Soportes Obligatorios y Habeas Data** | El sistema debe guiar el registro de nuevas fundaciones en un asistente (*wizard*) de 3 etapas (Datos Institucionales, Ubicación Veredal/Representante y Soportes Legales). Debe impedir la radicación si no se adjuntan ambos documentos obligatorios (**RUT DIAN** y **Certificado de Existencia y Representación Legal**) y la autorización expresa de **Habeas Data (Ley 1581 de 2012)**, dejando la entidad en estado `PENDIENTE`. | Alta | `CU02` |
| **RF04** | **Auditoría Documental y Activación Institucional de OSAL** | El sistema debe permitir a los roles `ADMIN` y `SUPER_ADMIN` inspeccionar los soportes jurídicos cargados por las fundaciones en estado `PENDIENTE` y cambiar su estado a `APROBADA` o `RECHAZADA`, actualizando simultáneamente el estado de revisión de sus documentos legales. | Alta | `CU01`, `CU02` |
| **RF05** | **Publicación de Campañas Sociales Vinculadas a ODS y Unidades de Medida** | El sistema debe permitir a las OSAL con estado `APROBADA` (y a los administradores) publicar campañas asociadas a un **Objetivo de Desarrollo Sostenible (`ODS 1, 2, 3, 4, 9, 10, 11, 15, 17`)** y a una categoría social, desglosando sus necesidades específicas con su respectiva **unidad de medida (`COP`, `KG`, `LT`, `UND`, `KIT`, `HORAS`)**. | Alta | `CU03` |
| **RF06** | **Visor Georreferenciado Territorial y Filtrado Contextual por Fundación** | El sistema debe mostrar en un mapa interactivo (`Leaflet`) las sedes veredales y urbanas de las OSAL aprobadas en la Sabana, permitiendo filtrar por municipio y navegar desde cada fundación hacia el catálogo filtrado exclusivamente por las campañas de dicha organización (`?fundacion_id=X`), incluyendo un botón de retorno directo al visor geográfico. | Alta | `CU06`, `CU03` |
| **RF07** | **Registro Controlado de Donaciones Monetarias y en Especie** | El sistema debe permitir a los donantes registrar aportes monetarios o en especie. Para aportes monetarios, el campo de importe debe aplicar separador de miles en tiempo real, prohibir valores decimales, exigir un monto mínimo parametrizable (`>= $10.000 COP`), obligar la carga del archivo de soporte/comprobante y exigir la referencia bancaria antes de afectar el libro transaccional. | Alta | `CU04` |
| **RF08** | **Certificación Tributaria Digital PDF (Norma DIAN) y Envío por Correo** | Por cada donación económica verificada, el sistema debe generar un recibo tributario único con hash criptográfico **SHA-256** y permitir su descarga en PDF con estructura de comprobante fiscal digital amparado en los **Arts. 125, 125-1, 125-2, 125-3 y 257 del Estatuto Tributario** y **Decreto 2150 de 2017**, así como su remisión al correo electrónico del donante con trazabilidad de envío. | Alta | `CU07` |
| **RF09** | **Trazabilidad Logística de Donaciones en Especie en Tres Estados** | El sistema debe permitir a los representantes de las OSAL y administradores actualizar y auditar el estado logístico de cada donación en especie a través de las etapas `RECIBIDO` → `EN_BODEGA` → `ENTREGADO`, registrando fecha, ubicación veredal/bodega y observaciones en `trazabilidad_entregas`. | Media | `CU09` |
| **RF10** | **Perfilamiento de Habilidades y Postulación Controlada de Voluntariado** | El sistema debe permitir a los voluntarios registrar sus habilidades (`BASICO`, `INTERMEDIO`, `AVANZADO`) y disponibilidad horaria semanal máxima. Al postularse a una labor comunitaria, el sistema debe exigir elegir una franja horaria de una lista desplegable parametrizada, impedir comprometer más horas de las disponibles en su perfil, bloquear postulaciones duplicadas y restringir la visibilidad para que cada voluntario vea únicamente sus propias asignaciones. | Alta | `CU05`, `CU10` |
| **RF11** | **Tablero de Control Analítico (Dashboard OSAL) e Indicadores por ODS** | El sistema debe presentar métricas ejecutivas (recaudo monetario vs. meta, campañas activas, tasa de cobertura de necesidades, horas de voluntariado, estado logístico en especie, avance agrupado por ODS y directorio detallado de voluntarios postulados con sus datos de contacto y habilidades), aplicando alcance por rol (cada OSAL ve sus propios indicadores y voluntarios; `ADMIN`/`SUPER_ADMIN` ven el consolidado regional). | Alta | `CU08` |
| **RF12** | **Parametrización Maestra de la Plataforma (`SUPER_ADMIN`)** | El sistema debe proveer una vista exclusiva para el rol `SUPER_ADMIN` que permita agregar o actualizar dinámicamente unidades de medida (`COP`, `KG`, `LT`, `UND`, `KIT`, `HORAS`), franjas horarias de voluntariado, categorías de causas, catálogo de habilidades y parámetros globales del sistema (`parametros_sistema`). | Media | `CU01` |

---

## 3. Especificación de Requerimientos No Funcionales (`RNF01` – `RNF06`)

| Código | Atributo de Calidad | Especificación Técnica y Métrica de Verificación en el MVP |
| :--- | :--- | :--- |
| **RNF01** | **Rendimiento y Resiliencia en Conectividad Rural Limitada** | El sistema debe operar de forma fluida sobre enlaces móviles rurales (3G/4G intermitentes). Los endpoints JSON deben responder en `< 250 ms` bajo carga local/regional, el mapa debe cargarse bajo demanda (*lazy-loading chunk*) y los formularios críticos deben contar con persistencia local (`OfflineSyncService` sobre `localStorage`) para evitar pérdida de datos ante caídas temporales de red. |
| **RNF02** | **Usabilidad, Accesibilidad e Inclusión Digital (WCAG 2.2 AA)** | Las interfaces deben emplear alto contraste tipográfico, etiquetas semánticas (`aria-label`, `role="status"`, `role="alert"`), retroalimentación cromática diferenciada (verde esmeralda `#15803D` para operaciones exitosas y rojo `#B91C1C` para alertas/duplicados), formateo numérico asistido y botones explícitos de finalización y retorno en cada flujo. |
| **RNF03** | **Desacoplamiento Arquitectónico y Mantenibilidad Modular** | Separación estricta entre la capa de presentación SPA (Angular Standalone Components + Signals) y la capa de servicios RESTful (Flask Blueprints + SQLAlchemy ORM), comunicadas exclusivamente mediante JSON sobre HTTP/HTTPS con políticas CORS controladas. |
| **RNF04** | **Seguridad, Integridad Criptográfica y Control RBAC** | Autenticación sin estado (*stateless*) mediante tokens JWT firmados (`HS256`), contraseñas almacenadas con *salted hash* (`Werkzeug Security`), validación de roles en servidor mediante el decorador `@requiere_roles`, bloqueo automático tras 5 intentos fallidos y firma de integridad **SHA-256** en todos los certificados tributarios PDF. |
| **RNF05** | **Integridad Referencial en Quinta Forma Normal (5FN)** | El esquema relacional de **34 tablas** debe garantizar ausencia de redundancias y anomalías de actualización mediante llaves primarias autoincrementales, llaves foráneas con políticas explícitas (`ON DELETE RESTRICT` / `CASCADE` / `SET NULL`) y restricciones de unicidad compuesta (`UniqueConstraint`). |
| **RNF06** | **Portabilidad y Despliegue Continuo en Nube (Cloud-Native)** | La aplicación debe ser desplegable de manera automatizada sobre infraestructura PaaS (**Render**) a partir de un único archivo declarativo (`render.yaml`), compilando e integrando el frontend estático dentro del servidor WSGI (`Gunicorn`) para minimizar costos de infraestructura. |

---

## 4. Matriz de Control de Acceso Basado en Roles (`RBAC`)

| Módulo / Funcionalidad del Sistema | Ruta / Vista Angular | Endpoint API Principal | Visitante (Público) | `VOLUNTARIO` | `DONANTE` | `REPRESENTANTE_OSAL` | `ADMIN` | `SUPER_ADMIN` |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Mapa Territorial Sabana y Filtro por Sede** | `/mapa` | `GET /api/osal/mapa` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Catálogo Público de Causas (General y por OSAL)** | `/campanas` | `GET /api/campanas` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Asistente de Vinculación de Nueva OSAL (3 Pasos)** | `/registro-osal` | `POST /api/osal/registro` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Resumen Ejecutivo Personal al Iniciar Sesión** | `/panel` | `GET /api/auth/me` | ❌ | ✅ *(Sus postulaciones y horas)* | ✅ *(Sus aportes y recibos)* | ✅ *(Estado de su OSAL)* | ✅ *(Gobernanza)* | ✅ *(Gobierno Total)* |
| **Configuración de Habilidades y Disponibilidad** | `/perfil-habilidades` | `POST /api/voluntariado/perfil-habilidades` | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ |
| **Postulación a Convocatoria de Voluntariado** | `/voluntariado` | `POST /api/voluntariado/postular` | ❌ | ✅ *(Ve solo sus postulaciones)* | ❌ | ❌ *(Ve postulados a su OSAL)* | ✅ *(Ve todas)* | ✅ *(Ve todas)* |
| **Registro de Donaciones (Monetarias / Especie)** | `/donaciones` | `POST /api/donaciones/economicas` / `/especie` | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Descarga y Envío de Certificado Tributario PDF** | `/donaciones` | `GET /certificado-pdf` / `POST /enviar-correo` | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Publicación de Campañas con Unidades de Medida** | `/campanas` | `POST /api/campanas` | ❌ | ❌ | ❌ | ✅ *(Solo si OSAL está APROBADA)* | ✅ | ✅ |
| **Trazabilidad Logística de Acopio en Especie** | `/trazabilidad` | `PUT /api/donaciones/especie/<id>/trazabilidad` | ❌ | ❌ | ❌ *(Solo lectura)* | ✅ | ✅ | ✅ |
| **Dashboard Analítico e Impacto por ODS** | `/dashboard` | `GET /api/dashboard/osal` | ❌ | ❌ | ❌ | ✅ *(Métricas y voluntarios de su OSAL)* | ✅ *(Global)* | ✅ *(Global)* |
| **Aprobación / Rechazo Jurídico de OSAL** | `/panel` | `PUT /api/osal/<id>/estado` | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Administración de Usuarios y Restablecimiento Clave** | `/panel` | `GET/POST /api/auth/usuarios` | ❌ | ❌ | ❌ | ❌ | ✅ *(Excepto crear ADMIN)* | ✅ *(Incluye crear ADMIN)* |
| **Parametrización Maestra de la Plataforma** | `/panel` | `POST /api/catalogos/unidades-medida`, `/parametros`, etc. | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ *(Exclusivo)* |

---

## 5. Especificación Formal RUP de los 10 Casos de Uso (`CU01` a `CU10`)

### CU01 — Autenticación JWT, Administración de Usuarios y Parametrización Global
- **Actores:** Todos los roles autenticados (`SUPER_ADMIN`, `ADMIN`, `REPRESENTANTE_OSAL`, `DONANTE`, `VOLUNTARIO`).
- **Precondiciones:** El usuario debe existir en la tabla `usuarios` y encontrarse activo (`esta_activo = True`).
- **Flujo Principal:**
  1. El usuario ingresa su correo y contraseña en `/login`.
  2. El backend (`POST /api/auth/login`) verifica el hash de la contraseña. Si es válido, reinicia `intentos_fallidos = 0`, actualiza `ultimo_acceso`, registra el evento en `logs_auditoria` y retorna el token JWT junto con el perfil y resumen operativo del usuario.
  3. El frontend redirige automáticamente a `/panel`, mostrando el tablero contextual según el rol:
     - Si es `VOLUNTARIO` o `DONANTE`: visualiza su ficha resumen de actividad y accesos rápidos.
     - Si es `ADMIN`: accede a la bandeja de validación jurídica de OSAL y al módulo de administración de usuarios y restablecimiento de contraseñas.
     - Si es `SUPER_ADMIN`: accede adicionalmente a la creación de cuentas `ADMIN` y al módulo de **Parametrización Maestra de Plataforma** (unidades de medida, franjas horarias, categorías, habilidades y parámetros de sistema).
- **Flujo Alternativo (Bloqueo por Seguridad):** Si la contraseña falla 5 veces consecutivas (`MAX_INTENTOS_LOGIN`), el sistema cambia `esta_activo = False` y bloquea el acceso hasta que un `ADMIN` o `SUPER_ADMIN` restablezca la cuenta.

### CU02 — Vinculación de OSAL mediante Wizard de 3 Etapas y Validación Documental
- **Actores:** Representante de Fundación Rural (Visitante) y Administrador (`ADMIN` / `SUPER_ADMIN`).
- **Precondiciones:** Disponer de NIT, datos de localización rural y archivos digitales del RUT (DIAN) y Certificado de Cámara de Comercio.
- **Flujo Principal:**
  1. En el **Paso 1**, el solicitante registra NIT, razón social, sigla, misión y teléfono institucional. `OfflineSyncService` guarda automáticamente el borrador en `localStorage`.
  2. En el **Paso 2**, selecciona el municipio de la Sabana (cargando coordenadas base), indica vereda, dirección física e información del representante legal.
  3. En el **Paso 3**, adjunta obligatoriamente los archivos **RUT (DIAN)** y **Certificado de Existencia y Representación Legal**, y marca la casilla de **Autorización de Tratamiento de Datos Personales (Ley 1581 de 2012)**.
  4. Al radicar (`POST /api/osal/registro`), el sistema persiste en `direcciones`, `usuarios`, `personas`, `documentos_identidad`, `fundaciones_osal` (con `estado_validacion = 'PENDIENTE'` y `acepta_tratamiento_datos = True`) y `documentos_legales_osal`, presentando el botón **"Finalizar Proceso y Volver al Inicio"**.
  5. Posteriormente, el `ADMIN` revisa los soportes en `/panel` y aprueba la organización (`PUT /api/osal/<id>/estado`), habilitándola en el mapa y permitiéndole publicar campañas.

### CU03 — Publicación y Consulta de Campañas Sociales con Unidades de Medida
- **Actores:** `REPRESENTANTE_OSAL`, `ADMIN`, `SUPER_ADMIN` (publicación); todos los usuarios (consulta).
- **Precondiciones:** Para publicar, la fundación debe estar en estado `APROBADA`.
- **Flujo Principal:**
  1. El usuario accede a `/campanas`. Si proviene del Mapa Territorial (`?fundacion_id=X`), el sistema filtra exclusivamente las campañas de esa fundación y habilita el botón **"← Volver al Visor Georreferenciado"** y **"Ver todas las fundaciones"**.
  2. Para crear una campaña, el representante ingresa título, descripción, ODS asociado (`ODS 1` a `ODS 17`), categoría, meta económica en `COP`, fechas y agrega las necesidades específicas seleccionando para cada ítem el tipo (`ECONOMICA`, `ESPECIE`, `TIEMPO_VOLUNTARIADO`), la **unidad de medida (`COP`, `KG`, `LT`, `UND`, `KIT`, `HORAS`)**, la cantidad requerida y la prioridad.
  3. El sistema almacena la campaña en `campanas` y sus ítems en `necesidades_campana`.

### CU04 — Registro Transaccional de Donaciones Monetarias y en Especie
- **Actores:** `DONANTE`, `ADMIN`, `SUPER_ADMIN`.
- **Precondiciones:** Usuario autenticado y campaña activa seleccionada.
- **Flujo Principal:**
  1. En `/donaciones`, el donante selecciona la campaña destino y la modalidad (`Monetaria` o `Especie`).
  2. En modalidad **Monetaria**, digita el monto en pesos; el componente formatea automáticamente los separadores de miles (`$ 50.000`), impide decimales, valida que el importe sea **mínimo de `$10.000 COP`**, exige número de referencia bancaria y obliga a adjuntar el soporte digital de pago.
  3. En modalidad **Especie**, selecciona la unidad de medida (`KG`, `LT`, `UND`, `KIT`), cantidad, descripción de artículos y punto de entrega veredal.
  4. Al confirmar, el sistema registra el aporte en `aportes_transaccionales`, actualiza el avance de la campaña, crea el registro en `donaciones_economicas` (junto con su `recibo_tributario` SHA-256) o `donaciones_especie` (con estado inicial `RECIBIDO`) y muestra confirmación con botón de finalización.

### CU05 — Postulación a Voluntariado con Franjas Desplegables y Control de Horas
- **Actores:** `VOLUNTARIO`, `REPRESENTANTE_OSAL`, `ADMIN`, `SUPER_ADMIN`.
- **Precondiciones:** Existencia de requerimientos de tipo `TIEMPO_VOLUNTARIADO` activos.
- **Flujo Principal:**
  1. El voluntario ingresa a `/voluntariado`, donde visualiza el cupo de horas semanales disponibles según su perfil (`disponibilidad_horas_semana`).
  2. Selecciona la labor comunitaria, elige una **Franja Horaria Propuesta** desde la lista desplegable parametrizada (`franjas_horarias`), ajusta las horas a comprometer (el sistema bloquea valores superiores a su disponibilidad semanal) y redacta su motivación.
  3. Al enviar (`POST /api/voluntariado/postular`), si no se había postulado antes, el sistema crea el registro en `postulaciones_voluntariado` y `asignaciones_actividades`, incrementa las horas cubiertas de la necesidad y despliega alerta en **verde** con botón **"Finalizar y Ver Mi Resumen"**.
  4. Si ya existía postulación previa para esa labor, retorna código HTTP `409` y muestra alerta en **rojo** indicando la postulación previa. Cada voluntario solo visualiza sus propias postulaciones en la tabla inferior.

### CU06 — Exploración en Visor Georreferenciado de la Sabana (`Leaflet`)
- **Actores:** Todos los usuarios (incluyendo Visitante público).
- **Precondiciones:** Sedes de fundaciones aprobadas con coordenadas (`latitud`, `longitud`) en `direcciones`.
- **Flujo Principal:**
  1. El usuario accede a `/mapa`. El sistema carga los polígonos/marcadores sobre cartografía OpenStreetMap centrada en la Sabana de Cundinamarca.
  2. El usuario filtra por municipio (Chía, Cajicá, Zipaquirá, Tabio, Tenjo, Cogua, Sopó, Tocancipá, Gachancipá, Nemocón) o selecciona una sede en el directorio lateral.
  3. Al pulsar **"Ver causas de esta fundación"**, el sistema navega hacia `/campanas?fundacion_id=X`, mostrando exclusivamente las campañas de dicha entidad y el botón de regreso al mapa.

### CU07 — Emisión, Descarga y Envío por Correo de Certificado Tributario Digital (PDF)
- **Actores:** `DONANTE`, `ADMIN`, `SUPER_ADMIN`.
- **Precondiciones:** Donación económica registrada con consecutivo en `recibos_tributarios`.
- **Flujo Principal:**
  1. Desde el libro mayor de transacciones en `/donaciones`, el usuario localiza un aporte monetario.
  2. Al pulsar **"Descargar Certificado PDF"**, el endpoint `GET /api/donaciones/economicas/<id>/certificado-pdf` genera en memoria con `ReportLab` un comprobante fiscal digital con membrete institucional, datos de la OSAL beneficiaria, identificación del donante, desglose económico, citación expresa de los **Artículos 125, 125-1, 125-2, 125-3 y 257 del Estatuto Tributario Nacional y Decreto 2150 de 2017**, firma digital y código **SHA-256**.
  3. Al pulsar **"Enviar por Correo"**, el endpoint `POST /api/donaciones/economicas/<id>/enviar-correo` registra el despacho al correo del donante (`enviado_correo = True`, `correo_destino`, `fecha_envio_correo`) y notifica en pantalla.

### CU08 — Monitoreo en Tablero de Control (Dashboard OSAL) e Impacto por ODS
- **Actores:** `REPRESENTANTE_OSAL`, `ADMIN`, `SUPER_ADMIN`.
- **Precondiciones:** Usuario autenticado con rol institucional o administrativo.
- **Flujo Principal:**
  1. Al ingresar a `/dashboard`, el backend (`GET /api/dashboard/osal`) determina el alcance según el token JWT: si es `REPRESENTANTE_OSAL`, filtra las campañas de su fundación; si es `ADMIN`/`SUPER_ADMIN`, consolida toda la región.
  2. Presenta las tarjetas ejecutivas (Recaudo Monetario vs. Meta, Horas y Voluntarios Activos, Campañas y **Tasa de Cobertura de Necesidades %**, y Estado Logístico en Especie).
  3. Despliega la matriz de **Indicadores de Validación de Impacto por ODS**, el avance presupuestal por campaña y el **Directorio de Voluntarios Postulados** con su teléfono, correo, franja horaria y habilidades certificadas.

### CU09 — Gestión de Trazabilidad Logística de Donaciones en Especie
- **Actores:** `REPRESENTANTE_OSAL`, `ADMIN`, `SUPER_ADMIN` (edición); `DONANTE` (consulta).
- **Precondiciones:** Existencia de donaciones físicas en `donaciones_especie`.
- **Flujo Principal:**
  1. En `/trazabilidad`, el operador selecciona un despacho en especie y actualiza su estado (`RECIBIDO`, `EN_BODEGA`, `ENTREGADO`), indicando la bodega veredal o punto de entrega final y una observación de auditoría.
  2. El sistema actualiza `estado_logistico_actual` y agrega un nuevo hito cronológico en `trazabilidad_entregas`.

### CU10 — Configuración de Perfil de Habilidades y Disponibilidad de Voluntario
- **Actores:** `VOLUNTARIO`, `ADMIN`, `SUPER_ADMIN`.
- **Precondiciones:** Usuario autenticado con registro en `voluntarios`.
- **Flujo Principal:**
  1. En `/perfil-habilidades`, el voluntario actualiza su disponibilidad de horas por semana (`disponibilidad_horas_semana`), su disposición para desplazamiento rural y su biografía corta.
  2. Asocia competencias del catálogo normalizado (`habilidades`) indicando su nivel de dominio (`BASICO`, `INTERMEDIO`, `AVANZADO`) y años de experiencia, persistiendo en `perfil_habilidades_voluntario`.

