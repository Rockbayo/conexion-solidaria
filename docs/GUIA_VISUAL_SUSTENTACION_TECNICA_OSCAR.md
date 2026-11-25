# GUÍA MAESTRA VISUAL DE SUSTENTACIÓN INTEGRAL (OSCAR ROBAYO)
**Proyecto:** CONEXIÓN SOLIDARIA. TECNOLOGÍA PARA EL CAMBIO SOCIAL  
**URL del MVP en Producción (Render):** https://conexion-solidaria.onrender.com/login  

## 1. Cómo Responde el Proyecto a los 6 Objetivos Específicos
| Objetivo Específico | Meta del Objetivo | Cómo lo Cumplimos (Respuesta Clara para el Jurado) |
|---|---|---|
| **OE1 (Diagnóstico - Fase Inicio RUP)** | Identificar necesidades de las OSAL rurales y levantar requerimientos. | Encuesta a 4 fundaciones (Cajicá, Machetá, Simijaca, La Calera: 100 % adopción) y 170 ciudadanos (64,7 % no conoce OSAL locales; 95,9 % usaría el portal). De ahí salieron los 5 roles, 12 Requisitos Funcionales y 6 No Funcionales. |
| **OE2 (Estrategia - Modelo Canvas)** | Diseñar el modelo de negocio Canvas y validar propuesta de valor. | Plataforma 100 % gratuita (0 % comisión) para las fundaciones. Separación total de cuentas: las donaciones van directo a cada fundación y el portal se sostiene con patrocinios empresariales RSE, convocatorias, reportes y aportes. |
| **OE3 (Diseño Técnico - Fase Elaboración RUP)** | Definir arquitectura, prototipos UI/UX, casos de uso y BD en 5FN. | Arquitectura ligera de 3 capas para zonas rurales, 10 Casos de Uso principales, interfaz accesible para celular y base de datos de 34 tablas en Quinta Forma Normal sin datos repetidos. |
| **OE4 (Desarrollo MVP - Fase Construcción RUP)** | Desarrollar el Producto Mínimo Viable (MVP) de forma modular. | Aplicación web desplegada en Render (https://conexion-solidaria.onrender.com/login) con Angular 17 en la parte visual y Python/Flask con 6 módulos (Blueprints) en el servidor. |
| **OE5 (Validación - Fase Transición RUP)** | Validar el desempeño técnico y funcional con pruebas de calidad. | 15 casos de prueba ejecutados con 5 fundaciones referentes de la Sabana: 100 % aprobados, tiempo de respuesta promedio de 19,8 milisegundos y paquetes livianos menores a 7,5 KB. |
| **OE6 (Sostenibilidad - Planes y Finanzas)** | Proyectar planes organizacional, operativo, mercadeo y financiero. | Constitución como Fundación en el Régimen Tributario Especial (RTE) y Memoria de Cálculo a 5 años trazable: inversión en efectivo Año 0 de $3,21 millones, capital semilla de $8,38 millones y autosostenibilidad desde el Año 2. |

## 2. Normatividad Aplicada en la Plataforma y el Emprendimiento
| Norma / Ley | Qué Exige la Norma | Cómo Está Aplicada en Conexión Solidaria |
|---|---|---|
| **Acuerdo 012 de 2024 y Guía ADOr006_V10 (UdeC)** | Reglamenta la Ruta de Emprendimiento e Innovación y el Plan de Vida Emprendedor articulado con el MEDIT. | El proyecto entrega el plan de emprendimiento completo, el MVP funcional en la nube y la reflexión emprendedora al servicio de 18 municipios de la Sabana. |
| **Ley 1581 de 2012 y Decreto 1377 de 2013 (Habeas Data)** | Protección de datos personales y autorización expresa e informada del titular. | En el Paso 3 del registro el botón no se activa si no se marca la casilla de autorización, y la base de datos guarda la fecha y hora exacta de aceptación. |
| **Estatuto Tributario (Arts. 19, 125-1, 257 y 356) y Ley 1819** | Régimen Tributario Especial (RTE) para fundaciones y descuento del 25 % en impuesto de renta por donaciones. | El sistema genera automáticamente el Certificado Tributario de Donación en PDF tras la confirmación de la fundación, facilitando el descuento del 25 % a donantes y empresas RSE. |
| **Ley 527 de 1999 (Comercio Electrónico y Mensajes de Datos)** | Da validez jurídica a los documentos, transacciones y firmas digitales en Colombia. | Cada donación confirmada y cada certificado PDF emitido por la plataforma lleva impreso un sello digital único (código hash) que garantiza su autenticidad. |
| **Ley 720 de 2001 (Ley de Voluntariado)** | Reconoce y regula la acción voluntaria formal en entidades sin ánimo de lucro. | El módulo de voluntariado formaliza las convocatorias con tareas claras, horarios, cupos controlados y registro de horas comprometidas. |
| **Directiva 04 de 2012 (Cero Papel) y Ley 1672 (RAEE)** | Eficiencia administrativa eliminando papel físico y gestión ambiental responsable. | Reemplaza los cuadernos manuales, planillas impresas de voluntarios y recibos en papel de las fundaciones rurales por registros y certificados 100 % digitales. |

## 3. Los 9 Objetivos de Desarrollo Sostenible (ODS) que Impacta
| Nivel de Impacto | ODS Vinculados | Cómo se Materializa en la Plataforma |
|---|---|---|
| **Impacto Directo de la Plataforma (5 ODS)** | ODS 1 (Fin de la pobreza), ODS 9 (Industria, innovación e infraestructura), ODS 10 (Reducción de las desigualdades), ODS 11 (Comunidades sostenibles) y ODS 17 (Alianzas para lograr los objetivos). | Se cumplen directamente al entregar infraestructura web gratuita a zonas rurales, cerrar la brecha digital entre el campo y la ciudad y conectar universidades, empresas y fundaciones. |
| **Impacto Misional a través de las Fundaciones (4 ODS)** | ODS 2 (Hambre cero), ODS 3 (Salud y bienestar), ODS 4 (Educación de calidad) y ODS 15 (Vida de ecosistemas terrestres y fauna). | Se cumplen y se miden en el Dashboard del sistema a través de las campañas de mercados campesinos, cuidado del adulto mayor, refuerzo escolar infantil, reforestación y rescate animal. |

## 4. Esbozo Ejecutivo de la Parte Financiera (Tus 5 Puntos para Respaldar a Angélica)
| Eje Financiero | Cifra Exacta de la Memoria de Cálculo | Explicación Sencilla y Contundente |
|---|---|---|
| **1. ¿De dónde salen los números? (Trazabilidad)** | Del archivo Memoria_Calculo_Conexion_Solidaria.xlsx (15 hojas con fórmulas, cero cifras inventadas). | Usa datos oficiales de 2026: Salario mínimo ($1.750.905) con factor prestacional 1,52 sobre 182 horas/mes (Ley 2101); inflación DANE (6,30 %); dólar TRM ($3.309,55); UVB ($12.110) para Cámara de Comercio; y precios públicos de Render. |
| **2. Inversión Inicial (Año 0 = $28,51 millones COP)** | Se divide en dos partes: Aporte en especie ($25,30 millones = 88,7 %) y Dinero en efectivo ($3,21 millones = 11,3 %). | Los $25,30 millones ya los pusimos Angélica y yo con las 640 horas de programación del software y nuestros equipos. En efectivo solo se necesitan $3.217.062 para constituir la fundación, pagar contador RTE, dominio .org.co, 1 mes de Render y la reserva de riesgos ($2.176.396). |
| **3. Costos Operativos del Año 1 ($16,23 millones COP)** | Equivale a $1.352.592 al mes para atender a las primeras 25 fundaciones verificadas. | El servidor y base de datos en Render cuestan apenas $3.233.935 al año (US$62/mes, unos $270.000/mes con IVA). El resto es verificación y talleres en veredas ($5,09 M, donde el 50 % de horas lo apoyan practicantes), contador RTE ($5,45 M) y mercadeo ($1,91 M). |
| **4. Ingresos del Año 1 ($11,80 millones COP) y Capital Semilla ($8,38 millones)** | En el Año 1 los ingresos cubren el 72,7 % de los costos mientras despega la gestión comercial (déficit de -$4,43 M). | En el Año 1 entran los primeros 3 patrocinadores RSE ($6,9 M), convocatorias ($4,5 M) y aportes ($0,4 M). Como el mes 6 es el punto donde más caja se necesita, se requiere un capital semilla total de $8.382.661 COP que cubre la inversión en efectivo y todo el déficit del Año 1. |
| **5. Autosostenibilidad desde el Año 2 y Crecimiento a 5 Años** | De 25 fundaciones en el Año 1 pasamos a 60 en el Año 2, 120 en el Año 3 y 200 en el Año 5. | Al pasar de 3 empresas patrocinadoras en el Año 1 a 7 en el Año 2 y 13 en el Año 3 (apenas el 2 % de las 650 empresas del corredor industrial), los ingresos superan a los gastos: cubren el 117,2 % en el Año 2, el 109 % en el Año 3 y el 103,7 % en el Año 4, recuperando el efectivo en 2,88 años. |

---

## DIAPOSITIVA 6 DEL PPT | 1. Cómo la Ingeniería responde a los Objetivos, la Normatividad y los 9 ODS (PARTE 1 (Minutos 0 a 4))
**Conexión con el Proyecto:** `Objetivos Específicos OE1 a OE6 · Acuerdo 012 (MEDIT) · Marco Legal y 9 ODS`

![Figuras 1 y 2. Alineación con los Objetivos de Desarrollo Sostenible (ODS) y Ciclo de Vida en las 4 fases de la metodología RUP](c:\Users\ingor\conexion-solidaria\docs\figuras_originales\Conexión_Solidaria_T_p4_img1_1439x292.jpeg)
![Figuras 1 y 2. Alineación con los Objetivos de Desarrollo Sostenible (ODS) y Ciclo de Vida en las 4 fases de la metodología RUP - Segunda Imagen](c:\Users\ingor\conexion-solidaria\docs\figuras_originales\Conexión_Solidaria_T_p6_img1_1120x1020.jpeg)
*Figuras 1 y 2. Alineación con los Objetivos de Desarrollo Sostenible (ODS) y Ciclo de Vida en las 4 fases de la metodología RUP*

### ¿Qué señalar en esta pantalla?
- Conectar de entrada tu parte técnica con lo que acaba de exponer Angélica: explicar que la plataforma no se programó al azar, sino que cada módulo responde a las encuestas (OE1), al modelo gratuito del Canvas (OE2), a la normativa colombiana y a 9 Objetivos de Desarrollo Sostenible.
- Señalar las 4 fases de la metodología RUP (Inicio, Elaboración, Construcción y Transición) ejecutadas en 16 semanas.

### Guion fluido sugerido para decir:
> «Muchas gracias, Angélica. Para que el modelo social que acabamos de ver funcione en la vida real, diseñamos y construimos la plataforma tecnológica Conexión Solidaria guiados por las cuatro fases de la metodología RUP: Inicio, Elaboración, Construcción y Transición. Lo más importante de nuestra ingeniería es que cada elemento del software responde directamente a los objetivos del proyecto, a la ley colombiana y a nueve Objetivos de Desarrollo Sostenible: cinco ODS los impactamos de forma directa al llevar infraestructura digital gratuita al campo y crear alianzas regionales —que son los ODS 1, 9, 10, 11 y 17—, y cuatro ODS los medimos a través de las causas de alimentación, salud, educación y medio ambiente de las fundaciones —los ODS 2, 3, 4 y 15—. Además, incorporamos la normatividad directamente dentro del código del sistema: la Ley 1581 de Habeas Data en el registro obligatorio, el Estatuto Tributario y la Ley 527 de comercio electrónico en los certificados PDF con sello digital, la Ley 720 en el agendamiento formal de voluntariado y la política de Cero Papel al digitalizar toda la operación.»

**Resumen clave en una línea:** 9 ODS (5 directos: 1, 9, 10, 11, 17 | 4 indirectos: 2, 3, 4, 15) + Metodología RUP en 4 fases (16 semanas / 640 horas).

---

## DIAPOSITIVA 7 DEL PPT | 2. Arquitectura Ligera para Zonas Rurales, Conexión Front-Back y Base de Datos de 34 Tablas (PARTE 2 (Minutos 4 a 8))
**Conexión con el Proyecto:** `Objetivos Específicos OE3 y OE4 · Requisitos No Funcionales RNF01 a RNF06 · Caso de Prueba CP-15`

![Figura 3. Modelo Entidad-Relación (MER) de 34 tablas en Quinta Forma Normal (5FN) diseñado en MySQL Workbench](c:\Users\ingor\conexion-solidaria\docs\figuras_originales\MER.png)
*Figura 3. Modelo Entidad-Relación (MER) de 34 tablas en Quinta Forma Normal (5FN) diseñado en MySQL Workbench*

### ¿Qué señalar en esta pantalla?
- Explicar de forma sencilla las 3 capas del sistema (Frontend en Angular, Backend en Python/Flask con 6 Blueprints y Base de Datos en SQLAlchemy) y cómo se comunican sin tecnicismos enredados.
- Señalar el diagrama de la base de datos de 34 tablas en Quinta Forma Normal divididas en 5 grupos.

### Guion fluido sugerido para decir:
> «Para cumplir nuestros seis Requisitos No Funcionales —especialmente que la plataforma cargue rápido en veredas con señal celular 3G regular y que el servidor sea muy económico de mantener—, construimos una arquitectura ligera de tres capas cien por ciento de código abierto: La primera capa es la parte visual o Frontend, hecha en Angular 17 con mapas libres de Leaflet y OpenStreetMap; está configurada con carga diferida para que el teléfono del usuario solo descargue la pantalla que está consultando en ese momento. La segunda capa es el servidor o Backend, hecho en Python con Flask y organizado en seis módulos independientes llamados Blueprints: autenticación, fundaciones, necesidades, voluntariado, donaciones y tablero de indicadores. ¿Cómo se conectan la pantalla en Angular y el servidor en Flask? Se comunican por internet enviándose paquetes de datos JSON muy livianos, de menos de 7,5 kilobytes, protegidos con una llave digital de sesión llamada token JWT. Y la tercera capa es esta Base de Datos que vemos en pantalla, diseñada en MySQL Workbench y conectada con SQLAlchemy, lo que nos permite usarla igual en SQLite local o en PostgreSQL en la nube de Render. La normalizamos hasta la Quinta Forma Normal con 34 tablas organizadas en cinco grupos: catálogos geográficos con los 18 municipios de la Sabana, catálogos de los 9 ODS y unidades de medida, usuarios y roles con auditoría de la Ley 1581, perfil jurídico de las fundaciones con sus sedes veredales, y las tablas de campañas, donaciones, certificados y voluntariado. Usar Quinta Forma Normal con tablas puente garantiza que nunca se repita ni se contradiga la información.»

**Resumen clave en una línea:** 3 Capas: Angular 17 + Leaflet (Front) <--> JSON + Token JWT <--> Python/Flask con 6 Blueprints (Back) <--> BD 5FN con 34 tablas en 5 grupos.

---

## DIAPOSITIVA 8 DEL PPT | 3. Identidad Social, Inicio de Sesión Seguro y los 5 Roles del Sistema (CU02 / RF02) (PARTE 3 (Minutos 8 a 11))
**Conexión con el Proyecto:** `Requisito Funcional RF02 y No Funcional RNF05 · Caso de Uso CU02 · Casos de Prueba CP-03 y CP-04`

![Figura 4. Portal de bienvenida con identidad social territorial y control de acceso por los 5 Roles (/login)](c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h06_login_roles.png)
*Figura 4. Portal de bienvenida con identidad social territorial y control de acceso por los 5 Roles (/login)*

### ¿Qué señalar en esta pantalla?
- Señalar el logo oficial de Conexión Solidaria, la vitrina fotográfica con las 4 líneas sociales reales (Adulto Mayor Campesino, Educación y Niñez, Protección Animal y Campamentos de Vida Nueva) y los 5 roles del sistema.
- Explicar que desde las encuestas definimos 5 roles y 12 Requisitos Funcionales que se viven en 10 Casos de Uso principales.

### Guion fluido sugerido para decir:
> «Veamos ahora cómo funcionan en pantalla nuestros doce Requisitos Funcionales y los diez Casos de Uso principales en la aplicación. Aquí vemos la pantalla de bienvenida con nuestra identidad institucional y la vitrina de las causas reales del territorio —adulto mayor campesino, niñez rural, protección animal y rehabilitación comunitaria—, donde se ejecuta el Caso de Uso número dos y el requisito funcional dos: la autenticación y el control de acceso por cinco roles: Visitante público, Donante, Voluntario, Representante de Fundación y Superadministrador. Cuando una persona inicia sesión, el servidor verifica su contraseña encriptada en solo 42 milisegundos y le entrega una llave digital temporal que indica qué rol tiene. Como comprobamos en los casos de prueba tres y cuatro, cada rol ve únicamente lo que le corresponde: un visitante o un donante jamás puede entrar al panel administrativo de una fundación ni al panel de aprobación del sistema.»

**Resumen clave en una línea:** 5 Roles con permisos separados | Caso de Uso 2 (RF02) validado en Casos de Prueba CP-03 y CP-04.

---

## DIAPOSITIVA 9 DEL PPT | 4. Registro de Fundación en 3 Pasos y Protección de Datos Ley 1581 (CU01 / RF01) (PARTE 4 (Minutos 11 a 14))
**Conexión con el Proyecto:** `Requisito Funcional RF01 y No Funcionales RNF02, RNF05 · Caso de Uso CU01 · Casos de Prueba CP-01 y CP-02`

![Figuras 5 y 6. Asistente de Registro de Fundación en 3 pasos: Datos jurídicos (Paso 1) y Documentos legales + Ley 1581 (Paso 3)](c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h04_wizard_paso1.png)
![Figuras 5 y 6. Asistente de Registro de Fundación en 3 pasos: Datos jurídicos (Paso 1) y Documentos legales + Ley 1581 (Paso 3) - Segunda Imagen](c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h05_wizard_paso3_habeas.png)
*Figuras 5 y 6. Asistente de Registro de Fundación en 3 pasos: Datos jurídicos (Paso 1) y Documentos legales + Ley 1581 (Paso 3)*

### ¿Qué señalar en esta pantalla?
- Mostrar cómo el registro se dividió en 3 pasos sencillos para líderes rurales (requisito de usabilidad RNF02).
- Señalar en la segunda imagen los dos candados legales: adjuntar RUT y Cámara de Comercio, y marcar el check obligatorio de la Ley 1581 de 2012.

### Guion fluido sugerido para decir:
> «En estas dos pantallas vemos el Caso de Uso número uno, que cumple el requisito funcional uno: el registro y vinculación de una fundación rural. Pensando en que muchos líderes comunitarios no son expertos en tecnología, dividimos el formulario en tres pasos muy cortos que toman en promedio cuatro minutos: en el Paso 1 ingresan el NIT, nombre y misión de la fundación; en el Paso 2 ubican su municipio y vereda en la Sabana; y en el Paso 3, que vemos a la derecha, pusimos dos controles legales obligatorios: primero, deben subir su RUT de la DIAN y su Certificado de Cámara de Comercio; y segundo, deben marcar la casilla de autorización de tratamiento de datos personales de la Ley 1581 de 2012. Como validamos en los casos de prueba uno y dos, si no marcan esa casilla el sistema no deja enviar el formulario, y cuando la marcan guarda la fecha y hora exacta en la base de datos. Además, la fundación entra en estado Pendiente de Validación para que ninguna entidad sin verificar aparezca ante el público.»

**Resumen clave en una línea:** Caso de Uso 1 (RF01) | Cumple Ley 1581 de 2012 y filtro antifraude documental | Validado en CP-01 y CP-02.

---

## DIAPOSITIVA 10 DEL PPT | 5. Mapa Interactivo y Directorio Georreferenciado de la Sabana (CU03 / RF03) (PARTE 5 (Minutos 14 a 17))
**Conexión con el Proyecto:** `Requisito Funcional RF03 y No Funcional RNF01 · Caso de Uso CU03 · Caso de Prueba CP-05`

![Figura 7. Visor Georreferenciado de Organizaciones Rurales con fotografías reales y sello de verificación](c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h01_mapa.png)
*Figura 7. Visor Georreferenciado de Organizaciones Rurales con fotografías reales y sello de verificación*

### ¿Qué señalar en esta pantalla?
- Señalar el mapa de la Sabana con las ubicaciones de las fundaciones en veredas de Cogua, Tabio, Chía, Cajicá y Zipaquirá, y las tarjetas de la derecha con fotografías reales y el sello verde 'VERIFICADA'.
- Conectar con el objetivo OE1: resuelve que el 64,7 % de los 170 ciudadanos encuestados no conocía las fundaciones de su municipio.

### Guion fluido sugerido para decir:
> «Una vez verificados sus documentos, la fundación pasa a estar visible en esta pantalla, que corresponde al Caso de Uso número tres y al requisito funcional tres: el Visor Georreferenciado y Directorio de Organizaciones Rurales. Este módulo responde directamente al diagnóstico del primer objetivo específico, donde descubrimos que ninguna de las cuatro fundaciones encuestadas usaba página web propia para difundir sus causas y que el 64,7 % de los ciudadanos desconocía las organizaciones de su entorno. Aquí cualquier ciudadano puede explorar el mapa de los municipios de la Sabana, filtrar por su municipio, ver la fotografía real de la labor comunitaria, su dirección veredal exacta, comprobar que tiene el sello verde de Verificada y entrar en un clic a conocer sus causas. En el caso de prueba cinco comprobamos que cargar este mapa y directorio toma apenas 18,4 milisegundos.»

**Resumen clave en una línea:** Caso de Uso 3 (RF03) | Resuelve el 64,7 % de desconocimiento ciudadano y el 0 % de web propia | Respuesta en 18,4 ms (CP-05).

---

## DIAPOSITIVA 11 DEL PPT | 6. Catálogo de Campañas, Metas en Dinero o Especie y Alertas de Acopio (CU04, CU05 / RF04, RF11) (PARTE 6 (Minutos 17 a 20))
**Conexión con el Proyecto:** `Requisitos Funcionales RF04 y RF11 · Casos de Uso CU04 y CU05 · Caso de Prueba CP-06`

![Figuras 8 y 9. Catálogo visual de Causas Comunitarias vinculadas a los ODS con metas en pesos y en unidades físicas](c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h02_catalogo_filtrado.png)
![Figuras 8 y 9. Catálogo visual de Causas Comunitarias vinculadas a los ODS con metas en pesos y en unidades físicas - Segunda Imagen](c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h03_publicar_campana_unidades.png)
*Figuras 8 y 9. Catálogo visual de Causas Comunitarias vinculadas a los ODS con metas en pesos y en unidades físicas*

### ¿Qué señalar en esta pantalla?
- Señalar cómo cada campaña luce las fotografías reales de los abuelos campesinos, niños, animales rescatados y campamentos juveniles junto con la etiqueta del ODS que impacta, la barra de meta en dinero y los contadores exactos de insumos en especie.
- Mencionar que también cubre el requisito funcional 11 (alertas de centros de acopio en emergencias).

### Guion fluido sugerido para decir:
> «En estas dos capturas vemos los Casos de Uso cuatro y cinco, que cumplen los requisitos funcionales cuatro y once: la publicación y consulta de campañas y necesidades comunitarias. En nuestras encuestas vimos que la falta de recursos es el problema número uno de las fundaciones y que el 32,4 % de la comunidad prefiere donar insumos físicos como alimentos o materiales en lugar de dinero. Por eso nuestro catálogo presenta cada causa con su fotografía real en terreno y maneja metas duales: muestra a qué Objetivo de Desarrollo Sostenible aporta, en qué vereda está, cuánto dinero lleva recaudado frente a su meta y cuántas unidades físicas de insumos se han reunido —como kits de semillas en Cogua, mercados para abuelos campesinos en Zipaquirá o kilos de concentrado para perros rescatados en Cajicá—, permitiendo además destacar centros de acopio urgentes cuando ocurre una emergencia municipal.»

**Resumen clave en una línea:** Casos de Uso 4 y 5 (RF04 y RF11) | Metas duales en Pesos (COP) y en Especie (Kilos, Mercados, Kits) | Validado en CP-06.

---

## DIAPOSITIVA 12 DEL PPT | 7. Confirmación Bilateral de Donaciones y Certificado Tributario PDF (CU06, CU07 / RF07, RF08, RF09) (PARTE 7 (Minutos 20 a 24))
**Conexión con el Proyecto:** `Requisitos Funcionales RF07, RF08 y RF09 · Casos de Uso CU06 y CU07 · Casos de Prueba CP-07, CP-08 y CP-09`

![Figuras 10 y 11. Registro y confirmación bilateral de donaciones y Certificado Tributario en PDF con código hash de seguridad](c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h09_donaciones_transaccional.png)
![Figuras 10 y 11. Registro y confirmación bilateral de donaciones y Certificado Tributario en PDF con código hash de seguridad - Segunda Imagen](c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h10_certificado_pdf.png)
*Figuras 10 y 11. Registro y confirmación bilateral de donaciones y Certificado Tributario en PDF con código hash de seguridad*

### ¿Qué señalar en esta pantalla?
- Explicar el flujo de confirmación en dos pasos que garantiza que ninguna donación falsa suba las barras de progreso (responde al 58,2 % de ciudadanos que exigió transparencia total).
- Señalar el Certificado Tributario en PDF: los datos de la fundación, del donante, la referencia a los Artículos 125-1 y 257 del Estatuto Tributario (25 % de descuento en renta) y el sello digital único SHA-256 abajo.

### Guion fluido sugerido para decir:
> «Estas dos pantallas muestran el flujo más importante para la confianza ciudadana, correspondiente a los Casos de Uso seis y siete y a los requisitos funcionales siete, ocho y nueve. Recordemos que en la encuesta a 170 ciudadanos, el 58,2 % nos dijo que su condición indispensable para donar es la transparencia total en el uso de los recursos. Para garantizarlo, implementamos un protocolo de confirmación bilateral: cuando un donante registra una ayuda en dinero o en especie, la donación queda en estado Pendiente con un código de seguimiento, pero la barra de avance de la campaña todavía NO sube, como probamos en el caso de prueba siete. Solo cuando la fundación revisa que el dinero o los insumos físicos realmente llegaron a su sede y confirma la recepción en su panel —caso de prueba ocho—, el sistema actualiza automáticamente el porcentaje de la meta, deja el registro en la bitácora de transparencia y habilita el Caso de Uso siete: la generación inmediata de este Certificado Tributario de Donación en PDF que vemos a la derecha. El certificado sale a nombre y NIT de la fundación rural receptora —porque el cien por ciento de la donación va directo a ella sin comisiones—, respalda el descuento tributario del 25 % en el impuesto de renta bajo el artículo 257 del Estatuto Tributario y lleva impreso en el pie de página un sello criptográfico único que impide cualquier alteración.»

**Resumen clave en una línea:** Casos de Uso 6 y 7 (RF07, RF08, RF09) | Responde al 58,2 % que exige transparencia + Cumple Art. 125-1 y 257 E.T. y Ley 527 | Validado en CP-07, CP-08 y CP-09.

---

## DIAPOSITIVA 13 DEL PPT | 8. Convocatorias y Postulación a Voluntariado con Control de Cupos (CU08, CU09 / RF05, RF06) (PARTE 8 (Minutos 24 a 26))
**Conexión con el Proyecto:** `Requisitos Funcionales RF05 y RF06 · Casos de Uso CU08 y CU09 · Casos de Prueba CP-10 y CP-11`

![Figuras 12 y 13. Inscripción a Voluntariado Comunitario con galería de jornadas reales y Panel del Voluntario](c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h08_postulacion_voluntariado.png)
![Figuras 12 y 13. Inscripción a Voluntariado Comunitario con galería de jornadas reales y Panel del Voluntario - Segunda Imagen](c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h07_resumen_voluntario.png)
*Figuras 12 y 13. Inscripción a Voluntariado Comunitario con galería de jornadas reales y Panel del Voluntario*

### ¿Qué señalar en esta pantalla?
- Mostrar cómo se formaliza la acción voluntaria bajo la Ley 720 de 2001: la galería de jornadas reales en terreno, la selección de actividad, horario, habilidades y cupos, y el resumen personal del voluntario.
- Señalar cómo al aprobarse una postulación se descuenta el cupo automáticamente.

### Guion fluido sugerido para decir:
> «En estas dos pantallas vemos los Casos de Uso ocho y nueve, que cumplen los requisitos funcionales cinco y seis bajo el marco de la Ley 720 de Voluntariado. En la encuesta vimos que el voluntariado presencial es la forma de participación más frecuente con el 35,3 %, pero que las personas exigen claridad en las tareas y horarios. Aquí la fundación publica sus jornadas indicando fecha, franja horaria, habilidades requeridas y número exacto de cupos. El voluntario selecciona la actividad que se ajusta a su perfil y horario, se postula y, cuando la fundación lo acepta —como comprobamos en los casos de prueba diez y once—, el sistema descuenta automáticamente el cupo disponible en tiempo real y le muestra en su panel sus horas comprometidas y las tareas asignadas.»

**Resumen clave en una línea:** Casos de Uso 8 y 9 (RF05 y RF06) | Responde al 35,3 % de voluntariado y 21,8 % de claridad en tareas | Cumple Ley 720 de 2001 (CP-10 y CP-11).

---

## DIAPOSITIVA 14 DEL PPT | 9. Tablero de Impacto por los 9 ODS, Panel SuperAdmin y Pruebas QA (CU10 / RF10, RF12) (PARTE 9 (Minutos 26 a 28))
**Conexión con el Proyecto:** `Objetivos OE4 y OE5 · Requisitos Funcionales RF10 y RF12 · Caso de Uso CU10 · Casos de Prueba CP-12, CP-13 y CP-14`

![Figuras 14 y 15. Tablero de Indicadores de Impacto por ODS con evidencia territorial y Panel SuperAdmin de verificación](c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h11_dashboard_ods.png)
![Figuras 14 y 15. Tablero de Indicadores de Impacto por ODS con evidencia territorial y Panel SuperAdmin de verificación - Segunda Imagen](c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h12_superadmin_parametros.png)
*Figuras 14 y 15. Tablero de Indicadores de Impacto por ODS con evidencia territorial y Panel SuperAdmin de verificación*

### ¿Qué señalar en esta pantalla?
- Señalar en el Dashboard el mosaico de evidencia territorial, el recaudo total verificado, las horas de voluntariado y los bloques de cumplimiento por cada Objetivo de Desarrollo Sostenible.
- Señalar en el Panel SuperAdmin la revisión del RUT y Cámara de Comercio de las fundaciones antes de aprobarlas, y cerrar con los resultados de los 15 Casos de Prueba QA.

### Guion fluido sugerido para decir:
> «Cerramos el recorrido funcional con el Caso de Uso número diez, que cumple los requisitos funcionales diez y doce: En la primera imagen vemos el Tablero de Control e Indicadores de Impacto por ODS. Como el 75 % de las fundaciones encuestadas no tenía cómo medir métricas, el sistema calcula automáticamente el recaudo verificado, la cobertura de necesidades, las horas de voluntariado y el avance aportado a cada uno de los Objetivos de Desarrollo Sostenible, generando así los reportes de impacto para las empresas patrocinadoras. En la segunda imagen vemos el Panel del Superadministrador, desde donde nuestro equipo revisa los archivos PDF del RUT de la DIAN y la Cámara de Comercio de cada fundación antes de darle clic al botón Aprobar Fundación. Con este despliegue en Render validamos el quinto objetivo específico ejecutando 15 casos de prueba funcional y de rendimiento: los 15 fueron aprobados al cien por ciento, logrando un tiempo promedio de respuesta del servidor de apenas 19,8 milisegundos y paquetes menores a 7,5 kilobytes, diez veces más rápido que el límite exigido para zonas rurales.»

**Resumen clave en una línea:** Caso de Uso 10 (RF10 y RF12) | 15/15 Casos de Prueba QA Aprobados | Respuesta media: 19,8 ms (< 200 ms) y Payload < 7,5 KB (CP-12, CP-13, CP-14).

---

## DIAPOSITIVA 15 DEL PPT | 10. Conexión entre Ingeniería de Bajo Costo y Sostenibilidad Financiera a 5 Años (OE6) (PARTE 10 (Minutos 28 a 30 — Conexión con la Parte Financiera))
**Conexión con el Proyecto:** `Objetivo Específico OE6 · Memoria de Cálculo Trazable a 5 Años (Anexo J) y Gestión de Riesgos`

![Figura 16. Respaldo del modelo gratuito (100 % adopción de fundaciones) conectado con la Memoria de Cálculo Financiera a 5 años](c:\Users\ingor\conexion-solidaria\docs\figuras_originales\encuesta_fundaciones_desafios_y_modulos.png)
*Figura 16. Respaldo del modelo gratuito (100 % adopción de fundaciones) conectado con la Memoria de Cálculo Financiera a 5 años*

### ¿Qué señalar en esta pantalla?
- Demostrar que como CTO también dominas perfectamente los números financieros que pidieron los jurados Jorge Iván Ortiz y Jairo Fernando Henao en su concepto.
- Conectar el bajo costo técnico de tu arquitectura en Render ($3,23 millones al año / ~$270.000 al mes) con la sostenibilidad financiera a 5 años.

### Guion fluido sugerido para decir:
> «Finalmente, para conectar esta arquitectura técnica con el sexto objetivo específico y el plan financiero que detallamos en la Memoria de Cálculo en Excel, quiero destacar cómo nuestras decisiones de ingeniería hacen que la fundación sea económicamente viable sin cobrarle un solo peso a las organizaciones rurales: Primero: de la inversión inicial del Año cero, que suma 28,5 millones de pesos, nosotros dos como cofundadores ya pusimos en especie el 88,7 % —25,3 millones de pesos representados en las 640 horas de desarrollo del software y nuestros equipos—. Por eso la inversión en efectivo del Año cero es de solo 3,21 millones de pesos para constituir legalmente la fundación en Cámara de Comercio, comprar el dominio y dejar guardada la reserva de riesgos de 2,17 millones. Segundo: gracias a nuestra arquitectura ligera sobre tecnologías libres, mantener encendido todo el servidor cloud, la base de datos y el dominio en Render cuesta apenas 3,23 millones de pesos en todo el primer año —62 dólares al mes, cerca de 270 mil pesos mensuales con IVA—. Sumando el contador del Régimen Tributario Especial, la verificación documental apoyada en un 50 % por practicantes universitarios y el mercadeo, operar la fundación en el Año uno para las primeras 25 fundaciones cuesta 16,23 millones de pesos. Tercero: en el primer año proyectamos ingresos conservadores por 11,8 millones de pesos con los primeros 3 patrocinadores empresariales RSE y convocatorias, cubriendo el 72,7 % de los gastos. Para cubrir tanto la inversión en efectivo como el despegue del primer año hasta el mes seis, determinamos un capital semilla total de 8,38 millones de pesos. Y cuarto: a partir del Año dos la fundación es autosostenible, cubriendo el 117,2 % de sus costos en el Año dos y el 109 % en el Año tres al pasar de 3 a 13 empresas patrocinadoras, lo que representa menos del 2 % de las 650 empresas del corredor industrial de la Sabana, quienes además descuentan el 25 % de lo donado en su impuesto de renta.»

**Resumen clave en una línea:** Cifras financieras infalibles: Inversión especie = $25,30 M (640 h) | Efectivo Año 0 = $3,21 M (incluye reserva riesgos $2,17 M) | Render Año 1 = $3,23 M (US$62/mes) | Egresos Año 1 = $16,23 M | Ingresos Año 1 = $11,80 M (72,7 %) | Capital Semilla = $8,38 M | Superávit desde Año 2 (117,2 %).

---
