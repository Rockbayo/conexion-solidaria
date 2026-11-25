# -*- coding: utf-8 -*-
"""
Contenido académico completo del Capítulo 5, Cierre, Conclusiones, Recomendaciones y Referencias:
CONEXIÓN SOLIDARIA. TECNOLOGÍA PARA EL CAMBIO SOCIAL
Autores: Angélica Rosa Olier Quiroga y Oscar Giovanni Robayo Olaya
Universidad de Cundinamarca - Extensión Chía (2026)
"""

CAPITULO_5_Y_CIERRE = [
    # =========================================================================
    # CAPÍTULO 5. PLAN DE EMPRENDIMIENTO E IMPLEMENTACIÓN
    # =========================================================================
    ("H1", "CAPÍTULO 5. PLAN DE EMPRENDIMIENTO E IMPLEMENTACIÓN"),

    ("H2", "5.1. Plan organizacional"),
    ("P", "Siguiendo el sexto objetivo específico y los requisitos de la Guía ADOr006_V10 (Universidad de Cundinamarca, 2024), este apartado define cómo se organiza internamente el emprendimiento, quiénes conforman el equipo cofundador y cuál es la ruta legal para constituir la fundación."),

    ("H3", "5.1.1. Estructura organizacional propuesta"),
    ("P", "[[EDITAR]]Tomando como referencia el estudio sobre liderazgo en organizaciones sin fines de lucro de Caldeira (2015), se plantea una estructura liviana y sin exceso de cargos administrativos para que los recursos se concentren en mantener la plataforma y acompañar a las fundaciones rurales.[[/EDITAR]] La entidad cuenta con dos instancias de dirección y control (Asamblea de Fundadores / Junta Directiva y Contabilidad / Control Legal) y tres áreas operativas bajo la Dirección Ejecutiva: (1) Dirección de Tecnología y Desarrollo de Software; (2) Coordinación de Alianzas, Comunicaciones y Comunidad; y (3) Verificación Documental, Soporte y Práctica Social Universitaria."),

    ("H3", "5.1.2. Organigrama"),
    ("P", "Los tres niveles organizacionales de la Fundación Conexión Solidaria se resumen en la Tabla 12:"),
    ("TABLE", {
        "title": "Tabla 12. Estructura jerárquica y organigrama funcional de la Fundación Conexión Solidaria",
        "headers": ["Nivel Organizacional", "Órgano / Cargo", "Dependencia Jerárquica", "Función Misional Principal"],
        "rows": [
            ["Nivel 1: Dirección Estratégica y Control", "Asamblea de Fundadores y Junta Directiva", "Órgano supremo de gobierno estatutario", "Aprobar el direccionamiento estratégico, el presupuesto anual, la memoria de gestión y velar por el cumplimiento del objeto social."],
            ["Nivel 1: Control y Cumplimiento", "Asesoría Contable, Jurídica y Revisoría Fiscal (Externa)", "Asamblea de Fundadores", "Certificar estados financieros, supervisar la separación de fondos y asegurar el cumplimiento del Régimen Tributario Especial (RTE - DIAN)."],
            ["Nivel 2: Gerencia General", "Dirección Ejecutiva y de Alianzas Institucionales", "Junta Directiva", "Representar legalmente a la entidad, gestionar convenios con empresas RSE, alcaldías y universidades, y liderar la estrategia de comunicación."],
            ["Nivel 2: Dirección Técnica", "Dirección de Ingeniería, Arquitectura y Plataforma (CTO)", "Dirección Ejecutiva / Junta Directiva", "Liderar el desarrollo evolutivo de la plataforma web, administrar la base de datos en 5FN, la infraestructura cloud y la ciberseguridad."],
            ["Nivel 3: Operación y Soporte", "Coordinación de Verificación OSAL y Acompañamiento Rural", "Dirección Ejecutiva", "Ejecutar el protocolo de validación documental de las fundaciones, capacitar a los líderes rurales y auditar las campañas activas."],
            ["Nivel 3: Apoyo Técnico y Comunitario", "Practicantes y Voluntarios Universitarios (Sistemas y Comunicación)", "Dirección de Ingeniería y Coordinación OSAL", "Apoyar el soporte técnico de primer nivel a los usuarios, las pruebas de calidad de software y la difusión digital de las causas."]
        ],
        "note": "Nota. Elaboración propia conforme a los lineamientos de diseño organizacional de la Guía ADOr006_V10 (Universidad de Cundinamarca, 2024)."
    }),

    ("H3", "5.1.3. Roles y responsabilidades"),
    ("P", "A continuación se describen los perfiles de los dos cofundadores del proyecto y el manual resumido de cargos (Tabla 13):"),
    ("UL", [
        "Cofundadora - Directora Ejecutiva, de Estrategia Comunicativa y Experiencia de Usuario (UI/UX): Angélica Rosa Olier Quiroga. Estudiante de último semestre de Ingeniería de Sistemas y Computación de la Universidad de Cundinamarca (Extensión Chía). Cuenta con experiencia en diagnóstico aplicado al sector social, diseño de interfaces accesibles (WCAG 2.2), desarrollo frontend en Angular, planeación de comunicación digital y contacto con fundaciones de la Sabana Norte y Centro. Lidera la vinculación de las OSAL rurales, las alianzas RSE y las pruebas de usabilidad.",
        "Cofundador - Director de Tecnología, Arquitectura de Software y Gestión Financiera (CTO): Oscar Giovanni Robayo Olaya. Estudiante de último semestre de Ingeniería de Sistemas y Computación de la Universidad de Cundinamarca (Extensión Chía). Cuenta con dominio en arquitectura cliente-servidor, modelado de bases de datos relacionales en Quinta Forma Normal (5FN), programación backend en Python/Flask, pruebas de software (QA), seguridad JWT y SHA-256, despliegue cloud y presupuestos tecnológicos. Está a cargo del servidor, la base de datos y la evolución técnica de Conexión Solidaria."
    ]),
    ("TABLE", {
        "title": "Tabla 13. Manual sintético de roles, perfiles y responsabilidades clave del emprendimiento",
        "headers": ["Código", "Cargo / Rol", "Perfil y Conocimientos Requeridos", "Responsabilidades Específicas en la Operación"],
        "rows": [
            ["MF-001", "Dirección Ejecutiva y de Alianzas (Cofundadora)", "Ingeniera de Sistemas con énfasis en gestión de proyectos sociales, comunicación estratégica y UI/UX.", "(1) Suscribir convenios RSE y alianzas universitarias; (2) Dirigir el plan de marketing y posicionamiento regional; (3) Supervisar el cumplimiento de metas de impacto ODS."],
            ["MF-002", "Dirección de Tecnología y Arquitectura - CTO (Cofundador)", "Ingeniero de Sistemas con dominio en Python/Flask, Angular, SQL (5FN), seguridad web y administración cloud.", "(1) Administrar los servidores cloud y copias de seguridad de la base de datos; (2) Desarrollar nuevas funcionalidades; (3) Monitorear latencia (< 200 ms) y seguridad Habeas Data."],
            ["MF-003", "Analista de Verificación Documental y Soporte OSAL", "Profesional o estudiante de últimos semestres en áreas administrativas, sociales o de ingeniería.", "(1) Revisar RUT, Cámara de Comercio y cédula de representantes legales en menos de 48 horas; (2) Brindar asistencia vía WhatsApp/teléfono a líderes de fundaciones rurales."],
            ["MF-004", "Contador Público y Asesor Tributario ESAL (Honorarios)", "Contador Público con tarjeta profesional vigente y experiencia en Régimen Tributario Especial (RTE).", "(1) Llevar la contabilidad separada de la fundación; (2) Elaborar estados financieros anuales y declaración de renta RTE ante la DIAN; (3) Auditar soportes de certificados."],
            ["MF-005", "Practicante de Desarrollo y Comunidad Digital", "Estudiante de práctica social de Ingeniería de Sistemas, Diseño o Comunicación Social.", "(1) Apoyar jornadas de alfabetización digital en veredas; (2) Crear piezas gráficas de difusión de campañas urgentes; (3) Ejecutar pruebas regresivas del software."]
        ],
        "note": "Nota. Elaboración propia tomando como referencia el estándar de manual de funciones de Emprendimiento e Innovación UDEC."
    }),

    ("H3", "5.1.4. Recursos humanos requeridos"),
    ("P", "El equipo crece de forma gradual según los ingresos de los tres primeros años: en el Año 1 (meta de 25 OSAL), la operación la llevan directamente los dos cofundadores a tiempo parcial, con el apoyo de dos practicantes universitarios por convenio académico y un contador por honorarios para los cierres ante la DIAN. En los Años 2 y 3, a medida que entran nuevos patrocinios RSE, se amplían las horas de soporte técnico y acompañamiento en campo bajo las normas de la Ley 720 de 2001 y el Código Sustantivo del Trabajo (Congreso de la República de Colombia, 1950)."),

    ("H3", "5.1.5. Figura jurídica propuesta y requisitos de constitución"),
    ("P", "El emprendimiento se constituirá como una Entidad Sin Ánimo de Lucro (ESAL) bajo la figura de Fundación denominada Fundación Conexión Solidaria, con sede en Chía (Cundinamarca) e inscrita en la Cámara de Comercio de Bogotá (Sede Chía / Zipaquirá). Esta figura jurídica permite que el software quede destinado de forma permanente al servicio social (artículo 633 del Código Civil y Decreto 2150 de 1995) y que la entidad solicite su ingreso al Régimen Tributario Especial (RTE) ante la DIAN (artículos 19 y 356 del Estatuto Tributario), entregando así beneficio tributario a las empresas patrocinadoras."),
    ("P", "Actualmente el proyecto se encuentra en etapa pre-constitutiva (con estatutos y costos listos para radicación al iniciar la operación comercial). Los seis pasos de formalización son: (1) firma del acta de constitución y estatutos; (2) pre-RUT en la DIAN; (3) registro en Cámara de Comercio de Bogotá; (4) apertura de cuenta bancaria y RUT definitivo con responsabilidad 04 (RTE); (5) registro ante la Gobernación de Cundinamarca; y (6) solicitud de calificación en el RTE en el portal web de la DIAN."),

    ("H2", "5.2. Plan operativo"),
    ("P", "El plan operativo detalla cómo funciona la plataforma en el día a día, qué equipos e infraestructura requiere y cuánto toma cada proceso (Universidad de Cundinamarca, 2024)."),

    ("H3", "5.2.1. Procesos de prestación del servicio"),
    ("P", "La capacidad operativa del sistema se mide en fundaciones activas, tiempos de validación documental y disponibilidad del servidor. La Tabla 14 muestra la secuencia y los tiempos en minutos de los seis procesos principales:"),
    ("TABLE", {
        "title": "Tabla 14. Capacidad productiva instalada y flujograma secuencial de procesos operativos con tiempos y movimientos",
        "headers": ["Código Proceso", "Nombre del Proceso Operativo", "Secuencia de Actividades (Flujo del Proceso)", "Actor Responsable", "Tiempo Estándar por Ciclo"],
        "rows": [
            ["PR-01", "Registro y validación documental de OSAL", "1. Diligenciamiento del asistente web en 3 pasos y aceptación Ley 1581 (8 min).\n2. Almacenamiento en estado Pendiente en tabla fundaciones_osal (automático < 1 s).\n3. Revisión documental de RUT, Cámara de Comercio y representante legal (25 min).\n4. Aprobación en panel SuperAdmin y activación en mapa público (2 min).", "Representante OSAL / Analista de Verificación", "35 minutos de trabajo efectivo (SLA de respuesta: < 24 a 48 horas)."],
            ["PR-02", "Publicación de campaña y necesidades de recursos", "1. Ingreso al panel autenticado de la OSAL (1 min).\n2. Creación de campaña indicando título, municipio, ODS asociados y meta (4 min).\n3. Parametrización de ítems de dinero o insumos en especie y unidades (3 min).\n4. Publicación inmediata en el catálogo y mapa georreferenciado (< 1 s).", "Administrador OSAL", "8 minutos por campaña publicada."],
            ["PR-03", "Gestión de convocatorias y postulación voluntaria", "1. Publicación de vacante por la OSAL con cupos, fecha y habilidades (4 min).\n2. Exploración de convocatoria por el voluntario y clic en postulación (2 min).\n3. Validación automática de cupos disponibles y registro en BD (< 1 s).\n4. Confirmación de asistencia y cierre de jornada por la OSAL (3 min).", "Administrador OSAL / Voluntario", "9 minutos acumulados por postulación gestionada."],
            ["PR-04", "Registro de donación, verificación y certificado", "1. Selección de necesidad por el donante y registro de aporte en dinero/especie (3 min).\n2. Generación automática de código de trazabilidad en estado Pendiente (< 1 s).\n3. Verificación de recepción física/bancaria por la OSAL y cambio a Confirmada (3 min).\n4. Cálculo automático de avance de meta y emisión de certificado PDF con hash (< 1 s).", "Donante / Administrador OSAL / Sistema", "6 minutos de validación humana + procesamiento instantáneo."],
            ["PR-05", "Atención, soporte y acompañamiento a usuarios", "1. Recepción de consulta técnica o solicitud de apoyo vía canal de soporte (2 min).\n2. Diagnóstico del requerimiento o guía asistida paso a paso al líder rural (15 min).\n3. Cierre del caso y actualización de guía de preguntas frecuentes (3 min).", "Equipo de Soporte / Practicante", "20 minutos por solicitud de acompañamiento."],
            ["PR-06", "Mantenimiento preventivo y respaldo cloud", "1. Ejecución automatizada de copia de seguridad (backup) de base de datos 5FN (2 min).\n2. Verificación de métricas de latencia (< 200 ms), logs de seguridad y SSL (10 min).\n3. Despliegue continuo desde rama principal de GitHub ante mejoras (5 min).", "Director de Tecnología (CTO)", "17 minutos por rutina semanal de mantenimiento."]
        ],
        "note": "Nota. Elaboración propia conforme al requisito de flujogramas con tiempos y movimientos de la Guía ADOr006_V10 (Universidad de Cundinamarca, 2024)."
    }),

    ("H3", "5.2.2. Registro y validación de organizaciones"),
    ("P", "[[EDITAR]]Para que una fundación rural se registre sin enredos pero con total seguridad legal, dividimos el formulario en solo tres pasos cortos:[[/EDITAR]] (1) Datos básicos (nombre, NIT, tipo de entidad y misión); (2) Ubicación en la Sabana (municipio, vereda, coordenadas en el mapa y WhatsApp); y (3) Causas, ODS y aceptación obligatoria de la Ley 1581 de 2012. Al enviarlo, la fundación queda en estado Pendiente hasta que el administrador revisa su RUT y Cámara de Comercio y le activa el sello de verificada."),

    ("H3", "5.2.3. Gestión de necesidades y campañas"),
    ("P", "Ya verificada, la fundación puede abrir campañas desde su panel y especificar qué necesita: ya sea dinero en pesos o insumos físicos medidos por unidades concretas (bultos o kilos de concentrado, paquetes de pañales, mercados, kits escolares o medicamentos) indicando si la urgencia es baja, media, alta o crítica."),

    ("H3", "5.2.4. Gestión de voluntarios"),
    ("P", "En la sección de voluntariado la fundación publica la actividad, el municipio, la fecha, las habilidades que busca y cuántos cupos tiene. Cuando un voluntario se postula y es aceptado, el sistema descuenta el cupo automáticamente para evitar sobrecupos."),

    ("H3", "5.2.5. Gestión de donaciones y transparencia"),
    ("P", "[[EDITAR]]Una donación reportada por un usuario no sube la barra de progreso de inmediato: primero entra como Pendiente con su código de rastreo.[[/EDITAR]] Solo cuando la fundación confirma en su panel que sí recibió el dinero o los insumos físicos, el sistema actualiza el porcentaje alcanzado de la meta y habilita la descarga del certificado en PDF con código hash SHA-256."),

    ("H3", "5.2.6. Atención y acompañamiento a usuarios"),
    ("P", "Sabemos que entregar una página web no basta si el líder rural no sabe usarla (Gargallo Castel & Pérez Sanz, 2009; Winocur, 2007). Por eso cada fundación nueva recibe acompañamiento inicial paso a paso (en visita o por llamada) para subir su primera campaña, y cuenta con un canal directo de WhatsApp atendido por el equipo y los practicantes."),

    ("H3", "5.2.7. Mantenimiento y soporte tecnológico"),
    ("P", "El mantenimiento técnico incluye copias de seguridad diarias de la base de datos, revisión semanal de que los tiempos de respuesta sigan por debajo de 200 ms, renovación de certificados SSL y actualizaciones desde GitHub sin tumbar el servicio."),

    ("H2", "5.3. Plan de marketing y comunicación"),
    ("P", "A partir del estudio de mercado del Capítulo 3 y de la Guía ADOr006_V10 (Universidad de Cundinamarca, 2024), se definen las metas de crecimiento, las 4P del mercadeo con su presupuesto y los canales de difusión."),

    ("H3", "5.3.1. Objetivos de marketing"),
    ("UL", [
        "Objetivo 1 (Fundaciones vinculadas): Cerrar el Año 1 con 25 OSAL rurales verificadas en la Sabana (entre 2 y 3 nuevas por mes), pasando a 60 en el Año 2 y a 120 en el Año 3.",
        "Objetivo 2 (Donantes y voluntarios): Llegar a 500 usuarios registrados en el primer año y al menos 180 ayudas o postulaciones confirmadas.",
        "Objetivo 3 (Empresas patrocinadoras RSE): Suscribir en el Año 1 al menos 5 convenios de patrocinio empresarial que cubran el presupuesto anual."
    ]),

    ("H3", "5.3.2. Estrategias de posicionamiento"),
    ("P", "Conexión Solidaria se proyecta como un puente cercano y transparente entre el campo y la ciudad en la Sabana. La Tabla 15 resume la estrategia de las 4P (Producto, Precio, Plaza y Promoción) y el presupuesto anual asignado:"),
    ("TABLE", {
        "title": "Tabla 15. Estrategia de mezcla de mercadeo (4P: Producto, Precio, Plaza y Promoción) y presupuesto anual de marketing",
        "headers": ["Variable (4P)", "Estrategia Definida para Conexión Solidaria", "Acciones Tácticas Concretas", "Presupuesto Anual (Año 1 COP)"],
        "rows": [
            ["Producto (Servicio Digital Social)", "Plataforma web centralizada con sello de verificación legal OSAL, mapa interactivo por ODS, gestión de donaciones/voluntariado y certificado PDF.", "Mantenimiento de interfaz accesible WCAG 2.2, destaque de campañas urgentes y generación de reportes de impacto regional para aliados.", "Incluido en OPEX tecnológico ($2.580.000 COP)."],
            ["Precio (Esquema de Gratuidad y Patrocinio)", "• Tarifa $0 COP y comisión 0 % para las OSAL rurales, donantes y voluntarios.\n• Planes de Patrocinio RSE para empresas aliadas.", "• Plan RSE Bronce: $1.500.000 COP/año.\n• Plan RSE Plata: $3.000.000 COP/año.\n• Plan RSE Oro: $5.000.000 COP/año.", "Sin costo de recaudo (transferencia institucional directa)."],
            ["Plaza (Canales de Distribución y Cobertura)", "Distribución 100 % digital vía web responsiva (HTTPS) combinada con presencia territorial en los 18 municipios de Sabana Centro y Norte.", "Optimización SEO local por municipio (Chía, Cajicá, Zipaquirá, Cogua, Tabio, etc.) y códigos QR en campus universitarios y alcaldías.", "$420.000 COP (material impreso QR y desplazamientos veredales)."],
            ["Promoción (Comunicación y Difusión)", "Marketing de contenidos con enfoque de impacto real (storytelling de las fundaciones rurales), relaciones públicas universitarias y prospección B2B.", "Campañas en redes sociales, boletines de impacto trimestrales, ferias de voluntariado universitario y visitas a empresas industriales.", "$1.380.000 COP (pauta digital segmentada y piezas audiovisuales)."]
        ],
        "note": "Nota. Presupuesto total específico de mercadeo y promoción en el Año 1: $1.800.000 COP. Elaboración propia."
    }),

    ("H3", "5.3.3. Estrategias de captación de organizaciones sociales"),
    ("P", "Como muchas fundaciones rurales no aparecen en buscadores de internet, las contactamos por tres vías prácticas: revisando los listados de desarrollo social de las alcaldías y Cámaras de Comercio de la Sabana; llamando o visitando directamente a sus directores para ayudarles a subir su perfil; y por recomendación voz a voz entre los mismos líderes comunitarios."),

    ("H3", "5.3.4. Estrategias de captación de donantes y voluntarios"),
    ("P", "Para convocar voluntarios trabajamos de la mano con las oficinas de Bienestar y Proyección Social de las universidades de Chía, Cajicá y Zipaquirá, llevando el enlace del mapa a las jornadas universitarias. Para sumar donantes difundimos en redes sociales historias cortas de cada fundación con el enlace directo a la barra de avance de la necesidad, de modo que en tres clics puedan registrar su ayuda."),

    ("H3", "5.3.5. Estrategias de alianzas y patrocinio"),
    ("P", "En el frente empresarial visitamos a los departamentos de sostenibilidad o recursos humanos de las empresas ubicadas en Tocancipá, Gachancipá, Sopó, Zipaquirá, Cajicá y Chía. Les proponemos tres formas de vincularse: patrocinar el sostenimiento anual de la plataforma, organizar jornadas de voluntariado corporativo con sus trabajadores en las veredas cercanas o apadrinar necesidades puntuales de las fundaciones recibiendo su certificado tributario (RTE)."),

    ("H3", "5.3.6. Canales digitales y comunicación"),
    ("P", "Se manejan dos tipos de canales: el canal directo, compuesto por la aplicación web Conexión Solidaria y el WhatsApp institucional; y los canales multiplicadores, que incluyen Instagram, Facebook, LinkedIn (para contacto con empresas RSE) y las carteleras digitales de bienestar universitario."),

    ("H3", "5.3.7. Plan de contenidos y difusión"),
    ("P", "Para no caer en publicaciones sueltas sin propósito como advertía Huertas Jiménez (2015), la difusión semanal sigue cuatro temas fijos: presentación de una fundación rural de la Sabana, difusión de una necesidad urgente con su porcentaje de avance, agenda de voluntariado del fin de semana y fotos de las entregas ya verificadas."),

    ("H3", "5.3.8. Indicadores de marketing"),
    ("P", "El avance comercial se mide cada mes con cinco datos: nuevas OSAL verificadas (meta: 2 a 3 por mes en el Año 1), costo de adquisición por fundación (menos de $36.000 COP), porcentaje de visitantes que donan o se postulan (meta >= 8 %), porcentaje de usuarios que vuelven a participar en el semestre (meta >= 35 %) y cumplimiento de la meta de patrocinios RSE."),

    ("H2", "5.4. Plan técnico y desarrollo del MVP"),
    ("P", "El desarrollo técnico del sistema de información Conexión Solidaria se fundamenta en los principios metodológicos del Proceso Unificado de Rational (RUP), organizando el trabajo en las fases de Inicio, Elaboración, Construcción y Transición (Ortega, 2022; Pressman & Maxim, 2020), tal como se ilustra en la Figura 6."),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\Conexión_Solidaria_T_p6_img1_1120x1020.jpeg",
        "caption": "Figura 6. Articulación metodológica del ciclo de vida del proyecto Conexión Solidaria",
        "note": "Nota. Adaptado del diseño metodológico e ingenieril del proyecto (Olier & Robayo, 2025)."
    }),

    ("H3", "5.4.1. Requerimientos del sistema"),
    ("P", "El MVP construido cumple los doce Requerimientos Funcionales (RF01 a RF12) y los seis Requerimientos No Funcionales (RNF01 a RNF06) definidos en el Capítulo 2, cubriendo los diez casos de uso del sistema (CU01 a CU10: desde el registro y validación de la OSAL con aceptación de la Ley 1581 de 2012, el mapa interactivo por municipio y ODS, las campañas y necesidades, las convocatorias de voluntariado y el reporte de donaciones, hasta la descarga del certificado en PDF y el panel SuperAdmin). Las tablas completas de requerimientos, permisos por rol (RBAC) y casos de uso están en el Anexo E."),

    ("H3", "5.4.2. Arquitectura tecnológica"),
    ("P", "Atendiendo a la necesidad de construir un Producto Mínimo Viable (MVP) ágil, escalable y mantenible por un equipo reducido, se seleccionó un enfoque de Monolito Modular desacoplado (Sommerville, 2016; Parnas, 1972). El backend fue implementado en Python 3.12 con Flask, organizado en seis Blueprints bajo el prefijo /api con 21 endpoints REST protegidos con tokens JWT. El frontend se construyó en Angular 17 consumiendo la API de forma asíncrona e integrando el mapa sobre Leaflet y OpenStreetMap. Los diagramas de arquitectura y secuencia se encuentran en el Anexo F."),

    ("H3", "5.4.3. Diseño de la base de datos"),
    ("P", "El diseño relacional se estructuró bajo los criterios de normalización hasta la Quinta Forma Normal (5FN), previniendo redundancias y anomalías en la actualización de datos. El esquema implementado en SQLAlchemy ORM comprende 34 tablas distribuidas en cinco dominios (localización en los 18 municipios de la Sabana, catálogos institucionales y 9 ODS, seguridad RBAC y auditoría de Ley 1581, perfil jurídico de las OSAL, y tablas transaccionales de campañas, necesidades, donaciones, certificados y voluntariado). En la Figura 7 se muestra el diagrama del Modelo Entidad-Relación (MER) elaborado en MySQL Workbench, y en el Anexo F se detalla el diccionario de las 34 tablas."),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\MER.png",
        "caption": "Figura 7. Diagrama del Modelo Entidad-Relación (MER) normalizado de la base de datos Conexión Solidaria",
        "note": "Nota. Modelo relacional estructurado en MySQL Workbench e implementado en SQLAlchemy ORM (Anexo F)."
    }),

    ("H3", "5.4.4. Desarrollo de módulos y funcionalidades"),
    ("P", "Siguiendo el criterio de descomposición modular de Parnas (1972), el código fuente del MVP se organizó en seis módulos funcionales cohesivos cuyos fragmentos principales se documentan en el Anexo G:"),
    ("UL", [
        "1. Módulo de Autenticación, Seguridad y Habeas Data (backend/app/blueprints/auth.py y frontend/src/app/core/services/auth.service.ts): Gestiona el registro de usuarios, el cifrado de credenciales con PBKDF2-SHA256, la emisión de tokens JWT con claims de rol y la validación obligatoria de aceptación de la Ley 1581 de 2012.",
        "2. Módulo de Gestión y Verificación Institucional de OSAL (backend/app/blueprints/osal.py y frontend/src/app/features/osal/): Implementa el asistente de registro en 3 pasos, la georreferenciación municipal en la Sabana, la alineación con los ODS y el flujo de aprobación documental.",
        "3. Módulo de Mapa Interactivo, Causas y Necesidades (backend/app/blueprints/necesidades.py y frontend/src/app/features/mapa/): Provee el visor cartográfico sobre Leaflet y OpenStreetMap con marcadores dinámicos de las fundaciones rurales, filtros combinados por municipio, categoría y ODS, y barras de progreso de cada necesidad.",
        "4. Módulo de Convocatorias y Postulaciones de Voluntariado (backend/app/blueprints/voluntariado.py y frontend/src/app/features/voluntariado/): Administra el ciclo de vida de las vacantes de voluntariado, las habilidades requeridas, la inscripción de ciudadanos y el descuento automático de cupos disponibles.",
        "5. Módulo Transaccional de Donaciones y Certificación PDF (backend/app/blueprints/donaciones.py): Ejecuta el protocolo PGVTT para el registro de donaciones en dinero o especie, la confirmación por parte de la OSAL, el recálculo porcentual de metas y la generación dinámica del certificado tributario en PDF con código hash SHA-256 mediante ReportLab.",
        "6. Módulo de Tablero de Impacto y Gobernanza SuperAdmin (backend/app/blueprints/dashboard.py y frontend/src/app/features/dashboard/): Calcula indicadores agregados de cobertura de necesidades, impacto desagregado por cada uno de los 9 ODS, bitácora de transparencia y administración de parámetros del sistema."
    ]),

    ("H3", "5.4.5. Interfaces de usuario"),
    ("P", "Las interfaces gráficas del MVP fueron construidas en Angular 17 aplicando diseño responsivo y pautas de accesibilidad WCAG 2.2 (W3C, 2023). A continuación, en las Figuras 8, 9, 10 y 11 se presentan cuatro vistas principales capturadas directamente del sistema en ejecución (la galería completa de doce capturas de pantalla de todos los módulos y roles se presenta en el Anexo H):"),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h01_mapa.png",
        "caption": "Figura 8. Interfaz principal del Mapa Interactivo y Directorio Georreferenciado de OSAL en la Sabana de Cundinamarca",
        "note": "Nota. Captura real del MVP en ejecución mostrando las fundaciones caracterizadas en Cogua, Cajicá, Zipaquirá, Chía y Tabio (Anexo H)."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h02_catalogo_filtrado.png",
        "caption": "Figura 9. Interfaz del Catálogo de Necesidades Activas Filtradas por Municipio, Categoría y ODS",
        "note": "Nota. Captura real del MVP mostrando el avance porcentual de metas y la prioridad de las causas rurales (Anexo H)."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h08_postulacion_voluntariado.png",
        "caption": "Figura 10. Interfaz de Convocatorias y Postulación a Voluntariado por Habilidades, Horarios y Cupos Disponibles",
        "note": "Nota. Captura real del MVP mostrando la oferta y postulación de voluntariado rural en las fundaciones de la Sabana (Anexo H)."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h11_dashboard_ods.png",
        "caption": "Figura 11. Interfaz del Tablero de Indicadores de Impacto Social, Cobertura de Necesidades y Aporte por ODS",
        "note": "Nota. Captura real del MVP con métricas en tiempo real y desglose por Objetivos de Desarrollo Sostenible (Anexo H)."
    }),

    ("H3", "5.4.6. Herramientas, entorno de desarrollo y despliegue en la nube (Render)"),
    ("P", "El entorno de trabajo se montó sobre Windows 11 Pro utilizando Visual Studio Code como editor principal, Python 3.12 en entorno virtual aislado (.venv), Node.js 20 LTS, Angular CLI 17 y MySQL Workbench 8.0 para el modelado relacional. El control de versiones se llevó en Git 2.45 sobre GitHub, la automatización de pruebas y capturas se ejecutó con Pytest y Playwright, y el despliegue productivo en la nube se realizó en la plataforma PaaS Render con certificado HTTPS activo en la dirección pública https://conexion-solidaria.onrender.com/login."),

    ("H3", "5.4.7. Evidencias del desarrollo del software y portafolio digital"),
    ("P", "Las evidencias técnicas que respaldan el desarrollo del software y el proceso investigativo están disponibles tanto en línea —a través del despliegue productivo del MVP en https://conexion-solidaria.onrender.com/login y del Portafolio Digital de CTeI de los autores en https://sites.google.com/view/angelica-olier-portafolio-ctei/página-principal— como en cuatro anexos técnicos al final de este informe: el Anexo E contiene la matriz de trazabilidad, la matriz RBAC y las especificaciones de casos de uso; el Anexo F reúne los diagramas de arquitectura, casos de uso, secuencia, modelo entidad-relación y el diccionario de las 34 tablas en 5FN; el Anexo G incluye fragmentos comentados del código fuente tanto en backend como en frontend; y el Anexo H presenta las doce capturas de pantalla de las interfaces del MVP en ejecución junto con el certificado tributario PDF generado por el sistema."),

    ("H3", "5.4.8. Estado actual y limitaciones del MVP"),
    ("P", "En su versión actual (MVP 1.0 desplegado en https://conexion-solidaria.onrender.com/login), la plataforma tiene todos sus flujos principales funcionando de punta a punta: registro con validación de la Ley 1581 de 2012, mapa interactivo de la Sabana, publicación de necesidades, postulación a voluntariado, reporte y confirmación de donaciones, descarga de certificados PDF con hash SHA-256 y tablero de impacto por ODS. Como limitación propia de un prototipo académico antes de constituir formalmente la personería jurídica, la conciliación de aportes en dinero se realiza subiendo el comprobante y confirmándolo desde el panel de la fundación, dejando la conexión con pasarelas bancarias pagas como PSE o Wompi para la segunda fase del proyecto."),

    ("H2", "5.5. Plan de pruebas y validación"),
    ("P", "En la Fase de Transición de RUP se ejecutó el plan de aseguramiento de calidad (QA) para comprobar el funcionamiento de los módulos construidos, su rapidez en condiciones de baja señal y su correspondencia con las necesidades reales de las fundaciones."),

    ("H3", "5.5.1. Estrategia de pruebas"),
    ("P", "La validación combinó tres tipos de pruebas sobre el software (Pressman & Maxim, 2020; Sommerville, 2016). Primero, pruebas funcionales de caja negra e integración API sobre quince casos de prueba (CP-01 a CP-15). Segundo, mediciones de latencia HTTP y peso de paquetes JSON para verificar su desempeño en redes móviles rurales 3G y 4G (RNF01). Tercero, pruebas de recorrido de usuario cargando los datos reales de las cinco organizaciones caracterizadas en la Sabana (FARASAN, FUNHUELLAS, ASOMAYOR, FUNDAULA y CORPOJUAICA)."),

    ("H3", "5.5.2. Casos de prueba"),
    ("P", "La Tabla 16 resume los quince casos de prueba ejecutados sobre el MVP (el detalle completo con precondiciones, pasos y capturas se encuentra en el Anexo I)."),
    ("TABLE", {
        "title": "Tabla 16. Matriz resumen de los 15 casos de prueba funcional y no funcional ejecutados sobre el MVP",
        "headers": ["ID Caso", "Requerimiento / Caso de Uso", "Escenario Evaluado", "Resultado Esperado", "Resultado Obtenido y Estado"],
        "rows": [
            ["CP-01", "RF01 / CU01", "Registro de nueva OSAL sin aceptar cláusula Ley 1581 de 2012.", "Bloqueo de envío en paso 3 y código HTTP 400 si se omite consentimiento.", "HTTP 400 / Botón deshabilitado hasta marcar aceptación. APROBADO."],
            ["CP-02", "RF01 / CU01", "Registro completo de OSAL rural en 3 pasos con aceptación Ley 1581.", "Creación de registro en fundaciones_osal con fecha_aceptacion_datos y estado Pendiente.", "HTTP 201 Created; registro persistido en BD 5FN. APROBADO."],
            ["CP-03", "RF02 / CU02", "Autenticación de usuario con credenciales válidas e inválidas.", "Emisión de token JWT válido ante clave correcta y rechazo HTTP 401 ante clave errónea.", "Token JWT firmado emitido en 42 ms; HTTP 401 en clave errada. APROBADO."],
            ["CP-04", "RF02 / RNF05", "Control de acceso basado en roles (RBAC) a rutas administrativas.", "Restricción de acceso a /superadmin para roles Visitante, Donante o Voluntario.", "Guard de Angular e interceptor JWT bloquean acceso no autorizado. APROBADO."],
            ["CP-05", "RF03 / CU03", "Carga del mapa interactivo y filtrado de OSAL por municipio y ODS.", "Retorno exclusivo de fundaciones verificadas con coordenadas en Sabana y ODS filtrados.", "HTTP 200 OK en 18,4 ms; 5 OSAL renderizadas en mapa Leaflet. APROBADO."],
            ["CP-06", "RF04 / CU04-05", "Creación de campaña y necesidad de insumos por Administrador OSAL.", "Almacenamiento de necesidad con unidad de medida, meta cuantitativa y prioridad.", "HTTP 201 Created; necesidad visible inmediatamente en catálogo. APROBADO."],
            ["CP-07", "RF07 / CU06", "Registro de donación por usuario Donante hacia una necesidad activa.", "Creación de transacción en estado Pendiente con código único de trazabilidad.", "HTTP 201 Created; código DON-2026 generado sin alterar meta aún. APROBADO."],
            ["CP-08", "RF08 / CU06", "Confirmación de recepción de donación por parte de la OSAL (PGVTT).", "Cambio de estado a Confirmada, suma automática al monto alcanzado y bitácora.", "HTTP 200 OK; barra de progreso actualizada al 69,3 % de cobertura. APROBADO."],
            ["CP-09", "RF09 / CU07", "Generación y descarga de Certificado Tributario de Donación en PDF.", "Emisión de archivo PDF válido con datos de OSAL, donante, valor y hash SHA-256.", "HTTP 200 application/pdf (2,6 KB) descargado y verificado. APROBADO."],
            ["CP-10", "RF05 / CU08", "Publicación de convocatoria de voluntariado con cupos limitados.", "Creación de convocatoria activa asociada a municipio, fecha y habilidades.", "HTTP 201 Created; convocatoria listada en módulo de voluntariado. APROBADO."],
            ["CP-11", "RF06 / CU09", "Postulación de voluntario y control de descuento de cupos.", "Registro de postulación, validación de no duplicidad y actualización de cupos.", "HTTP 201 Created; cupo descontado correctamente al aprobarse. APROBADO."],
            ["CP-12", "RF10 / CU10", "Cálculo de indicadores del Dashboard e impacto por los 9 ODS.", "Retorno de KPIs exactos: OSAL verificadas, tasa de cobertura (69,3 %) y matriz ODS.", "HTTP 200 OK en 22,1 ms; 9 ODS tabulados con métricas reales. APROBADO."],
            ["CP-13", "RF12 / CU10", "Aprobación documental de OSAL desde el panel SuperAdmin.", "Cambio de estado de validación de la fundación a Verificada y aparición pública.", "HTTP 200 OK; estado actualizado y registrado en auditoría. APROBADO."],
            ["CP-14", "RNF01", "Prueba de estrés de latencia y tamaño de payload para red rural 3G.", "Latencia media < 200 ms y tamaño de respuesta JSON < 15 KB en todos los endpoints.", "Latencia media: 19,8 ms (máx. 56,4 ms); payload máx.: 7,42 KB. APROBADO."],
            ["CP-15", "RNF04", "Verificación de integridad referencial en las 34 tablas en 5FN.", "Creación y consulta sin anomalías de actualización ni registros huérfanos.", "34 tablas creadas y pobladas con integridad referencial 100 %. APROBADO."]
        ],
        "note": "Nota. El 100 % de los 15 casos de prueba (CP-01 a CP-15) arrojó resultado satisfactorio (Aprobado). Detalle extendido en el Anexo I."
    }),

    ("H3", "5.5.3. Pruebas funcionales"),
    ("P", "Las trece pruebas funcionales (CP-01 a CP-13) pasaron sin errores lógicos ni fallos de guardado. En los casos CP-07, CP-08 y CP-09 se puso especial cuidado en comprobar que una donación recién reportada no sume al indicador de la fundación mientras siga en estado Pendiente; solo cuando el administrador de la OSAL confirma que recibió el dinero o los insumos, el porcentaje de cobertura sube y se habilita la descarga del certificado PDF."),

    ("H3", "5.5.4. Pruebas de usabilidad"),
    ("P", "En las pruebas de usabilidad (RNF02) se verificó un contraste visual superior a 4.5:1 bajo la guía WCAG 2.2 (W3C, 2023) y la correcta visualización tanto en pantallas de celular (360x800 px) como de computador (1440x900 px). El registro completo de una fundación en tres pasos tomó un tiempo promedio de 4 minutos y 20 segundos."),

    ("H3", "5.5.5. Validación con usuarios y organizaciones"),
    ("P", "La prueba de contexto se realizó cargando y operando en el sistema los perfiles, campañas de insumos (mercados no perecederos, concentrado canino, kits escolares, pañales geriátricos y plántulas nativas) y jornadas de voluntariado de cinco organizaciones reales de la Sabana: FARASAN en Cogua, FUNHUELLAS en Cajicá, ASOMAYOR en Zipaquirá, FUNDAULA en Chía y CORPOJUAICA en Tabio. El modelo en 5FN permitió registrar las particularidades operativas de todas ellas sin requerir campos improvisados."),

    ("H3", "5.5.6. Resultados y ajustes realizados"),
    ("P", "A partir de las pruebas y de las revisiones académicas se aplicaron tres ajustes puntuales al MVP antes de su entrega final: (1) se añadió la validación obligatoria de la cláusula de protección de datos (Ley 1581 de 2012) con fecha y hora en la base de datos y en el Paso 3 del registro; (2) se completó la base de datos semilla con los nueve Objetivos de Desarrollo Sostenible vinculados al proyecto (ODS 1, 2, 3, 4, 9, 10, 11, 15 y 17); y (3) se incorporó en el dashboard la tabla desagregada por ODS y el porcentaje global de cobertura de necesidades."),

    ("H3", "5.5.7. Limitaciones de la validación"),
    ("P", "Cabe precisar que las pruebas realizadas corresponden a validación funcional automatizada, mediciones técnicas de respuesta en servidor y pruebas piloto con los datos parametrizados de las cinco fundaciones caracterizadas. La medición del aumento en el recaudo bancario anual de las fundaciones es un indicador longitudinal que solo podrá evaluarse tras el primer año de operación pública del portal."),

    ("H2", "5.6. Plan financiero"),
    ("P", "Siguiendo el sexto objetivo específico y la Guía ADOr006_V10 (Universidad de Cundinamarca, 2024), el plan financiero detalla la inversión inicial, los costos de desarrollo y mantenimiento, el presupuesto a tres años, el flujo de caja y el análisis de sensibilidad. El objetivo de estos cálculos es demostrar con cifras reales que la plataforma puede mantenerse activa sin cobrarle un solo peso a las fundaciones rurales."),

    ("H3", "5.6.1. Inversión inicial"),
    ("P", "La inversión inicial en el Año 0 asciende a un valor total de $18.450.000 COP. De ese monto, $16.200.000 COP corresponden al aporte intelectual en especie de los dos cofundadores (desarrollo del software y uso de equipos propios), por lo que el requerimiento de dinero en efectivo para arrancar es de solo $2.250.000 COP, destinados a la constitución legal como ESAL ante Cámara de Comercio, compra del dominio .org.co, servidor cloud inicial y capital de trabajo (Tabla 17)."),

    ("H3", "5.6.2. Costos de desarrollo"),
    ("P", "Para valorar contablemente el software construido se tomaron como base 640 horas de ingeniería (320 horas por cada autor durante las 16 semanas del proyecto, sumando análisis RUP, base de datos en 5FN, backend en Flask, frontend en Angular y pruebas QA). A una tarifa conservadora de ingeniero junior de $22.500 COP por hora, el desarrollo equivale a $14.400.000 COP, más $1.800.000 COP por depreciación de dos computadores portátiles y conectividad durante los cuatro meses. Esos $16.200.000 COP constituyen el patrimonio tecnológico inicial aportado por los fundadores."),

    ("H3", "5.6.3. Costos operativos y de mantenimiento"),
    ("P", "Los costos operativos anuales (OPEX) para sostener la plataforma en línea, verificar documentos y acompañar a las fundaciones suman $14.100.000 COP en el Año 1 ($1.175.000 COP al mes en promedio). Se dividen en cuatro rubros: (1) Infraestructura Cloud, Base de Datos, Almacenamiento, Dominio y SSL: $2.580.000 COP/año ($215.000 COP/mes); (2) Soporte Técnico, Verificación OSAL y Mantenimiento: $6.600.000 COP/año; (3) Difusión Digital y Visitas Veredales: $1.800.000 COP/año; y (4) Contabilidad RTE, Renovación de Matrícula ESAL y Papelería: $3.120.000 COP/año."),

    ("H3", "5.6.4. Proyección de ingresos y fuentes de financiación"),
    ("P", "Para cubrir el 100 % de estos gastos sin cobrar comisión a las fundaciones, los ingresos de la Fundación Conexión Solidaria se proyectan a tres años desde las cuatro fuentes definidas en el Canvas: (1) Patrocinios Corporativos RSE de empresas de la Sabana (5 empresas aliadas en el Año 1 por $10.500.000 COP, 10 en el Año 2 por $22.000.000 COP y 16 en el Año 3 por $36.000.000 COP); (2) Subvenciones y Convocatorias TIC/Sociales ($4.500.000 COP en Año 1, $8.000.000 COP en Año 2 y $12.000.000 COP en Año 3); (3) Convenios de Reportes de Impacto ($1.500.000 COP en Año 1, $3.600.000 COP en Año 2 y $6.000.000 COP en Año 3); y (4) Aportes Voluntarios de Sostenimiento ($1.200.000 COP en Año 1, $2.400.000 COP en Año 2 y $4.000.000 COP en Año 3)."),

    ("H3", "5.6.5. Presupuesto de funcionamiento"),
    ("P", "La Tabla 17 consolida el presupuesto de ingresos y egresos para los Años 1, 2 y 3."),
    ("TABLE", {
        "title": "Tabla 17. Presupuesto consolidado de ingresos institucionales, costos operativos (OPEX) y flujo de caja a 3 años (en pesos colombianos COP)",
        "headers": ["Concepto Financiero / Rubro Presupuestal", "Año 0 (Inversión Inicial)", "Año 1 (25 OSAL Verificadas)", "Año 2 (60 OSAL Verificadas)", "Año 3 (120 OSAL Verificadas)"],
        "rows": [
            ["A. INGRESOS OPERATIVOS INSTITUCIONALES (Tarifa a OSAL = $0)", "$0", "$17.700.000", "$36.000.000", "$58.000.000"],
            ["1. Patrocinios Corporativos RSE (Planes Bronce, Plata y Oro)", "$0", "$10.500.000", "$22.000.000", "$36.000.000"],
            ["2. Subvenciones y Convocatorias de Innovación Social / TIC", "$0", "$4.500.000", "$8.000.000", "$12.000.000"],
            ["3. Convenios de Analítica y Reportes de Impacto Territorial", "$0", "$1.500.000", "$3.600.000", "$6.000.000"],
            ["4. Aportes Voluntarios al Fondo de Sostenimiento Tecnológico", "$0", "$1.200.000", "$2.400.000", "$4.000.000"],
            ["B. INVERSIÓN Y EGRESOS OPERATIVOS (CAPEX / OPEX)", "$2.250.000*", "$14.100.000", "$27.400.000", "$43.200.000"],
            ["1. Infraestructura Cloud (Servidor, BD 5FN, Storage, Dominio, SSL)", "$450.000", "$2.580.000", "$4.200.000", "$6.800.000"],
            ["2. Ingeniería, Soporte Técnico, QA y Verificación Documental OSAL", "$0*", "$6.600.000", "$14.400.000", "$24.000.000"],
            ["3. Plan de Marketing, Difusión Digital y Acompañamiento Veredal", "$600.000", "$1.800.000", "$4.200.000", "$6.400.000"],
            ["4. Constitución Legal ESAL, Contabilidad RTE y Gastos Administrativos", "$1.200.000", "$3.120.000", "$4.600.000", "$6.000.000"],
            ["C. EXCEDENTE OPERATIVO NETO DEL PERIODO (A - B)", "-$2.250.000", "+$3.600.000", "+$8.600.000", "+$14.800.000"],
            ["D. FLUJO DE CAJA ACUMULADO (Reserva de Sostenibilidad ESAL)", "-$2.250.000", "+$1.350.000", "+$9.950.000", "+$24.750.000"]
        ],
        "note": "Nota. *En el Año 0, además del capital líquido de arranque ($2.250.000 COP), el proyecto cuenta con el aporte intelectual en especie del desarrollo del MVP valorizado en $16.200.000 COP. En calidad de ESAL (RTE), el 100 % del excedente neto se reinvierte en la reserva de estabilidad tecnológica y expansión regional."
    }),

    ("H3", "5.6.6. Flujo de caja proyectado"),
    ("P", "El flujo de caja de la Tabla 17 muestra que el capital en efectivo inicial ($2.250.000 COP) se recupera dentro del primer año de operación, cerrando el Año 1 con un excedente neto de $3.600.000 COP y un saldo acumulado en caja de $1.350.000 COP. En los Años 2 y 3, la entrada de nuevas empresas patrocinadoras permite ampliar la capacidad de servidores y el equipo de soporte para atender a 60 y 120 fundaciones, acumulando al final del tercer año una reserva institucional de $24.750.000 COP."),
    ("P", "Descontando los flujos de efectivo con una tasa social (COK) del 12 % efectivo anual, el proyecto arroja un Valor Presente Neto (VPN) positivo de $17.420.000 COP sobre la inversión líquida inicial y una relación Beneficio/Costo de 1,32. Si además se contabiliza el ahorro en licencias y páginas web que reciben gratuitamente las fundaciones beneficiarias, el VPN social supera los $85.000.000 COP."),

    ("H3", "5.6.7. Escenarios financieros"),
    ("P", "Para medir qué pasa si al inicio se consiguen menos patrocinios de los previstos, la Tabla 18 evalúa tres escenarios en el Año 1: Pesimista (Mínimo Vital Cloud), Base Esperado y Optimista."),
    ("TABLE", {
        "title": "Tabla 18. Evaluación de escenarios financieros del Año 1 y estrategia de ajuste de costos",
        "headers": ["Indicador / Rubro (Año 1)", "Escenario Pesimista (Mínimo Vital Cloud)", "Escenario Base (Proyectado Realista)", "Escenario Optimista (Alta Adopción RSE)"],
        "rows": [
            ["Supuesto de captación de fondos", "Solo 2 patrocinios RSE Bronce + aportes mínimos (sin subvenciones).", "5 patrocinios RSE + 1 subvención local + convenios base.", "8 patrocinios RSE (incluyendo Oro) + 2 subvenciones regionales."],
            ["Ingresos Operativos Anuales (COP)", "$5.400.000", "$17.700.000", "$28.500.000"],
            ["Costos de Infraestructura Cloud y Dominio", "$2.580.000", "$2.580.000", "$3.200.000"],
            ["Costos de Soporte, Legal y Difusión (ajustables)", "$2.400.000 (operación 100 % voluntaria fundadores + practicantes).", "$11.520.000 (operación base completa).", "$16.800.000 (ampliación de cobertura veredal)."],
            ["Total Egresos Anuales (COP)", "$4.980.000", "$14.100.000", "$20.000.000"],
            ["Resultado Neto del Ejercicio (COP)", "+$420.000 (Sostenible)", "+$3.600.000 (Sostenible con reserva)", "+$8.500.000 (Expansión acelerada)"],
            ["Impacto sobre la gratuidad para las OSAL", "Se mantiene 100 % gratuito (0 % cobro a OSAL).", "Se mantiene 100 % gratuito (0 % cobro a OSAL).", "Se mantiene 100 % gratuito (0 % cobro a OSAL)."]
        ],
        "note": "Nota. Incluso en el escenario pesimista (ingresos de solo $450.000 COP/mes), la arquitectura ligera LBRSA permite cubrir el 100 % del hosting cloud ($215.000 COP/mes) y los gastos legales mínimos sin cobrar a las fundaciones."
    }),

    ("H3", "5.6.8. Análisis de sostenibilidad económica"),
    ("P", "[[EDITAR]]En el escenario base, el punto de equilibrio se alcanza con un ingreso mensual promedio de $1.175.000 COP, lo que equivale a vincular apenas cuatro o cinco empresas patrocinadoras dentro de un corredor industrial que supera las 650 compañías. Más aún, en caso de una contingencia donde el soporte sea asumido directamente por nosotros como cofundadores junto con practicantes universitarios, el costo mínimo vital para mantener los servidores y la base de datos encendidos en la nube es de tan solo $215.000 COP al mes ($2.580.000 COP al año), reduciendo al mínimo el riesgo de que la plataforma tenga que apagarse por falta de recursos.[[/EDITAR]]"),

    ("H2", "5.7. Plan de gestión de riesgos"),
    ("P", "Siguiendo el numeral 14 de la Guía ADOr006_V10 (Universidad de Cundinamarca, 2024), se identificaron y valoraron los principales riesgos del proyecto junto con sus acciones de prevención y mitigación."),

    ("H3", "5.7.1. Identificación de riesgos"),
    ("P", "Los riesgos se agruparon en cinco categorías: técnicos y de ciberseguridad, financieros, operativos, legales/regulatorios y de adopción comunitaria."),

    ("H3", "5.7.2. Riesgos técnicos"),
    ("P", "Incluyen la señal móvil intermitente en veredas apartadas (R-01), posibles intentos de acceso no autorizado o alteración de estados de donación (R-02) y caídas temporales del servicio cloud (R-03)."),

    ("H3", "5.7.3. Riesgos financieros"),
    ("P", "Se refieren a una captación de patrocinios RSE más lenta de lo previsto durante el primer semestre (R-04) o a subidas en el costo de servidores internacionales por variaciones del dólar (R-05)."),

    ("H3", "5.7.4. Riesgos operativos y legales"),
    ("P", "Abarcan el intento de registro de supuestas fundaciones sin personería jurídica vigente (R-06), reclamaciones sobre tratamiento de datos personales bajo la Ley 1581 de 2012 (R-07) y demoras de los líderes de las OSAL al confirmar en la plataforma las donaciones recibidas (R-08)."),

    ("H3", "5.7.5. Riesgos de adopción y participación"),
    ("P", "Comprenden la dificultad de algunos líderes comunitarios mayores para usar herramientas web (R-09) y la baja estacional de voluntarios universitarios en meses de vacaciones de mitad y fin de año (R-10)."),

    ("H3", "5.7.6. Estrategias de mitigación"),
    ("P", "La Tabla 19 presenta la Matriz de Gestión de Riesgos con la probabilidad, impacto, nivel de criticidad, responsable y plan de respuesta para cada uno de los diez riesgos."),
    ("TABLE", {
        "title": "Tabla 19. Matriz de identificación, valoración y mitigación de riesgos del proyecto Conexión Solidaria",
        "headers": ["ID", "Categoría", "Descripción del Riesgo", "Probabilidad", "Impacto", "Nivel", "Responsable", "Estrategia de Prevención y Mitigación"],
        "rows": [
            ["R-01", "Técnico / Producción", "Fallas de carga de la plataforma en veredas con señal móvil 3G inestable.", "Alta", "Medio", "Medio-Alto", "Director de Tecnología (CTO)", "Implementación de Arquitectura LBRSA con payloads JSON < 7,5 KB, latencia < 57 ms y diseño sin activos pesados."],
            ["R-02", "Técnico / Seguridad", "Acceso no autorizado o alteración de estados de donaciones y certificados.", "Baja", "Alto", "Medio", "Director de Tecnología (CTO)", "Autenticación JWT con expiración, RBAC estricto en servidor, contraseñas PBKDF2-SHA256 y hash criptográfico en PDF."],
            ["R-03", "Técnico / Operativo", "Caída del servidor cloud o corrupción de la base de datos relacional.", "Baja", "Alto", "Medio", "Director de Tecnología (CTO)", "Backups automáticos diarios de la BD 5FN, código en GitHub y arquitectura portable entre SQLite, MySQL y PostgreSQL."],
            ["R-04", "Financiero", "Captación de patrocinios RSE inferior a la meta proyectada en el semestre 1.", "Media", "Alto", "Alto", "Directora Ejecutiva", "Activación del presupuesto de Mínimo Vital Cloud ($215.000 COP/mes) y diversificación en 4 fuentes de ingreso."],
            ["R-05", "Financiero", "Incremento cambiario (USD/COP) en costos de servicios cloud.", "Media", "Bajo", "Bajo", "Director de Tecnología (CTO)", "Uso de niveles gratuitos/sociales para ONG (GitHub Education/Nonprofit, Cloudflare) y reserva financiera del 15 %."],
            ["R-06", "Legal / Operativo", "Solicitud de ingreso de una fundación no constituida o con fines fraudulentos.", "Media", "Crítico", "Alto", "Coordinación de Verificación OSAL", "Protocolo PGVTT: ninguna OSAL aparece en el mapa público sin validación previa de RUT, Cámara de Comercio y cédula."],
            ["R-07", "Legal / Regulatorio", "Reclamación por tratamiento de datos personales (Ley 1581 de 2012).", "Baja", "Alto", "Medio", "Directora Ejecutiva / CTO", "Captura obligatoria de checkbox expreso y fecha_aceptacion_datos en la BD antes de crear cualquier cuenta."],
            ["R-08", "Operativo", "Demora del líder de la OSAL en confirmar en el sistema una donación recibida.", "Media", "Medio", "Medio", "Coordinación de Verificación OSAL", "Alertas automáticas vía WhatsApp al representante de la OSAL y seguimiento semanal desde el equipo de soporte."],
            ["R-09", "Mercado / Adopción", "Baja adopción o abandono del sistema por líderes rurales con baja alfabetización digital.", "Media", "Alto", "Alto", "Directora Ejecutiva / Practicantes", "Interfaz simplificada en 3 pasos (WCAG 2.2), registro inicial asistido y acompañamiento por practicantes universitarios."],
            ["R-10", "Mercado / Participación", "Baja postulación de voluntarios durante recesos universitarios (junio/diciembre).", "Alta", "Medio", "Medio", "Directora Ejecutiva", "Activación de campañas de voluntariado familiar y corporativo RSE durante los meses de vacaciones estudiantiles."]
        ],
        "note": "Nota. Elaboración propia conforme a los lineamientos de gestión de riesgos de la Guía ADOr006_V10 (Universidad de Cundinamarca, 2024)."
    }),

    ("H2", "5.8. Plan de implementación y crecimiento"),
    ("P", "El plan de implementación organiza los pasos para poner en marcha la plataforma tras la aprobación del MVP, definiendo sus horizontes de expansión, su cronograma mes a mes y sus metas de seguimiento."),

    ("H3", "5.8.1. Fases de implementación"),
    ("P", "El crecimiento territorial se proyecta en tres horizontes anuales: (a) Horizonte 1 - Arranque Local (Año 1): Constitución legal de la Fundación Conexión Solidaria, salida a producción en servidor cloud y vinculación de las primeras 25 OSAL verificadas en el eje Chía, Cajicá, Zipaquirá, Cogua, Tabio, Tenjo y Sopó; (b) Horizonte 2 - Consolidación en Sabana Centro y Norte (Año 2): Ampliación a 60 OSAL verificadas cubriendo los 18 municipios del corredor (sumando Tocancipá, Gachancipá, Nemocón, Suesca, Sesquilé, Guatavita, Chocontá, Villapinzón, Machetá, Manta y Tibirita) e integración de botón de pagos PSE; y (c) Horizonte 3 - Expansión Departamental (Año 3): Llegar a 120 OSAL activas extendiendo el modelo hacia las provincias de Ubaté, Gualivá y Sumapaz."),

    ("H3", "5.8.2. Cronograma de actividades"),
    ("P", "La Tabla 20 detalla el cronograma operativo mes a mes para el primer año de funcionamiento (complementando el cronograma de ingeniería de 16 semanas ejecutado durante el desarrollo del MVP, disponible en el Anexo K)."),
    ("TABLE", {
        "title": "Tabla 20. Cronograma de implementación y plan de operación mes a mes durante el primer año",
        "headers": ["Actividad Estratégica / Operativa", "Meses 1-2", "Meses 3-4", "Meses 5-6", "Meses 7-8", "Meses 9-10", "Meses 11-12", "Meta Anual Verificable"],
        "rows": [
            ["1. Constitución legal ESAL, RUT (RTE) y despliegue cloud productivo", "Ejecución", "Cierre", "-", "-", "-", "-", "1 Fundación constituida y portal HTTPS activo."],
            ["2. Vinculación y verificación de OSAL rurales (Meta: 25 en Año 1)", "5 OSAL (Piloto)", "+4 OSAL (Acum: 9)", "+4 OSAL (Acum: 13)", "+4 OSAL (Acum: 17)", "+4 OSAL (Acum: 21)", "+4 OSAL (Acum: 25)", "25 OSAL rurales verificadas y activas en mapa."],
            ["3. Suscripción de convenios universitarios de voluntariado y práctica", "2 Convenios", "+1 Convenio", "Ejecución brigadas", "+1 Convenio", "Ejecución brigadas", "Evaluación anual", "4 convenios académicos activos en la Sabana."],
            ["4. Gestión comercial y cierre de patrocinios corporativos RSE", "Prospección", "2 Empresas RSE", "+1 Empresa RSE", "+1 Empresa RSE", "+1 Empresa RSE", "Renovación", "5 empresas patrocinadoras ($10,5 M COP)."],
            ["5. Jornadas de capacitación digital y acompañamiento veredal", "Jornada 1", "Jornada 2", "Jornada 3", "Jornada 4", "Jornada 5", "Jornada 6", "6 jornadas de alfabetización digital ejecutadas."],
            ["6. Auditoría de transparencia, backups y reporte de impacto ODS", "Mensual", "Mensual", "Reporte Semestral 1", "Mensual", "Mensual", "Reporte Anual RTE", "2 reportes públicos de impacto y 100 % SLA."]
        ],
        "note": "Nota. Elaboración propia conforme al requisito de plan de operación mes a mes del primer año de la Guía ADOr006_V10 (Universidad de Cundinamarca, 2024)."
    }),

    ("H3", "5.8.3. Recursos necesarios"),
    ("P", "La puesta en marcha durante el primer año se apoya en tres bloques de recursos ya definidos: (1) Tecnológicos: el código fuente completo del MVP, servidor cloud Python/WSGI, base de datos relacional y dominio .org.co con certificado SSL; (2) Humanos: los dos ingenieros cofundadores, dos practicantes universitarios y un contador público a tiempo parcial; y (3) Financieros: el capital semilla en efectivo de $2.250.000 COP y el presupuesto anual de ingresos de $17.700.000 COP detallado en la Sección 5.6."),

    ("H3", "5.8.4. Indicadores de seguimiento"),
    ("P", "El control del plan se llevará mediante seis indicadores trimestrales: (1) número de OSAL rurales verificadas activas en el mapa; (2) porcentaje de cobertura de las necesidades monetarias y en especie publicadas; (3) horas de voluntariado agendadas y cumplidas; (4) certificados de donación emitidos; (5) disponibilidad mensual del servidor (Uptime >= 99 % y latencia < 200 ms); y (6) porcentaje de costos operativos cubiertos mediante patrocinios RSE."),

    ("H3", "5.8.5. Estrategia de crecimiento y expansión"),
    ("P", "El crecimiento en los Años 2 y 3 se apalanca en la demostración práctica entre pares: a medida que las primeras 25 fundaciones de Chía, Cajicá, Zipaquirá, Cogua y Tabio reciban insumos y voluntarios a través del portal, su experiencia servirá de referencia directa para que las organizaciones de los trece municipios restantes se sumen a la red."),

    ("H2", "5.9. Evaluación de la viabilidad integral"),
    ("P", "Los resultados de los cinco capítulos permiten sintetizar la viabilidad del proyecto en seis ámbitos:"),

    ("H3", "5.9.1. Viabilidad técnica"),
    ("P", "Comprobada con la construcción y prueba del MVP en Angular 17 y Python/Flask sobre una base de datos de 34 tablas en 5FN, superando el 100 % de los quince casos de prueba con tiempos medios de respuesta de 19,8 ms y paquetes JSON menores a 7,5 KB aptos para zonas rurales."),

    ("H3", "5.9.2. Viabilidad operativa"),
    ("P", "Respaldada por ciclos operativos breves (entre 6 y 35 minutos), un registro guiado en tres pasos pensado para líderes con poca experiencia digital y el apoyo de practicantes universitarios en terreno."),

    ("H3", "5.9.3. Viabilidad comercial y de adopción"),
    ("P", "Sustentada en un mercado regional medible (SAM de 420 OSAL, más de 35.000 universitarios y 650 empresas en Sabana Centro y Norte) y en la gratuidad total para las fundaciones beneficiarias."),

    ("H3", "5.9.4. Viabilidad financiera"),
    ("P", "Demostrada con una estructura de costos baja (OPEX de $14.100.000 COP en el Año 1 y mínimo vital cloud de $2.580.000 COP/año), cuatro fuentes de ingreso institucional, recuperación del capital líquido en el primer año y VPN positivo."),

    ("H3", "5.9.5. Viabilidad jurídica e institucional"),
    ("P", "Asegurada por el cumplimiento de la Ley 1581 de 2012 (implementada directamente en el flujo de registro y en la base de datos), la Ley 527 de 1999, la Ley 720 de 2001, el Régimen Tributario Especial (RTE) y la separación contable entre las donaciones de las OSAL y el sostenimiento del portal."),

    ("H3", "5.9.6. Viabilidad social"),
    ("P", "Reflejada en el aporte directo al cierre de la brecha digital rural y a nueve Objetivos de Desarrollo Sostenible (ODS 1, 2, 3, 4, 9, 10, 11, 15 y 17), dando visibilidad a las organizaciones que atienden a las poblaciones más vulnerables de la Sabana."),

    ("H2", "5.10. Conclusiones del plan de emprendimiento"),
    ("P", "El Capítulo 5 demuestra que Conexión Solidaria no se queda en un ejercicio de programación para una materia, sino que cuenta con la estructura legal, operativa y financiera necesaria para sostenerse en el tiempo como una entidad sin ánimo de lucro real al servicio de las fundaciones rurales de Cundinamarca."),

    # =========================================================================
    # CIERRE: CONCLUSIONES, REFLEXIÓN PERSONAL, RECOMENDACIONES Y REFERENCIAS
    # =========================================================================
    ("H1", "CIERRE"),

    ("H2", "CONCLUSIONES GENERALES"),
    ("P", "A partir del trabajo de campo, del modelado de negocio y de la construcción del Producto Mínimo Viable (MVP) de Conexión Solidaria, se presentan las conclusiones generales del proyecto frente a cada uno de los seis objetivos específicos trazados:"),
    ("UL", [
        "1. Frente al Primer Objetivo Específico (Diagnóstico y estudio de mercado - Fase de Inicio RUP): [[EDITAR]]El diagnóstico confirmó con datos primarios y oficiales la brecha digital que frena a las pequeñas fundaciones de Cundinamarca. Al cruzar el DANE (2021, 2022) —36 % sin presupuesto para tecnología y 14 % sin personal técnico— con la encuesta diagnóstica aplicada a cuatro fundaciones de la región (Gotitas de Amor en Cajicá, Casa de los Abuelos en Machetá, Campamentos de Nueva Vida en Simijaca y Patitas Campesinas en La Calera), se comprobó que ninguna emplea un portal web propio como canal activo de difusión de necesidades, sus mayores obstáculos son la falta de recursos económicos (ranking 1,25), la baja visibilidad (2,25) y el reclutamiento de voluntarios (2,50), y el 100 % adoptaría la plataforma de inmediato. Asimismo, la encuesta de percepción e interés aplicada a n = 170 personas de la Sabana y su área de influencia reveló que el 64,7 % desconoce en detalle las fundaciones locales, el 58,2 % exige transparencia total en el uso de fondos, el 21,8 % claridad en las actividades a realizar y el 95,9 % (163 de 170) está dispuesto a utilizar Conexión Solidaria, sustentando los cinco actores, doce requerimientos funcionales y seis no funcionales del sistema.[[/EDITAR]]",
        "2. Frente al Segundo Objetivo Específico (Modelo estratégico y Lienzo Canvas): [[EDITAR]]La construcción de los nueve bloques del Modelo Canvas nos permitió resolver la tensión entre el propósito social y el sostenimiento económico. Mediante un esquema de subsidio cruzado donde las empresas con programas de RSE, las convocatorias de innovación y los convenios institucionales cubren la operación del servidor, logramos asegurar que el uso de la plataforma sea 100 % gratuito para las fundaciones rurales, manteniendo siempre separadas las cuentas operativas del portal y las donaciones que recibe cada organización.[[/EDITAR]]",
        "3. Frente al Tercer Objetivo Específico (Arquitectura de software, prototipos UI/UX y base de datos en 5FN - Fase de Elaboración RUP): [[EDITAR]]Se diseñó una arquitectura ligera de bajo consumo para entornos rurales bajo el patrón de Monolito Modular Desacoplado, acompañada de interfaces accesibles (WCAG 2.2) y una base de datos relacional normalizada hasta la Quinta Forma Normal (5FN) con 34 tablas. Esta estructura permitió conectar sin duplicidades los municipios, fundaciones, sedes veredales, los nueve ODS, campañas, necesidades en dinero o especie, donaciones, certificados y cupos de voluntariado.[[/EDITAR]]",
        "4. Frente al Cuarto Objetivo Específico (Desarrollo modular del MVP - Fase de Construcción RUP): [[EDITAR]]Se programó, integró y desplegó en la nube (https://conexion-solidaria.onrender.com/login) el MVP de Conexión Solidaria uniendo un backend API REST en Python 3.12 y Flask con un frontend en Angular 17 y mapas interactivos en Leaflet/OpenStreetMap. El sistema dejó operativos el registro con consentimiento expreso de la Ley 1581 de 2012, la autenticación JWT por roles, el mapa georreferenciado de la Sabana, el catálogo de necesidades, el agendamiento de voluntarios, la confirmación bilateral de donaciones, la descarga de certificados PDF con hash SHA-256 y el tablero de impacto por ODS.[[/EDITAR]]",
        "5. Frente al Quinto Objetivo Específico (Validación técnica, funcional y de propuesta de valor - Fase de Transición RUP): [[EDITAR]]Los quince casos de prueba (CP-01 a CP-15) ejecutados con los escenarios reales de cinco fundaciones de la región (FARASAN, FUNHUELLAS, ASOMAYOR, FUNDAULA y CORPOJUAICA) aprobaron en su totalidad. Las mediciones arrojaron tiempos medios de respuesta de 19,8 ms (nunca mayores a 57 ms) y respuestas JSON por debajo de 7,5 KB, demostrando que la plataforma carga rápido incluso con señal celular rural limitada.[[/EDITAR]]",
        "6. Frente al Sexto Objetivo Específico (Planes organizacional, operativo, de marketing y financiero): [[EDITAR]]La proyección financiera a tres años comprobó que la Fundación Conexión Solidaria es sostenible con una inversión en efectivo inicial de $2.250.000 COP (respaldada por $16.200.000 COP en trabajo de ingeniería aportado por los fundadores) y costos operativos de $14.100.000 COP en el primer año (con un mínimo vital en la nube de apenas $215.000 COP mensuales). El proyecto recupera su capital inicial en el primer año, arroja un Valor Presente Neto positivo y construye una reserva acumulada de $24.750.000 COP al tercer año sin cobrarle nada a las fundaciones beneficiarias.[[/EDITAR]]"
    ]),

    ("P_BOLD", "Narrativa Personal, Propósito Emprendedor y Reflexión del Plan de Vida (Acuerdo 012)"),
    ("P", "Conexión Solidaria nació de una experiencia profundamente humana. Como estudiantes de Ingeniería de Sistemas y Computación, siempre hemos creído que la tecnología tiene el poder de transformar realidades, pero fue hasta que nos enfrentamos de cerca con las dificultades que viven muchas organizaciones sociales en nuestra región, que entendimos cuál era nuestro verdadero propósito. Durante una actividad académica, conocimos varias fundaciones pequeñas en zonas rurales de Cundinamarca que trabajan incansablemente por comunidades vulnerables: adultos mayores, niños en condición de pobreza, animales abandonados, madres cabeza de hogar, jóvenes en rehabilitación. Nos impactó ver cómo estas organizaciones hacen tanto con tan poco, pero también cómo su labor se ve limitada por la falta de visibilidad, recursos y herramientas digitales. Muchas ni siquiera tienen presencia en internet o redes sociales activas, no porque no quieran, sino porque no saben cómo hacerlo o no tienen los medios."),
    ("P", "Esa realidad nos tocó profundamente. Nos dimos cuenta de que mientras el mundo avanza hacia la hiperconectividad, quienes más necesitan apoyo siguen desconectados. Y nos hicimos una pregunta sencilla pero poderosa: ¿y si usamos lo que sabemos para ayudar a quienes ayudan? Así nació Conexión Solidaria: una plataforma digital pensada desde la empatía, el compromiso social y la innovación tecnológica. No queríamos crear solo una página web, sino un puente real entre las organizaciones sociales y las personas que desean aportar su tiempo, sus recursos o sus conocimientos para cambiar vidas. Nuestro objetivo como emprendedores sociales no es solo desarrollar software, sino poner la tecnología al servicio de la solidaridad, democratizar el acceso a las oportunidades y demostrar que desde nuestras capacidades profesionales podemos construir un mundo más justo, más humano y conectado con las verdaderas necesidades de la gente."),

    ("H2", "RECOMENDACIONES Y TRABAJO FUTURO"),
    ("P", "Para dar continuidad al proyecto y abrir nuevas líneas de trabajo en la Universidad de Cundinamarca, se plantean cuatro recomendaciones puntuales:"),
    ("UL", [
        "1. Integración de pasarela de pagos electrónicos y billeteras digitales (Fase 2 del MVP): Una vez constituida la personería jurídica de la Fundación Conexión Solidaria y abiertas las cuentas institucionales, se recomienda integrar pasarelas de recaudo con dispersión directa (PSE, Nequi y Daviplata) para que los aportes en dinero entren de inmediato a la cuenta de cada fundación y se confirmen automáticamente mediante webhooks.",
        "2. Sincronización desconectada (Offline-First PWA): Para las veredas más alejadas de municipios como Machetá, Manta, Tibirita o Guatavita donde la señal móvil se corta por horas, conviene agregar Service Workers e IndexedDB en Angular para guardar temporalmente registros de insumos o asistencias de voluntarios en el teléfono y sincronizarlos apenas vuelva la conexión.",
        "3. Alianza permanente con Proyección Social y Semilleros de la Universidad de Cundinamarca: Se sugiere formalizar un acuerdo con la Facultad de Ingeniería en la Extensión Chía para que estudiantes de semestres intermedios realicen sus horas de práctica social acompañando en terreno a nuevas fundaciones rurales en el uso del portal.",
        "4. Continuidad del observatorio regional a partir de las encuestas aplicadas (Anexo B) y medición anual de impacto: Partiendo de la línea base ya consolidada con las 170 respuestas ciudadanas y las 4 fundaciones diagnosticadas, durante el primer año de operación pública se recomienda mantener habilitados los formularios en la plataforma para construir un observatorio regional continuo sobre donaciones, voluntariado y digitalización del tercer sector en Cundinamarca."
    ]),

    ("H2", "REFERENCIAS BIBLIOGRÁFICAS"),
    ("REF", [
        "Acevedo de la Ossa, J. E. (2023). Guía práctica de comunicación para asociaciones sin ánimo de lucro en Antioquia [Trabajo de grado de maestría, Universidad EAFIT]. Repositorio Institucional Universidad EAFIT.",
        "Aguilera Castro, A., & Riascos Erazo, S. C. (2009). Direccionamiento estratégico apoyado en las TIC. Estudios Gerenciales, 25(111), 127-143. http://www.scielo.org.co/scielo.php?script=sci_arttext&pid=S0123-59232009000200007",
        "Aliaga Bernal, J. (2009). La información financiera de las entidades sin ánimo de lucro. Una aproximación internacional a su marco conceptual. Contaduría Universidad de Antioquia, (55), 149-164.",
        "Asociación de Fundaciones Familiares y Empresariales [AFE]. (2018). Las fundaciones en Colombia: Características, tendencias y desafíos. AFE Colombia.",
        "Banco Interamericano de Desarrollo [BID]. (2020). La transformación digital de las organizaciones de la sociedad civil en América Latina. BID.",
        "Bedoya Dorado, C. (2015). Gestión del conocimiento en el tercer sector: de la competitividad a la eficiencia organizacional. Entramado, 11(2), 94-111. https://www.redalyc.org/pdf/2654/265443638007.pdf",
        "Caldeira, M. D. (2015). Liderazgo innovador para emprendimientos sociales en organizaciones sin fines de lucro. CICAG: Revista Electrónica Arbitrada del Centro de Investigación de Ciencias Administrativas y Gerenciales, 13(1), 191-207.",
        "Cámara de Comercio de Bogotá [CCB]. (2023). Guía práctica de las Entidades Sin Ánimo de Lucro (ESAL): Constitución, registro y vigilancia. Cámara de Comercio de Bogotá.",
        "Castillo, E., Sosa Zitto, R., Rapallini, U., Blanc, R., & Lepratte, L. (2013). TICs para una educación inclusiva. En Libro de Actas del XIX Congreso Argentino de Ciencias de la Computación (CACIC 2013) (pp. 1-9). Universidad Autónoma de Entre Ríos, Facultad de Ciencia y Tecnología.",
        "Chacón-Penagos, Á. M., Ordóñez-Córdoba, J. A., & Anichiarico-González, A. M. (2017). Hacia el reconocimiento de la inclusión digital como un derecho fundamental en Colombia. Vniversitas, 66(134), 139-168. https://doi.org/10.11144/Javeriana.vj134.hrid",
        "Congreso de la República de Colombia. (1950). Decreto Ley 2663 de 1950. Código Sustantivo del Trabajo. Diario Oficial No. 27.407.",
        "Congreso de la República de Colombia. (1989). Decreto 624 de 1989. Por el cual se expide el Estatuto Tributario de los Impuestos Administrados por la Dirección General de Impuestos Nacionales. Diario Oficial No. 38.756.",
        "Congreso de la República de Colombia. (1999). Ley 527 de 1999. Por medio de la cual se define y reglamenta el acceso y uso de los mensajes de datos, del comercio electrónico y de las firmas digitales. Diario Oficial No. 43.673.",
        "Congreso de la República de Colombia. (2001). Ley 720 de 2001. Por medio de la cual se reconoce, promueve y regula la acción voluntaria de los ciudadanos colombianos. Diario Oficial No. 44.661.",
        "Congreso de la República de Colombia. (2012). Ley Estatutaria 1581 de 2012. Por la cual se dictan disposiciones generales para la protección de datos personales. Diario Oficial No. 48.587.",
        "Congreso de la República de Colombia. (2013). Ley 1672 de 2013. Por la cual se establecen los lineamientos para la adopción de una política pública de gestión integral de residuos de aparatos eléctricos y electrónicos (RAEE). Diario Oficial No. 48.856.",
        "Congreso de la República de Colombia. (2016). Ley 1819 de 2016. Por medio de la cual se adopta una reforma tributaria estructural y se fortalecen los mecanismos para la lucha contra la evasión y la elusión fiscal (Régimen Tributario Especial ESAL). Diario Oficial No. 50.101.",
        "Contreras Duarte, A. M., Henríquez, S., & Gutiérrez Campos, L. (2022). La intervención social y las TIC en tiempos de crisis: una aproximación desde los discursos de trabajadores sociales. Rumbos TS, 17(27), 47-68.",
        "Departamento Administrativo Nacional de Estadística [DANE]. (2021). Encuesta de Desarrollo e Innovación Tecnológica y de Investigación y Desarrollo (I+D) 2020-2021: Boletín técnico total nacional. DANE.",
        "Departamento Administrativo Nacional de Estadística [DANE]. (2022). Encuesta Nacional de Calidad de Vida (ECV) 2021: Indicadores de tenencia y uso de Tecnologías de la Información y la Comunicación en hogares rurales y urbanos. DANE.",
        "Departamento Nacional de Planeación [DNP]. (2018). Documento CONPES 3918: Estrategia para la implementación de los Objetivos de Desarrollo Sostenible (ODS) en Colombia. Consejo Nacional de Política Económica y Social.",
        "Escobar Cazal, E. A., & Escobar Reyes, G. (2017). Diagnóstico y capacitación a entidades sin ánimo de lucro. Provincia del Sumapaz, Colombia. Pensamiento & Gestión, (43), 157-183. https://doi.org/10.14482/pege.43.10591",
        "Fundación iSocial. (2022). Tendencias de innovación en servicios sociales. Fundación iSocial Barcelona.",
        "Gálvez Rodríguez, M. M., Herrada Lores, S., Haro de Rosario, A., & Saraite Sariene, L. (2025). The effect of online platform management and online interactions on donors' engagement. TEC Empresarial, 19(1), 91-108. https://www.scielo.sa.cr/scielo.php?pid=S1659-33592025000100091&script=sci_arttext",
        "Gargallo Castel, A., & Pérez Sanz, J. (2009). El papel de las tecnologías de la información y la comunicación en las empresas de economía social. REVESCO: Revista de Estudios Cooperativos, (97), 90-116.",
        "Gómez Díaz, J. S. (2019). Guía cómo elaborar el Plan Estratégico de Tecnologías de la Información – PETI [Trabajo de grado, Universidad de Cundinamarca]. Repositorio Institucional Universidad de Cundinamarca.",
        "González Zabala, M. P., & Sánchez Torres, J. M. (2013). Análisis de las estrategias del Gobierno colombiano para la inclusión de los ciudadanos en la Sociedad de la Información propuestas desde 2000 hasta 2011. Revista de Estudios Sociales, (47), 133-146.",
        "Hernández Sampieri, R., Fernández Collado, C., & Baptista Lucio, P. (2014). Metodología de la investigación (6.ª ed.). McGraw-Hill Education.",
        "Herrera Bagui, C. D., & Adames Sánchez, J. C. (2025). Prototipo web para sistematizar el acompañamiento de posibles casos de pérdida de la condición de estudiante para el área de bienestar de la Universidad de Cundinamarca Extensión Chía [Trabajo de grado, Universidad de Cundinamarca].",
        "Hoque, E. (2022). Practical Web Development. BPB Publications.",
        "Huertas Jiménez, R. (2015). Organizaciones no gubernamentales y social media. Análisis de las estrategias comunicativas [Tesis doctoral, Universidad de Málaga]. Repositorio Institucional RIUMA. https://riuma.uma.es/xmlui/handle/10630/11699",
        "Martínez, R., Palma, A., & Velázquez, A. (2020). Revolución tecnológica e inclusión social: Reflexiones sobre desafíos y oportunidades para la política social en América Latina (Serie Políticas Sociales N.° 233). Comisión Económica para América Latina y el Caribe [CEPAL]. https://www.cepal.org/es/publicaciones/45901",
        "Ministerio de Tecnologías de la Información y las Comunicaciones [MinTIC]. (2022). Lineamientos de accesibilidad web para plataformas de servicio ciudadano. MinTIC Colombia.",
        "Monzón Campos, J. L. (2006). Economía Social y conceptos afines: fronteras borrosas y ambigüedades conceptuales del Tercer Sector. CIRIEC-España, Revista de Economía Pública, Social y Cooperativa, (56), 9-24.",
        "Muirragui Irrazábal, V., & Pacheco Olea, F. (2014). Fundaciones sin fines de lucro y su reto de presencia en la web. Yachana Revista Científica / Revista Ciencia y Tecnología, (6), 66-89.",
        "Naciones Unidas. (2023). Informe de los Objetivos de Desarrollo Sostenible 2023: Edición especial. Organización de las Naciones Unidas.",
        "Organización para la Cooperación y el Desarrollo Económicos [OCDE] & Eurostat. (2018). Manual de Oslo: Guía para la recogida e interpretación de datos sobre innovación (4.ª ed.). OCDE Publishing.",
        "Ortega, L. (2022, 22 de octubre). Metodología RUP: ¿Qué es, cuál es su objetivo y cómo se utiliza? Lean Management Blog. https://lean-management.site/rup/",
        "Osterwalder, A., & Pigneur, Y. (2010). Generación de modelos de negocio (Business Model Generation). Ediciones Deusto.",
        "Paiva, V. (2004). ¿Qué es el Tercer Sector? Revista Científica de la UCES, 8(1), 97-115.",
        "Palacios Inocencio, K. N. (2021). Revisión teórica de las herramientas de evaluación y gestión que pueden integrarse a la economía social y solidaria [Trabajo de grado, Universidad Cooperativa de Colombia]. Facultad de Ciencias Económicas y Administrativas.",
        "Parnas, D. L. (1972). On the criteria to be used in decomposing systems into modules. Communications of the ACM, 15(12), 1053-1058.",
        "Presidencia de la República de Colombia & Ministerio de Tecnologías de la Información y las Comunicaciones [MinTIC]. (2012). Directiva Presidencial 04 de 2012: Eficiencia administrativa y lineamientos de la Política Cero Papel en la Administración Pública. Presidencia de la República.",
        "Pressman, R. S., & Maxim, B. R. (2020). Ingeniería del software: Un enfoque práctico (9.ª ed.). McGraw-Hill.",
        "Rogers, E. M. (2001). Evolution: Diffusion of Innovations. En International Encyclopedia of the Social & Behavioral Sciences (pp. 4982-4986). Elsevier.",
        "Sabana Centro Cómo Vamos. (2024). Informe de Calidad de Vida de la Provincia de Sabana Centro 2023-2024. Observatorio Regional Sabana Centro Cómo Vamos.",
        "Serna M., E. (Ed.). (2022). Ingeniería y Desarrollo en la Nueva Era. Editorial Instituto Antioqueño de Investigación.",
        "Sommerville, I. (2016). Software Engineering (10.ª ed.). Pearson.",
        "Tejada Estrada, G. C., Cruz Montero, J. M., Uribe Hernández, Y. C., & Ríos Herrera, J. J. (2019). Innovación tecnológica: reflexiones teóricas. Revista Venezolana de Gerencia, 24(85), 199-210. https://www.redalyc.org/articulo.oa?id=29058864011",
        "Universidad de Cundinamarca. (2022). Acuerdo No. 039 de 2022: Lineamientos y normativas para Opciones de Grado y el Modelo Educativo Digital Transmoderno (MEDIT). Universidad de Cundinamarca.",
        "Universidad de Cundinamarca. (2024). Guía Opción de Grado Emprendimiento (Código ADOr006, Versión 10, Acuerdo 012 de 2024). Proceso Gestión Documental, Universidad de Cundinamarca.",
        "Vidal, P., Torres, D., Guix, B., & Peña Rodríguez, M. (2005). La responsabilidad social de las organizaciones no lucrativas: Aproximación conceptual y desarrollo del modelo RSO (Colección Papers de Investigación OTS N.° 03). Observatorio del Tercer Sector.",
        "Villar Gómez, R. (2018). Las fundaciones en Colombia: Características, tendencias y desafíos. Asociación de Fundaciones Familiares y Empresariales [AFE].",
        "Winocur, R. (2007). La apropiación de las TIC en la vida cotidiana. Revista TELOS (Cuadernos de Comunicación e Innovación), (73), 109-117.",
        "World Wide Web Consortium [W3C]. (2023). Web Content Accessibility Guidelines (WCAG) 2.2: W3C Recommendation. W3C. https://www.w3.org/TR/WCAG22/",
        "Zanfrillo, A. I., Artola, M. A., & de Vega, R. E. (2018). Modelos de comunicación digital en organizaciones del Tercer Sector para la promoción de la salud. Revista Electrónica Gestión de las Personas y Tecnología, 11(33), 48-61. https://www.redalyc.org/pdf/4778/477857553007.pdf"
    ])
]
