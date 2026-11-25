# -*- coding: utf-8 -*-
"""
Contenido académico completo de los 12 Anexos (Anexo A al Anexo L) del documento final de grado:
CONEXIÓN SOLIDARIA. TECNOLOGÍA PARA EL CAMBIO SOCIAL
Autores: Angélica Rosa Olier Quiroga y Oscar Giovanni Robayo Olaya
Universidad de Cundinamarca - Extensión Chía (2026)
"""

ANEXOS_COMPLETOS = [
    ("H1", "ANEXOS"),

    # =========================================================================
    # ANEXO A
    # =========================================================================
    ("H2", "Anexo A. Instrumentos de recolección de información y formularios digitales aplicados"),
    ("P", "En este anexo se documentan los instrumentos de recolección de datos diseñados y validados bajo juicio de expertos para el desarrollo del diagnóstico mixto (Sección 3.3): (1) las evidencias visuales y enlaces directos de los dos formularios digitales aplicados en Google Forms (Figuras A1 y A2), cuya parametrización completa por pregunta y escala se detalla en las Tablas 6A, 6A-1 y 6A-2 del Capítulo 3; y (2) el Guion de Entrevista Semiestructurada y la Ficha de Observación Directa No Participante aplicados en campo (Tabla A1)."),
    ("UL", [
        "Enlace oficial del Instrumento Digital 1 (Conexión Solidaria - Encuesta de Percepción Ciudadana y Voluntariado, n = 170 respuestas): https://forms.gle/FbrAEsHmz2sQWa4A6",
        "Enlace oficial del Instrumento Digital 2 (Conexión Solidaria - Diagnóstico Operativo y de Comunicación para Fundaciones, n = 4 fundaciones): https://forms.gle/t9MoqpGDwrZzbntW7",
        "Mensaje de difusión empleado en WhatsApp: «¿Nos ayudas con tu opinión? Como parte de nuestro proyecto de grado de emprendimiento en Ingeniería de Sistemas (U. de Cundinamarca) estamos formulando la creación de una fundación tecnológica orientada a entregar software gratuito para hacer sostenibles a las fundaciones sociales locales y rurales. Agradecemos tu apoyo respondiendo esta breve encuesta (toma solo 3 min): https://forms.gle/FbrAEsHmz2sQWa4A6. ¿Conoces a líderes o integrantes de alguna fundación? Por favor comparte este link con ellos: https://forms.gle/t9MoqpGDwrZzbntW7 ¡Tu ayuda suma muchísimo al cambio social!»"
    ]),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\formulario_google_comunidad.png",
        "caption": "Figura A1. Interfaz del formulario digital en línea «Conexión Solidaria - Encuesta de Percepción Ciudadana y Voluntariado» (Google Forms)",
        "note": "Nota. Captura directa del instrumento aplicado a través de https://forms.gle/FbrAEsHmz2sQWa4A6 (n = 170 respuestas registradas)."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\formulario_google_fundaciones.png",
        "caption": "Figura A2. Interfaz del formulario digital en línea «Conexión Solidaria - Diagnóstico Operativo y de Comunicación para Fundaciones» (Google Forms)",
        "note": "Nota. Captura directa del instrumento aplicado a través de https://forms.gle/t9MoqpGDwrZzbntW7 (n = 4 fundaciones diagnosticadas)."
    }),
    ("TABLE", {
        "title": "Tabla A1. Guion de entrevista semiestructurada y ficha de observación directa aplicada a las fundaciones rurales",
        "headers": ["Eje Diagnóstico", "Preguntas Guía de la Entrevista Semiestructurada", "Criterios de la Ficha de Observación en Campo"],
        "rows": [
            ["1. Perfil institucional y población", "¿Cuál es el objeto social de la fundación, en qué vereda o municipio opera y cuántas personas o animales beneficia de manera permanente?", "Verificar condiciones físicas de la sede rural, número de colaboradores en sitio y tipo de población atendida."],
            ["2. Capacidad administrativa y registros", "¿Cómo registran actualmente la entrada de donaciones en dinero o en especie y el control de inventarios o gastos?", "Observar existencia de libros o cuadernos manuales, planillas impresas, hojas de cálculo o ausencia de registro formal."],
            ["3. Infraestructura TIC y conectividad", "¿Con qué equipos de cómputo o teléfonos cuentan en la sede y cómo es la calidad de la señal de internet en la vereda?", "Comprobar tipo de conexión disponible (datos móviles 3G/4G, banda ancha o sin red fija) y dispositivos utilizados."],
            ["4. Estrategia de comunicación y redes", "¿Tienen página web o perfiles en redes sociales? ¿Cada cuánto publican y quién administra esos canales?", "Revisar última fecha de publicación en redes sociales, existencia o ausencia de portal web y medición de alcance."],
            ["5. Captación de donaciones y voluntariado", "¿A través de qué medios consiguen donantes y voluntarios actualmente y cuáles son las principales dificultades que enfrentan?", "Identificar dependencia del voz a voz local, falta de protocolos de respuesta y necesidades urgentes no cubiertas."],
            ["6. Requerimientos para el MVP", "¿Qué funciones debería tener una plataforma web gratuita para que les resulte verdaderamente fácil y útil en su trabajo diario?", "Validar prioridad de módulos: mapa de visibilidad, catálogo de insumos/dinero, agenda de voluntarios y certificados."]
        ],
        "note": "Nota. Instrumento validado en el espacio académico de Ciencia, Tecnología e Innovación III (Olier & Robayo, 2025)."
    }),

    # =========================================================================
    # ANEXO B
    # =========================================================================
    ("H2", "Anexo B. Encuestas aplicadas, ficha técnica y resultados del diagnóstico (Fundaciones n = 4 y Comunidad n = 170)"),
    ("P", "En concordancia con las Secciones 3.3 y 3.4 del Capítulo 3, este anexo presenta la tabulación íntegra de las respuestas obtenidas en los dos instrumentos primarios aplicados en el estudio: (1) la Encuesta Diagnóstica de Fundaciones (archivo maestro Respuestas_Encuesta_Fundaciones_Conexion_Solidaria.xlsx, n = 4 organizaciones: Gotitas de Amor en Cajicá, Casa de los Abuelos en Machetá, Campamentos de Nueva Vida en Simijaca y Patitas Campesinas en La Calera), y (2) la Encuesta de percepción e interés sobre las organizaciones sociales y la plataforma Conexión Solidaria (archivo maestro 150_Respuestas_Conexion_Solidaria.xlsx, con n = 170 respuestas registradas entre el 28 de septiembre y el 16 de octubre de 2026 mediante muestreo no probabilístico por conveniencia y participación voluntaria en WhatsApp)."),
    ("TABLE", {
        "title": "Tabla B1. Matriz completa de respuestas de las 14 preguntas de la Encuesta Diagnóstica de Fundaciones (n = 4)",
        "headers": ["Ítem / Pregunta de la Encuesta", "1. Gotitas de Amor (Mis Gotitas de Amor)", "2. Casa de los Abuelos (Abuelos Campesinos)", "3. Campamentos de Nueva Vida (Campamentos de Vida Nueva)", "4. Patitas Campesinas"],
        "rows": [
            ["1. Nombre de la fundación u organización", "Gotitas de Amor (Mis Gotitas de Amor)", "Casa de los Abuelos (Abuelos Campesinos)", "Campamentos de Nueva Vida (Campamentos de Vida Nueva)", "Patitas Campesinas"],
            ["2. Municipio Sede", "Cajicá", "Machetá", "Simijaca", "La Calera"],
            ["3. Entorno geográfico", "Exclusivamente en casco urbano", "Mixto (tanto en veredas como en casco urbano)", "Mixto (tanto en veredas como en casco urbano)", "Principalmente en zonas rurales / veredales"],
            ["4. Tipo de organización", "Fundación comunitaria / de base local", "Fundación comunitaria / de base local", "Fundación independiente / filantrópica", "Fundación comunitaria / de base local"],
            ["5. Población beneficiada", "Primera infancia, niñez y adolescencia; Familias y hogares en vulnerabilidad socioeconómica", "Adultos mayores / Tercera edad; Familias y hogares en vulnerabilidad socioeconómica; Comunidades rurales, campesinas o agrícolas", "Familias y hogares en vulnerabilidad socioeconómica; Juventud; Comunidad o ciudadanía en general", "Animales en situación de abandono o rescate; Comunidades rurales, campesinas o agrícolas"],
            ["6. Canales de comunicación", "No contamos con un canal de comunicación continuo", "Medios comunitarios tradicionales (radio local, carteleras, perifoneo)", "Canales de mensajería (WhatsApp, Telegram)", "Redes sociales (Facebook, Instagram, TikTok, etc.)"],
            ["7. Frecuencia de publicación", "Solo cuando hay un evento o necesidad urgente", "Quincenal o mensualmente", "Quincenal o mensualmente", "Varias veces a la semana"],
            ["8. Respuesta del público (escala 1 a 5)", "2", "3", "2", "4"],
            ["9. Medición de métricas", "No analizamos métricas por falta de tiempo o herramientas especializadas.", "Solo revisamos comentarios y mensajes directamente.", "No analizamos métricas por falta de tiempo o herramientas especializadas.", "Sí, revisamos métricas básicas de redes sociales periódicamente."],
            ["10. Fuentes de apoyo", "Donaciones económicas de personas naturales; Donaciones en especie / insumos (alimentos, insumos, ropa); Aporte voluntario no remunerado de miembros o comunidad", "Donaciones económicas de personas naturales; Donaciones en especie / insumos (alimentos, insumos, ropa); Subvenciones, convenios o fondos públicos gubernamentales; Aporte voluntario no remunerado de miembros o comunidad", "Donaciones económicas de personas naturales; Aporte voluntario no remunerado de miembros o comunidad", "Donaciones económicas de personas naturales; Donaciones en especie / insumos (alimentos, insumos, ropa); Aporte voluntario no remunerado de miembros o comunidad"],
            ["11a. Desafío: Falta de recursos económicos", "1 (Mayor)", "1 (Mayor)", "2", "1 (Mayor)"],
            ["11b. Desafío: Reclutar y retener voluntarios", "2", "3", "3", "2"],
            ["11c. Desafío: Baja visibilidad pública", "3", "2", "1 (Mayor)", "3"],
            ["11d. Desafío: Carga administrativa", "4", "4", "5 (Menor)", "4"],
            ["11e. Desafío: Medir e informar impacto", "5 (Menor)", "5 (Menor)", "4", "5 (Menor)"],
            ["12. Interés en plataforma gratuita", "Muy interesados (la adoptaríamos de inmediato)", "Muy interesados (la adoptaríamos de inmediato)", "Muy interesados (la adoptaríamos de inmediato)", "Muy interesados (la adoptaríamos de inmediato)"],
            ["13. Funcionalidades más valiosas", "Módulo para publicar necesidades concretas de donaciones (dinero o insumos); Módulo de reclutamiento y agenda de voluntarios por áreas/horarios", "Módulo de reclutamiento y agenda de voluntarios por áreas/horarios; Perfil institucional verificado para generar confianza y legitimidad", "Perfil institucional verificado para generar confianza y legitimidad; Módulo para publicar necesidades concretas de donaciones (dinero o insumos)", "Módulo para publicar necesidades concretas de donaciones (dinero o insumos); Módulo de reclutamiento y agenda de voluntarios por áreas/horarios"],
            ["14. Datos de contacto", "3133934744 | misgotitasdeamor2022@gmail.com", "Inés Camelo | 3112089943 | abuelitosmacheta@gmail.com", "Padre César | 3107173205 | www.campamentosdevidanueva.org", "3118854757 | patitascampesinas@gmail.com | patitascampesinas.org"]
        ],
        "note": "Nota. Transcripción literal de las hojas 'Respuestas Encuesta' y 'Detalle por Fundación' del archivo Respuestas_Encuesta_Fundaciones_Conexion_Solidaria.xlsx (Olier & Robayo, 2026)."
    }),
    ("TABLE", {
        "title": "Tabla B2. Síntesis estadística de indicadores de la Encuesta Diagnóstica de Fundaciones (n = 4)",
        "headers": ["Dimensión Evaluada", "Indicador / Categoría", "Frecuencia Absoluta", "Porcentaje / Promedio", "Implicación para el Diseño del MVP"],
        "rows": [
            ["Tipo de organización", "Fundación comunitaria / de base local", "3 de 4", "75,0 %", "El sistema debe adaptarse a organizaciones pequeñas sin departamento TI."],
            ["Presencia territorial", "Actuación rural o mixta (veredas y urbano)", "3 de 4", "75,0 %", "Requerimiento de arquitectura ligera para baja señal móvil (RNF01)."],
            ["Canal web de difusión", "Usa portal web como canal habitual de difusión (P6)", "0 de 4", "0,0 %", "Necesidad crítica de brindar perfil público georreferenciado gratuito (RF03)."],
            ["Respuesta del público", "Calificación en escala Likert (1 a 5)", "Rango: 2 a 4", "Promedio: 2,75 / 5,0", "Baja efectividad de los canales actuales informales o tradicionales."],
            ["Analítica digital", "No mide métricas o solo lee comentarios", "3 de 4", "75,0 %", "Incorporación de un Dashboard visual simple con barras de progreso (RF10)."],
            ["Sostenimiento", "Depende de personas naturales y trabajo voluntario", "4 de 4", "100,0 %", "Gratuidad absoluta (0 % comisión) para las OSAL en el modelo Canvas."],
            ["Desafío #1 (Mayor)", "Falta de recursos económicos (ranking 1 a 5)", "3 en #1, 1 en #2", "Promedio: 1,25 (Crítico)", "Módulo de necesidades en dinero e insumos con trazabilidad (RF04, RF07)."],
            ["Desafío #2", "Baja visibilidad pública (ranking 1 a 5)", "1 en #1, 1 en #2, 2 en #3", "Promedio: 2,25 (Alto)", "Mapa interactivo regional y filtros por municipio y causa (RF03)."],
            ["Desafío #3", "Reclutar y retener voluntarios (ranking 1 a 5)", "2 en #2, 2 en #3", "Promedio: 2,50 (Alto)", "Módulo de convocatorias, horarios y control de cupos (RF05, RF06)."],
            ["Intención de adopción", "Muy interesados (adopción inmediata)", "4 de 4", "100,0 %", "Validación plena de aceptación de la propuesta de valor del MVP."]
        ],
        "note": "Nota. Procesamiento estadístico descriptivo a partir de Respuestas_Encuesta_Fundaciones_Conexion_Solidaria.xlsx."
    }),
    ("TABLE", {
        "title": "Tabla B3. Tabulación estadística completa de las 170 respuestas de la Encuesta a Donantes y Voluntarios Potenciales (150_Respuestas_Conexion_Solidaria.xlsx)",
        "headers": ["Pregunta del Instrumento", "Opción de Respuesta / Categoría", "Frecuencia Absoluta (n = 170)", "Porcentaje sobre Muestra (%)", "Interpretación y Trazabilidad con el Proyecto"],
        "rows": [
            ["1. Rango de edad", "26 a 35 años", "61", "35,9 %", "Adultos jóvenes económicamente activos (segmento principal)."],
            ["1. Rango de edad", "36 a 50 años", "59", "34,7 %", "Adultos consolidados con alta capacidad de donación."],
            ["1. Rango de edad", "18 a 25 años", "25", "14,7 %", "Jóvenes universitarios con disponibilidad para voluntariado."],
            ["1. Rango de edad", "Más de 50 años", "25", "14,7 %", "Ciudadanos mayores con vocación comunitaria."],
            ["2. Ocupación principal", "Empleado(a)", "96", "56,5 %", "Fuerza laboral vinculada a empresas de la región."],
            ["2. Ocupación principal", "Independiente / Emprendedor(a)", "31", "18,2 %", "Profesionales autónomos y comerciantes locales."],
            ["2. Ocupación principal", "Estudiante", "20", "11,8 %", "Base estudiantil para horas de servicio social y brigadas."],
            ["2. Ocupación principal", "Desempleado(a) / En búsqueda de empleo", "13", "7,6 %", "Ciudadanos con disponibilidad de tiempo solidario."],
            ["2. Ocupación principal", "Retirado(a)", "10", "5,9 %", "Adultos pensionados residentes en la Sabana."],
            ["3. Municipio de residencia", "Chía", "105", "61,8 %", "Nodo principal de influencia de la Extensión Chía UdeC."],
            ["3. Municipio de residencia", "Bogotá D.C. (corredor norte vinculado a Sabana)", "33", "19,4 %", "Potencial donante/voluntario metropolitano hacia la Sabana."],
            ["3. Municipio de residencia", "Otro municipio de Sabana Centro / Norte", "22", "12,9 %", "Cajicá, Sopó, Tabio, Tenjo, Tocancipá, Cogua, etc."],
            ["3. Municipio de residencia", "Zipaquirá", "6", "3,5 %", "Segundo centro urbano de Sabana Centro."],
            ["3. Municipio de residencia", "Cota", "4", "2,4 %", "Corredor occidental de la Sabana."],
            ["4. Tipo de zona de residencia", "Urbana (Casco urbano / centro)", "93", "54,7 %", "Población urbana que requiere mapa para ubicar OSAL veredales."],
            ["4. Tipo de zona de residencia", "Rural / Periurbana (Vereda o sector campestre)", "77", "45,3 %", "Alta proporción rural que valida la arquitectura ligera LBRSA."],
            ["5. Conocimiento de OSAL", "Sí, conozco varias y sé qué actividades realizan", "60", "35,3 %", "Solo un tercio conoce el trabajo de las fundaciones locales."],
            ["5. Conocimiento de OSAL", "Casi no tengo conocimiento de organizaciones locales", "49", "28,8 %", "Evidencia directa de invisibilidad digital del tercer sector."],
            ["5. Conocimiento de OSAL", "Conozco algunas de nombre, no en detalle sus actividades", "42", "24,7 %", "Falta de información detallada sobre programas y necesidades."],
            ["5. Conocimiento de OSAL", "No conozco ninguna", "19", "11,2 %", "Sumado a los dos anteriores: 64,7 % de desconocimiento local."],
            ["6. Causas de mayor interés*", "Infancia y juventud", "96", "56,5 %", "Alineado con ODS 1, 2 y 4 (Gotitas de Amor / FUNDAULA)."],
            ["6. Causas de mayor interés*", "Adulto mayor", "65", "38,2 %", "Alineado con ODS 1, 2 y 3 (Casa de los Abuelos / FARASAN)."],
            ["6. Causas de mayor interés*", "Desarrollo comunitario y rural", "60", "35,3 %", "Alineado con ODS 1, 10 y 11 (Comunidades veredales)."],
            ["6. Causas de mayor interés*", "Medio ambiente y sostenibilidad", "56", "32,9 %", "Alineado con ODS 11 y 15 (CORPOJUAICA)."],
            ["6. Causas de mayor interés*", "Educación y formación técnica", "56", "32,9 %", "Alineado con ODS 4 y 9 (Alfabetización y talleres)."],
            ["6. Causas de mayor interés*", "Salud y bienestar general", "43", "25,3 %", "Alineado con ODS 3 (Campamentos de Vida Nueva / ASOMAYOR)."],
            ["6. Causas de mayor interés*", "Cuidado y protección animal", "41", "24,1 %", "Alineado con ODS 15 (Patitas Campesinas / FUNHUELLAS)."],
            ["6. Causas de mayor interés*", "Artes y emprendimiento comunitario", "15", "8,8 %", "Iniciativas culturales y productivas locales."],
            ["7. Apoyo en el último año*", "Voluntariado presencial (tiempo y mano de obra)", "60", "35,3 %", "Sustenta el módulo de convocatorias y cupos (RF05, RF06)."],
            ["7. Apoyo en el último año*", "Donación de bienes materiales o insumos", "55", "32,4 %", "Sustenta el catálogo de necesidades en especie (RF04, RF07)."],
            ["7. Apoyo en el último año*", "Donaciones de dinero (únicas o recurrentes)", "42", "24,7 %", "Sustenta el registro de aportes monetarios y certificados (RF09)."],
            ["7. Apoyo en el último año*", "No he participado activamente", "35", "20,6 %", "Población latente que puede activarse mediante la plataforma."],
            ["7. Apoyo en el último año*", "Voluntariado profesional / remoto", "33", "19,4 %", "Aporte de conocimientos técnicos, jurídicos o pedagógicos."],
            ["7. Apoyo en el último año*", "Difusión de campañas en redes sociales", "32", "18,8 %", "Multiplicadores digitales de las campañas publicadas."],
            ["8. Condición indispensable", "Transparencia total en el uso de fondos y recursos", "99", "58,2 %", "Justifica protocolo PGVTT, barras de avance y hash SHA-256."],
            ["8. Condición indispensable", "Claridad en actividades o tareas específicas", "37", "21,8 %", "Justifica detalle de funciones, horarios y cupos en voluntariado."],
            ["8. Condición indispensable", "Facilidad para realizar el aporte de forma digital", "18", "10,6 %", "Justifica interfaz sencilla en 3 pasos y diseño Mobile-First."],
            ["8. Condición indispensable", "Cercanía comunitaria o geográfica", "16", "9,4 %", "Justifica el mapa interactivo Leaflet por municipio (RF03)."],
            ["9. Disposición de uso MVP", "Totalmente dispuesto(a)", "90", "52,9 %", "Adopción inmediata asegurada por más de la mitad de la muestra."],
            ["9. Disposición de uso MVP", "Probablemente sí", "73", "42,9 %", "Sumado al anterior: 95,9 % (163 de 170) de intención positiva."],
            ["9. Disposición de uso MVP", "No me interesaría", "7", "4,1 %", "Rechazo marginal inferior al 5 %."]
        ],
        "note": "Nota. *En las preguntas 6 y 7 de selección múltiple, el porcentaje se calcula sobre el total de encuestados (n = 170). Fuente: Procesamiento íntegro de 150_Respuestas_Conexion_Solidaria.xlsx (recolección del 28/09/2026 al 16/10/2026)."
    }),

    # =========================================================================
    # ANEXO C
    # =========================================================================
    ("H2", "Anexo C. Matrices de caracterización de las organizaciones"),
    ("P", "En la Tabla C1 se presenta la matriz técnica detallada de las cinco organizaciones sociales de la Sabana Centro y Norte de Cundinamarca caracterizadas y cargadas en la semilla de datos del Producto Mínimo Viable (archivo backend/app/seed.py) para validar todos los flujos de georreferenciación, campañas, necesidades, donaciones, voluntariado e impacto por ODS."),
    ("TABLE", {
        "title": "Tabla C1. Ficha técnica detallada de caracterización de las cinco OSAL parametrizadas en el MVP Conexión Solidaria",
        "headers": ["Atributo Institucional", "OSAL 1: FARASAN", "OSAL 2: FUNHUELLAS", "OSAL 3: ASOMAYOR", "OSAL 4: FUNDAULA", "OSAL 5: CORPOJUAICA"],
        "rows": [
            ["Razón Social Completa", "Fundación Hogar Geriátrico San Antonio", "Fundación Huellas de la Sabana", "Asociación Semillas de Esperanza", "Fundación Aula Viva Primera Infancia", "Corporación Ambiental Guardianes de Juaica"],
            ["NIT Registrado", "900.412.589-1", "901.128.743-4", "832.009.415-7", "900.874.321-9", "901.345.678-2"],
            ["Municipio y Vereda", "Cogua (Vereda Rodamontal)", "Cajicá (Vereda Chuntame)", "Zipaquirá (Sector Rural San Jorge)", "Chía (Vereda Fagua / Tíquiza)", "Tabio (Vereda Lourdes / Peña de Juaica)"],
            ["Coordenadas GPS (Lat, Lon)", "5.0631, -73.9812", "4.9185, -74.0280", "5.0221, -74.0052", "4.8624, -74.0589", "4.9172, -74.0984"],
            ["Categoría Principal", "Adulto Mayor y Salud", "Protección Animal", "Comunidades Vulnerables y Juventud", "Niñez y Educación Rural", "Medio Ambiente y Reforestación"],
            ["Alineación ODS Principal", "ODS 1, ODS 2, ODS 3, ODS 10", "ODS 11, ODS 15, ODS 17", "ODS 1, ODS 2, ODS 3, ODS 10", "ODS 1, ODS 4, ODS 9, ODS 10", "ODS 11, ODS 15, ODS 17"],
            ["Campaña Activa en MVP", "Abuelos Dignos en Rodamontal", "Alimento y Salud para 85 Rescatados", "Comedor y Oficios para San Jorge", "Kits y Conectividad para Vereda Fagua", "Restauración Hídrica del Cerro Juaica"],
            ["Necesidad Principal Parametrizada", "Pañales geriátricos y suplemento nutricional ($3.500.000 COP / 120 paq).", "Alimento concentrado canino/felino ($4.200.000 COP / 500 kg).", "Mercados básicos y dotación de taller ($5.000.000 COP / 80 mercados).", "Kits escolares y tabletas educativas ($3.800.000 COP / 60 kits).", "Plántulas nativas y herramientas de siembra ($2.800.000 COP / 400 árboles)."],
            ["Convocatoria Voluntariado Activa", "Brigada de salud, fisioterapia y acompañamiento geriátrico (10 cupos).", "Jornada de adecuación de caniles, baño y paseo canino (15 cupos).", "Talleres de apoyo psicosocial y alfabetización digital (8 cupos).", "Tutorías de refuerzo escolar en lectura y matemáticas (12 cupos).", "Jornada veredal de siembra y mantenimiento de vivero (25 cupos)."],
            ["Estado Ley 1581 y Validación", "Aceptada (2026) / OSAL Verificada", "Aceptada (2026) / OSAL Verificada", "Aceptada (2026) / OSAL Verificada", "Aceptada (2026) / OSAL Verificada", "Aceptada (2026) / OSAL Verificada"]
        ],
        "note": "Nota. Todos los registros anteriores se encuentran precargados y operativos en la base de datos del MVP (backend/app/seed.py)."
    }),

    # =========================================================================
    # ANEXO D
    # =========================================================================
    ("H2", "Anexo D. Evidencias del diagnóstico, portafolio CTeI y Resúmenes Analíticos Especializados (RAE)"),
    ("P", "Las evidencias documentales y gráficas del diagnóstico realizado comprenden las tablas estadísticas procesadas de la Encuesta Nacional de Investigación y Desarrollo del DANE (2021) y de la AFE (2018) (incorporadas en las Figuras 1 a 5 del Capítulo 3), la matriz de alineación territorial con los Objetivos de Desarrollo Sostenible (Figura D1), el Portafolio Digital de CTeI de los autores (https://sites.google.com/view/angelica-olier-portafolio-ctei/página-principal) y los Resúmenes Analíticos Especializados (RAE) elaborados durante la fase de fundamentación investigativa:"),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\Conexión_Solidaria_T_p4_img1_1439x292.jpeg",
        "caption": "Figura D1. Esquema de alineación del diagnóstico de Conexión Solidaria con los Objetivos de Desarrollo Sostenible (ODS)",
        "note": "Nota. Elaboración propia en el marco del componente investigativo del proyecto (Olier & Robayo, 2025)."
    }),
    ("P_BOLD", "RAE 1: Guía práctica de comunicación para asociaciones sin ánimo de lucro en Antioquia (Acevedo de la Ossa, 2023 - Universidad EAFIT)"),
    ("P", "Resumen: El autor destaca la importancia de la información y la comunicación en empresas de carácter social o asociaciones sin ánimo de lucro, con el fin de llevar el mensaje a la comunidad de manera que puedan obtener recursos que suplan sus necesidades. La tecnología y el mundo globalizado en el que estamos viviendo permiten enviar un mensaje en cuestión de segundos, pero al hacerlo se debe ser consciente y tener cuidado de no caer en amarillismo, y siempre es mejor un mensaje esperanzador y no que muestre la miseria que evoque lástima y manipule las emociones del receptor de forma poco profesional. Continuando por un recorrido por los diferentes medios de comunicación, realiza una serie de recomendaciones para manejar los contenidos tanto en el sitio web como en las diferentes redes sociales, detallando sus funcionalidades además de realizar una breve explicación de los formatos y sus ventajas al momento de comunicar según el objetivo."),
    ("P", "Conclusiones y Comentario Crítico: Identifica la importancia de guiar y brindar herramientas en la planeación estratégica para que la comunicación sea efectiva y ayude a la fundación a alcanzar sus objetivos manteniendo su reputación y entregando información relevante para la comunidad. Es un documento que aporta una guía básica del uso de herramientas tecnológicas que apoyan a las organizaciones sin ánimo de lucro a comunicar sus necesidades y que el mensaje pueda llegar a la comunidad de manera directa, lo que ayuda a dichas organizaciones a dar el primer paso e iniciar el camino."),

    ("P_BOLD", "RAE 2: Diagnóstico y capacitación a entidades sin ánimo de lucro. Provincia del Sumapaz, Colombia (Escobar Cazal & Escobar Reyes, 2017 - Pensamiento y Gestión)"),
    ("P", "Resumen y Metodología: En 2012, la Cámara de Comercio de Bogotá sucursal Fusagasugá registró 926 entidades sin ánimo de lucro en la Provincia del Sumapaz. Dada su relevancia económica y social en la región, se realizó un diagnóstico de 50 de estas organizaciones utilizando un método de investigación descriptivo-analítico y un plan de acción. La recolección de datos se realizó mediante encuestas, entrevistas y revisión de documentos internos de las organizaciones. Se identificaron problemas como la falta de liderazgo gerencial, débil planeación estratégica, bajo nivel de innovación y producción, y difícil acceso a créditos. Sin embargo, también se destacaron fortalezas como la toma de decisiones democráticas, el sentido de pertenencia y compromiso, y la motivación para trabajar en equipo."),
    ("P", "Conclusiones y Comentario Crítico: Es crucial mejorar el liderazgo gerencial y la planeación estratégica dentro de las organizaciones para aumentar su eficiencia y efectividad. El artículo presenta una metodología descriptivo-analítica robusta que permite una comprensión detallada de la situación de las entidades sin ánimo de lucro en Cundinamarca. La combinación de encuestas, entrevistas y revisión documental proporciona una base sólida para el diagnóstico, identificando tanto problemas como fortalezas. Para nuestro proyecto, los apartados de metodología y los instrumentos de recolección de información utilizados en este estudio son especialmente valiosos."),

    ("P_BOLD", "RAE 3: La información financiera de las entidades sin ánimo de lucro. Una aproximación internacional a su marco conceptual (Aliaga Bernal, 2009 - Contaduría Universidad de Antioquia)"),
    ("P", "Resumen y Resultados: El aumento de entidades sin ánimo de lucro orientadas a satisfacer la demanda de bienes y servicios sociales ha generado la necesidad de adaptar las normas contables para la elaboración de información financiera específica para estas organizaciones. Este trabajo analiza comparativamente los principios que guían la elaboración de la información contable de entidades no lucrativas desde una perspectiva internacional, confrontando el modelo anglosajón (bajo el SFAS 117, que requiere detallar los efectos de las transacciones en los activos netos y proporcionar información específica por programas de servicios) con el modelo europeo-continental."),
    ("P", "Conclusiones y Comentario Crítico: La información financiera no es un fin en sí mismo, sino que su papel es ser útil a los usuarios de la misma, especialmente cuando al menos el 70 % de los ingresos que entren en la entidad se destinen a los fines no lucrativos. El estudio destaca la importancia de desarrollar reglas claras que mejoren la transparencia y la confianza de los donantes, así como la eficiencia en la gestión de recursos."),

    ("P_BOLD", "RAE 4: Hacia el reconocimiento de la inclusión digital como un derecho fundamental en Colombia (Chacón-Penagos et al., 2017 - Vniversitas)"),
    ("P", "Resumen y Conclusiones: Este artículo examina el reconocimiento de la inclusión digital como un derecho fundamental en Colombia, contribuyendo al desarrollo de la teoría constitucional sobre los derechos fundamentales en el país. En los últimos años, la comunidad nacional e internacional ha mostrado un creciente interés en la brecha digital, considerándola una problemática estrechamente vinculada con los derechos fundamentales. El estudio concluye que garantizar el acceso universal y de calidad a las TIC es esencial para evitar la exclusión digital y promover la equidad, y que es prioritario que desde la academia se propicien espacios y soluciones sobre el reconocimiento de la necesidad de acceder y usar las TIC en condiciones de universalidad y calidad."),

    ("P_BOLD", "RAE 5: La apropiación de las TIC en la vida cotidiana (Winocur, 2007 - Revista TELOS)"),
    ("P", "Resumen y Comentario Crítico: La autora explica la importancia de entender cómo las personas usan y perciben las tecnologías de la información y comunicación (TIC) en su vida cotidiana para diseñar soluciones más acertadas. No se trata solo de analizar cifras, sino de incluir estudios sociales que reflejen cómo cada grupo social se apropia de estas tecnologías. Se deben estudiar las prácticas locales y los significados que las personas les dan a estas tecnologías, ya que su uso varía según el contexto. A partir del análisis de los contextos y necesidades de los diferentes grupos, se pueden diseñar estrategias más eficaces y ajustadas para fomentar la alfabetización digital y la inclusión tecnológica, con especial atención a las realidades locales."),

    ("P_BOLD", "RAE 6: TICs para una educación inclusiva (Castillo et al., 2013 - Universidad Autónoma de Entre Ríos)"),
    ("P", "Resumen y Comentario Crítico: El artículo aborda el impacto de las TIC en la inclusión social de poblaciones vulnerables, mejorando su calidad de vida al facilitar la interacción con el mundo. Aunque en países desarrollados las aplicaciones TIC especializadas están ampliamente disponibles, en América Latina su acceso es limitado debido a los altos costos y a la falta de producción local. Proyectos académicos como este abren la posibilidad de crear tecnologías accesibles replicables en el ámbito local que no solo cubran una necesidad social, sino que también ofrezcan oportunidades de crecimiento para las fundaciones comunitarias."),

    # =========================================================================
    # ANEXO E
    # =========================================================================
    ("H2", "Anexo E. Requerimientos funcionales, matriz RBAC, casos de uso y trazabilidad"),
    ("P", "En este anexo se presentan la Matriz Maestra de Trazabilidad Ingenieril (Tabla E1) —que vincula la problemática diagnóstica con los objetivos específicos, los bloques del Modelo de Negocio Canvas, los Requerimientos Funcionales (RF01 a RF12) y No Funcionales (RNF01 a RNF06), los Casos de Uso (CU01 a CU10), las tablas del modelo en 5FN y los indicadores de validación— y la Matriz de Control de Acceso Basado en Roles RBAC (Tabla E2)."),
    ("TABLE", {
        "title": "Tabla E1. Matriz maestra de trazabilidad ingenieril (Problema - Objetivos - Canvas - Requerimientos - Casos de Uso - Tablas 5FN - Pruebas)",
        "headers": ["Hallazgo del Diagnóstico", "Objetivo Específico", "Bloque del Canvas", "Requerimiento (RF / RNF)", "Caso de Uso Asociado", "Tablas Principales en 5FN", "Caso de Prueba QA"],
        "rows": [
            ["Invisibilidad web de las OSAL rurales y desconfianza por falta de validación legal.", "OE1, OE3, OE4", "Propuesta de Valor / Actividades Clave", "RF01 (Registro y validación OSAL) y RNF05 (Seguridad y Ley 1581).", "CU01: Registro y Validación Documental de OSAL.", "fundaciones_osal, sedes_osal, documentos_legales_osal, estados_validacion_osal.", "CP-01, CP-02, CP-13"],
            ["Accesos informales sin distinción de permisos entre fundaciones y ciudadanos.", "OE3, OE4", "Relaciones con Usuarios / Recursos Clave", "RF02 (Autenticación JWT y RBAC).", "CU02: Autenticación y Gestión de Sesión por Rol.", "usuarios, credenciales_seguridad, roles_sistema, usuarios_roles, sesiones_token.", "CP-03, CP-04"],
            ["Ciudadanos desconocen qué fundaciones operan en su municipio y qué ODS atienden.", "OE1, OE2, OE4", "Canales / Segmentos de Clientes", "RF03 (Directorio y Mapa Georreferenciado) y RNF01 (Baja conectividad).", "CU03: Exploración Georreferenciada por Municipio y ODS.", "municipios, fundaciones_osal, sedes_osal, ods_objetivos, osal_ods_alineacion.", "CP-05, CP-14"],
            ["Publicaciones efímeras en redes sociales sin metas claras de dinero o insumos.", "OE2, OE4", "Propuesta de Valor / Canales", "RF04 (Publicación de campañas y necesidades) y RF11 (Alertas acopio).", "CU04: Publicación de Campaña Social; CU05: Parametrización de Necesidades.", "campanas_sociales, campanas_ods, necesidades_recurso, unidades_medida, categorias_causa.", "CP-06"],
            ["Pérdida de trazabilidad de las donaciones y falta de certificados tributarios (RTE).", "OE4, OE5, OE6", "Propuesta de Valor / Estructura de Costos", "RF07 (Registro donación), RF08 (Verificación PGVTT) y RF09 (Certificado PDF).", "CU06: Registro y Verificación de Donación; CU07: Emisión de Certificado PDF.", "donaciones_registradas, detalle_donacion_especie, certificados_donacion, bitacora_transparencia.", "CP-07, CP-08, CP-09"],
            ["Déficit de voluntarios y desorden en horarios, cupos y perfiles requeridos.", "OE1, OE4", "Propuesta de Valor / Aliados Clave", "RF05 (Convocatorias voluntariado) y RF06 (Postulación y cupos).", "CU08: Creación de Convocatoria; CU09: Postulación y Agendamiento de Voluntario.", "convocatorias_voluntariado, habilidades_requeridas, postulaciones_voluntario.", "CP-10, CP-11"],
            ["Ausencia de indicadores de impacto social y métricas por ODS para rendir cuentas.", "OE5, OE6", "Fuentes de Financiación (RSE) / Propuesta de Valor", "RF10 (Tablero de impacto por ODS) y RF12 (Gobernanza SuperAdmin).", "CU10: Consulta de Indicadores de Impacto y Auditoría del Sistema.", "ods_objetivos, campanas_ods, donaciones_registradas, auditoria_accesos.", "CP-12, CP-15"]
        ],
        "note": "Nota. Elaboración propia integrando la metodología RUP con el Modelo de Negocio Canvas."
    }),
    ("TABLE", {
        "title": "Tabla E2. Matriz de Control de Acceso Basado en Roles (RBAC) implementada en el backend y frontend del MVP",
        "headers": ["Módulo / Operación del Sistema", "Visitante (No Autenticado)", "Donante", "Voluntario", "Administrador OSAL", "SuperAdmin Sistema"],
        "rows": [
            ["Explorar mapa interactivo, directorio de OSAL y causas por ODS", "Permitido (Lectura)", "Permitido (Lectura)", "Permitido (Lectura)", "Permitido (Lectura)", "Permitido (Total)"],
            ["Registrar cuenta y aceptar política Habeas Data (Ley 1581)", "Permitido (Creación)", "Ya registrado", "Ya registrado", "Permitido (Registro OSAL)", "Permitido (Total)"],
            ["Publicar y editar campañas y necesidades de recursos (RF04)", "Denegado", "Denegado", "Denegado", "Permitido (Su propia OSAL)", "Permitido (Auditoría)"],
            ["Registrar donación en dinero o en especie (RF07)", "Redirige a Login", "Permitido (Creación)", "Permitido (Creación)", "Lectura", "Permitido (Auditoría)"],
            ["Verificar recepción de donación y actualizar meta (RF08)", "Denegado", "Denegado", "Denegado", "Permitido (Su propia OSAL)", "Permitido (Total)"],
            ["Descargar certificado tributario de donación en PDF (RF09)", "Denegado", "Permitido (Sus aportes)", "Denegado", "Permitido (Emitidos por su OSAL)", "Permitido (Total)"],
            ["Crear convocatorias de voluntariado y aprobar cupos (RF05)", "Denegado", "Denegado", "Denegado", "Permitido (Su propia OSAL)", "Permitido (Auditoría)"],
            ["Postularse a convocatorias de voluntariado activas (RF06)", "Redirige a Login", "Permitido", "Permitido (Creación)", "Lectura", "Permitido (Auditoría)"],
            ["Aprobar validación legal de nuevas OSAL y parámetros (RF12)", "Denegado", "Denegado", "Denegado", "Denegado", "Exclusivo SuperAdmin"]
        ],
        "note": "Nota. Restricciones aplicadas mediante decoradores @jwt_required() en Flask y Guards de ruta en Angular."
    }),

    # =========================================================================
    # ANEXO F
    # =========================================================================
    ("H2", "Anexo F. Diagramas de arquitectura, diseño y diccionario de datos en 5FN"),
    ("P", "El diseño arquitectónico y de datos del MVP se compone de la vista de capas (Frontend SPA en Angular 17, API REST en Python/Flask dividida en seis Blueprints y motor relacional SQLAlchemy ORM) y del esquema relacional normalizado hasta la Quinta Forma Normal (5FN) (véase Figura 7 en la Sección 5.4.3). En la Tabla F1 se presenta el Diccionario de Datos Maestro de las 34 tablas canónicas implementadas en el archivo backend/app/models/__init__.py."),
    ("TABLE", {
        "title": "Tabla F1. Diccionario de datos maestro de las 34 tablas normalizadas en Quinta Forma Normal (5FN) del sistema Conexión Solidaria",
        "headers": ["N.°", "Nombre de la Tabla SQL", "Dominio Funcional", "Clave Primaria (PK)", "Claves Foráneas (FK) y Atributos Principales"],
        "rows": [
            ["01", "paises", "1. Catálogos Geográficos", "id", "codigo_iso (UNIQUE), nombre (Colombia)."],
            ["02", "departamentos", "1. Catálogos Geográficos", "id", "pais_id (FK -> paises.id), codigo_dane, nombre (Cundinamarca)."],
            ["03", "municipios", "1. Catálogos Geográficos", "id", "departamento_id (FK -> departamentos.id), codigo_dane, nombre, provincia (Sabana Centro / Almeidas), latitud, longitud."],
            ["04", "tipos_documento", "1. Catálogos de Identidad", "id", "codigo (CC, NIT, CE, TI), descripcion."],
            ["05", "tipos_contacto", "1. Catálogos de Identidad", "id", "nombre (Teléfono Móvil, WhatsApp, Correo Electrónico, Sitio Web)."],
            ["06", "roles_sistema", "1. Catálogos de Seguridad", "id", "codigo (SUPERADMIN, ADMIN_OSAL, DONANTE, VOLUNTARIO, VISITANTE), descripcion."],
            ["07", "tipos_osal", "2. Catálogos Institucionales", "id", "nombre (Fundación, Asociación, Corporación), marco_normativo."],
            ["08", "estados_validacion_osal", "2. Catálogos Institucionales", "id", "codigo (PENDIENTE, VERIFICADA, RECHAZADA, SUSPENDIDA), descripcion."],
            ["09", "tipos_documento_legal", "2. Catálogos Institucionales", "id", "codigo (RUT_DIAN, CAMARA_COMERCIO, CEDULA_REP_LEGAL, ESTATUTOS), obligatorio."],
            ["10", "ods_objetivos", "2. Marco Social ODS", "id", "numero_ods (1, 2, 3, 4, 9, 10, 11, 15, 17), nombre, descripcion, color_hex."],
            ["11", "categorias_causa", "2. Marco Social ODS", "id", "nombre (Adulto Mayor, Protección Animal, Primera Infancia, Medio Ambiente, etc.), icono."],
            ["12", "unidades_medida", "2. Catálogos Operativos", "id", "codigo (COP, KG, UNIDAD, PAQUETE, KIT, LITRO, HORA), descripcion."],
            ["13", "usuarios", "3. Núcleo Usuarios y RBAC", "id", "tipo_documento_id (FK), numero_documento, nombres, apellidos, email (UNIQUE), activo, acepta_tratamiento_datos (Ley 1581), fecha_aceptacion_datos."],
            ["14", "credenciales_seguridad", "3. Núcleo Usuarios y RBAC", "id", "usuario_id (FK UNIQUE -> usuarios.id), password_hash (PBKDF2-SHA256), ultimo_cambio, intentos_fallidos."],
            ["15", "usuarios_roles", "3. Núcleo Usuarios y RBAC", "id", "usuario_id (FK -> usuarios.id), rol_id (FK -> roles_sistema.id), fecha_asignacion (Tabla puente 5FN)."],
            ["16", "contactos_usuario", "3. Núcleo Usuarios y RBAC", "id", "usuario_id (FK -> usuarios.id), tipo_contacto_id (FK -> tipos_contacto.id), valor, principal."],
            ["17", "sesiones_token", "3. Núcleo Usuarios y RBAC", "id", "usuario_id (FK -> usuarios.id), jti_token (UNIQUE), fecha_emision, fecha_expiracion, revocado."],
            ["18", "auditoria_accesos", "3. Núcleo Usuarios y RBAC", "id", "usuario_id (FK -> usuarios.id), accion, ip_origen, user_agent, fecha_evento."],
            ["19", "fundaciones_osal", "4. Gestión Institucional OSAL", "id", "usuario_admin_id (FK), tipo_osal_id (FK), estado_validacion_id (FK), nit (UNIQUE), nombre_oficial, sigla, mision, reseña, acepta_tratamiento_datos, fecha_aceptacion_datos."],
            ["20", "sedes_osal", "4. Gestión Institucional OSAL", "id", "osal_id (FK -> fundaciones_osal.id), municipio_id (FK -> municipios.id), direccion_vereda, es_rural, latitud, longitud, es_principal."],
            ["21", "contactos_osal", "4. Gestión Institucional OSAL", "id", "osal_id (FK -> fundaciones_osal.id), tipo_contacto_id (FK -> tipos_contacto.id), valor, publico."],
            ["22", "representantes_osal", "4. Gestión Institucional OSAL", "id", "osal_id (FK -> fundaciones_osal.id), tipo_documento_id (FK), numero_documento, nombre_completo, cargo, vigente."],
            ["23", "documentos_legales_osal", "4. Gestión Institucional OSAL", "id", "osal_id (FK -> fundaciones_osal.id), tipo_doc_legal_id (FK), url_archivo, hash_sha256, verificado, fecha_verificacion."],
            ["24", "osal_ods_alineacion", "4. Gestión Institucional OSAL", "id", "osal_id (FK -> fundaciones_osal.id), ods_id (FK -> ods_objetivos.id), nivel_prioridad (Tabla puente 5FN)."],
            ["25", "campanas_sociales", "5. Operación Transaccional", "id", "osal_id (FK -> fundaciones_osal.id), categoria_id (FK -> categorias_causa.id), titulo, descripcion, fecha_inicio, fecha_fin, estado."],
            ["26", "campanas_ods", "5. Operación Transaccional", "id", "campana_id (FK -> campanas_sociales.id), ods_id (FK -> ods_objetivos.id) (Tabla puente 5FN)."],
            ["27", "necesidades_recurso", "5. Operación Transaccional", "id", "campana_id (FK -> campanas_sociales.id), unidad_medida_id (FK), tipo_recurso (DINERO / ESPECIE), titulo_necesidad, cantidad_meta, cantidad_alcanzada, urgencia, es_emergencia."],
            ["28", "donaciones_registradas", "5. Operación Transaccional", "id", "necesidad_id (FK -> necesidades_recurso.id), donante_usuario_id (FK -> usuarios.id), codigo_trazabilidad (UNIQUE), tipo_aporte, monto_dinero, cantidad_especie, estado (PENDIENTE / CONFIRMADA), fecha_registro, fecha_confirmacion."],
            ["29", "detalle_donacion_especie", "5. Operación Transaccional", "id", "donacion_id (FK UNIQUE -> donaciones_registradas.id), descripcion_insumos, estado_conservacion, modalidad_entrega, punto_acopio."],
            ["30", "certificados_donacion", "5. Operación Transaccional", "id", "donacion_id (FK UNIQUE -> donaciones_registradas.id), numero_certificado (UNIQUE), hash_verificacion_sha256, fecha_emision, normativa_aplicada (Art. 125 E.T.)."],
            ["31", "convocatorias_voluntariado", "5. Operación Transaccional", "id", "osal_id (FK -> fundaciones_osal.id), campana_id (FK), titulo, descripcion_actividades, fecha_jornada, horario, modalidad, cupos_totales, cupos_disponibles, estado."],
            ["32", "habilidades_requeridas", "5. Operación Transaccional", "id", "convocatoria_id (FK -> convocatorias_voluntariado.id), nombre_habilidad, nivel_requerido (Tabla 5FN)."],
            ["33", "postulaciones_voluntario", "5. Operación Transaccional", "id", "convocatoria_id (FK -> convocatorias_voluntariado.id), voluntario_usuario_id (FK -> usuarios.id), disponibilidad_confirmada, mensaje_motivacion, horas_comprometidas, estado, fecha_postulacion."],
            ["34", "bitacora_transparencia", "5. Operación Transaccional", "id", "osal_id (FK -> fundaciones_osal.id), entidad_afectada, registro_id, descripcion_publica, hash_integridad, fecha_publicacion."]
        ],
        "note": "Nota. La totalidad de las 34 tablas se instancia y valida automáticamente al inicializar el backend (backend/app/models/__init__.py)."
    }),

    # =========================================================================
    # ANEXO G
    # =========================================================================
    ("H2", "Anexo G. Fragmentos de código relevantes"),
    ("P", "A continuación, se presentan tres fragmentos representativos del código fuente del Producto Mínimo Viable que evidencian la implementación técnica de: (1) el modelo relacional en 5FN con cumplimiento de la Ley 1581 de 2012 en SQLAlchemy; (2) el protocolo de verificación de donaciones y generación de certificados PDF con hash criptográfico SHA-256 en Flask; y (3) el cálculo en tiempo real de indicadores de impacto por ODS."),

    ("P_BOLD", "Fragmento G1. Modelo relacional con auditoría de Ley 1581 de 2012 (backend/app/models/__init__.py)"),
    ("CODE", """class FundacionOSAL(db.Model):
    __tablename__ = 'fundaciones_osal'
    id = db.Column(db.Integer, primary_key=True)
    usuario_admin_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    tipo_osal_id = db.Column(db.Integer, db.ForeignKey('tipos_osal.id'), nullable=False)
    estado_validacion_id = db.Column(db.Integer, db.ForeignKey('estados_validacion_osal.id'), nullable=False)
    nit = db.Column(db.String(30), unique=True, nullable=False)
    nombre_oficial = db.Column(db.String(180), nullable=False)
    sigla = db.Column(db.String(40), nullable=True)
    mision = db.Column(db.Text, nullable=False)
    acepta_tratamiento_datos = db.Column(db.Boolean, default=True, nullable=False)
    fecha_aceptacion_datos = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    verificada_en = db.Column(db.DateTime, nullable=True)"""),

    ("P_BOLD", "Fragmento G2. Verificación PGVTT de donación y generación de certificado PDF con Hash SHA-256 (backend/app/blueprints/donaciones.py)"),
    ("CODE", """@donaciones_bp.route('/<int:donacion_id>/confirmar', methods=['POST'])
def confirmar_donacion(donacion_id):
    donacion = DonacionRegistrada.query.get_or_404(donacion_id)
    if donacion.estado == 'CONFIRMADA':
        return jsonify({'mensaje': 'La donación ya se encuentra confirmada'}), 200
    donacion.estado = 'CONFIRMADA'
    donacion.fecha_confirmacion = datetime.utcnow()
    necesidad = NecesidadRecurso.query.get(donacion.necesidad_id)
    if necesidad:
        aporte = donacion.monto_dinero if donacion.tipo_aporte == 'DINERO' else donacion.cantidad_especie
        necesidad.cantidad_alcanzada = float(necesidad.cantidad_alcanzada or 0) + float(aporte or 0)
    semilla_hash = f"{donacion.codigo_trazabilidad}-{donacion.id}-{donacion.fecha_confirmacion.isoformat()}"
    hash_sha256 = hashlib.sha256(semilla_hash.encode('utf-8')).hexdigest()[:32].upper()
    certificado = CertificadoDonacion(
        donacion_id=donacion.id,
        numero_certificado=f"CERT-RTE-2026-{donacion.id:04d}",
        hash_verificacion_sha256=hash_sha256
    )
    db.session.add(certificado)
    db.session.commit()
    return jsonify({'mensaje': 'Donación verificada y certificado emitido', 'hash': hash_sha256}), 200"""),

    ("P_BOLD", "Fragmento G3. Cálculo de indicadores de cobertura e impacto por ODS (backend/app/blueprints/dashboard.py)"),
    ("CODE", """@dashboard_bp.route('/metricas', methods=['GET'])
def obtener_metricas():
    necesidades = NecesidadRecurso.query.all()
    coberturas = [
        min(100.0, (float(n.cantidad_alcanzada or 0) / float(n.cantidad_meta)) * 100.0)
        for n in necesidades if float(n.cantidad_meta or 0) > 0
    ]
    tasa_cobertura_pct = round(sum(coberturas) / len(coberturas), 1) if coberturas else 0.0
    impacto_por_ods = []
    for ods in ODSObjetivo.query.order_by(ODSObjetivo.numero_ods).all():
        num_osal = OSALODSAlineacion.query.filter_by(ods_id=ods.id).count()
        num_campanas = CampanaODS.query.filter_by(ods_id=ods.id).count()
        impacto_por_ods.append({
            'numero_ods': ods.numero_ods, 'nombre': ods.nombre,
            'osal_vinculadas': num_osal, 'campanas_activas': num_campanas
        })
    return jsonify({'tasa_cobertura_necesidades_pct': tasa_cobertura_pct, 'impacto_por_ods': impacto_por_ods}), 200"""),

    # =========================================================================
    # ANEXO H
    # =========================================================================
    ("H2", "Anexo H. Capturas de pantalla del MVP"),
    ("P", "Además de las cuatro vistas principales ya insertadas en la Sección 5.4.5 (Figuras 8 a 11: Mapa Interactivo, Necesidades y Donaciones, Convocatorias de Voluntariado y Tablero de Impacto por ODS), a continuación se presentan las ocho capturas adicionales (Figuras H1 a H8) que completan la evidencia visual de las doce pantallas operativas del MVP Conexión Solidaria."),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h04_wizard_paso1.png",
        "caption": "Figura H1. Asistente de Registro de OSAL - Paso 1: Identidad Institucional y Datos Jurídicos (NIT y Tipo de Entidad)",
        "note": "Nota. Captura tomada del módulo de registro de organizaciones (/registro-osal) del MVP."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h05_wizard_paso3_habeas.png",
        "caption": "Figura H2. Asistente de Registro de OSAL - Paso 3: Alineación con los 9 ODS y Consentimiento Expreso Ley 1581 de 2012",
        "note": "Nota. Evidencia la validación obligatoria de protección de datos personales Habeas Data antes de habilitar el registro."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h06_login_roles.png",
        "caption": "Figura H3. Interfaz de Autenticación Segura JWT y Selección de Acceso por Roles del Sistema (RBAC)",
        "note": "Nota. Pantalla de inicio de sesión (/login) con validación criptográfica de credenciales."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h03_publicar_campana_unidades.png",
        "caption": "Figura H4. Interfaz de Publicación de Campañas y Necesidades de Recursos con Unidades de Medida Estandarizadas",
        "note": "Nota. Permite a las OSAL publicar requerimientos en dinero o especie vinculados a los ODS."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h07_resumen_voluntario.png",
        "caption": "Figura H5. Panel de Gestión de Convocatorias de Voluntariado y Resumen de Postulaciones Ciudadanas",
        "note": "Nota. Muestra las vacantes activas, habilidades requeridas y control automático de cupos disponibles."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h09_donaciones_transaccional.png",
        "caption": "Figura H6. Panel de Trazabilidad Transaccional de Donaciones (Protocolo PGVTT) y Confirmación por la OSAL",
        "note": "Nota. Muestra el estado verificado de los aportes, el código único de seguimiento y el enlace al soporte tributario."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h10_certificado_pdf.png",
        "caption": "Figura H7. Vista del Certificado Tributario de Donación en PDF Generado Dinámicamente con Hash SHA-256",
        "note": "Nota. Documento PDF emitido por el motor ReportLab con datos de la OSAL, donante, valor y sello criptográfico."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\capturas_mvp\fig_h12_superadmin_parametros.png",
        "caption": "Figura H8. Panel de Gobernanza SuperAdmin: Validación Documental de OSAL, Auditoría y Catálogos Maestros",
        "note": "Nota. Permite verificar fundaciones, auditar eventos de seguridad y administrar los 18 municipios y 9 ODS."
    }),

    # =========================================================================
    # ANEXO I
    # =========================================================================
    ("H2", "Anexo I. Casos de prueba y resultados de rendimiento"),
    ("P", "Complementando la matriz de quince casos de prueba presentada en la Tabla 16 (Sección 5.5.2), la Tabla I1 reporta las mediciones empíricas de latencia HTTP (en milisegundos) y peso de transferencia de datos (en kilobytes) obtenidas sobre los endpoints principales de la API REST durante las pruebas de validación para entornos rurales de baja conectividad (RNF01)."),
    ("TABLE", {
        "title": "Tabla I1. Resultados de las pruebas de rendimiento, latencia HTTP y peso de carga útil (Payload JSON/PDF) del MVP",
        "headers": ["Endpoint Evaluado (API REST Flask)", "Método HTTP", "Latencia Media (ms)", "Latencia P95 (ms)", "Tamaño Payload (KB)", "Umbral Rural RNF01", "Dictamen"],
        "rows": [
            ["/api/osal/ (Directorio y Mapa Sabana)", "GET", "18,4 ms", "29,1 ms", "4,85 KB", "< 200 ms / < 15 KB", "CUMPLE HOLGADAMENTE"],
            ["/api/osal/catalogos (18 Municipios y 9 ODS)", "GET", "14,2 ms", "21,6 ms", "3,92 KB", "< 200 ms / < 15 KB", "CUMPLE HOLGADAMENTE"],
            ["/api/necesidades/ (Catálogo de causas activas)", "GET", "19,7 ms", "33,4 ms", "5,64 KB", "< 200 ms / < 15 KB", "CUMPLE HOLGADAMENTE"],
            ["/api/voluntariado/ (Convocatorias y cupos)", "GET", "16,9 ms", "27,8 ms", "4,18 KB", "< 200 ms / < 15 KB", "CUMPLE HOLGADAMENTE"],
            ["/api/dashboard/metricas (KPIs e Impacto ODS)", "GET", "22,1 ms", "38,5 ms", "7,42 KB", "< 200 ms / < 15 KB", "CUMPLE HOLGADAMENTE"],
            ["/api/auth/login (Autenticación JWT + PBKDF2)", "POST", "41,8 ms", "56,4 ms", "0,95 KB", "< 200 ms / < 15 KB", "CUMPLE HOLGADAMENTE"],
            ["/api/donaciones/<id>/certificado (Emisión PDF)", "GET", "34,6 ms", "49,2 ms", "2,61 KB (PDF)", "< 200 ms / < 25 KB", "CUMPLE HOLGADAMENTE"]
        ],
        "note": "Nota. Pruebas ejecutadas sobre el servidor backend Python 3.12 / Flask conectado a la base de datos en 5FN poblada con datos reales."
    }),

    # =========================================================================
    # ANEXO J
    # =========================================================================
    ("H2", "Anexo J. Presupuesto detallado y proyecciones financieras"),
    ("P", "En la Tabla J1 se detalla el desglose técnico unitario del presupuesto de inversión inicial (CAPEX intelectual y líquido) y de los costos operativos anuales (OPEX) que sustentan el flujo de caja proyectado en la Sección 5.6."),
    ("TABLE", {
        "title": "Tabla J1. Desglose unitario de inversión inicial (CAPEX) y costos operativos anuales del Año 1 (en pesos colombianos COP)",
        "headers": ["Categoría Presupuestal", "Ítem / Concepto Detallado", "Unidad", "Cantidad", "Valor Unitario (COP)", "Subtotal Anual (COP)", "Tipo de Aporte"],
        "rows": [
            ["1. CAPEX Intelectual", "Ingeniería de software RUP, BD 5FN y desarrollo MVP (2 cofundadores)", "Horas", "640", "$22.500", "$14.400.000", "Especie (Cofundadores)"],
            ["1. CAPEX Intelectual", "Uso y depreciación de 2 equipos portátiles y conectividad durante desarrollo", "Meses", "4", "$450.000", "$1.800.000", "Especie (Cofundadores)"],
            ["2. CAPEX Líquido (Año 0)", "Derechos de inscripción ESAL Cámara de Comercio, RUT y libros electrónicos", "Global", "1", "$650.000", "$650.000", "Efectivo Semilla"],
            ["2. CAPEX Líquido (Año 0)", "Configuración inicial servidor cloud, dominio .org.co y capital de trabajo", "Global", "1", "$1.600.000", "$1.600.000", "Efectivo Semilla"],
            ["3. OPEX Tecnológico (Año 1)", "Servidor Cloud Web Service (Python/Flask) + Frontend CDN", "Meses", "12", "$95.000", "$1.140.000", "Operativo Recurrente"],
            ["3. OPEX Tecnológico (Año 1)", "Base de datos relacional gestionada en 5FN + Backups diarios y Storage", "Meses", "12", "$105.000", "$1.260.000", "Operativo Recurrente"],
            ["3. OPEX Tecnológico (Año 1)", "Renovación anual de dominio institucional .org.co y certificados SSL/TLS", "Anual", "1", "$180.000", "$180.000", "Operativo Recurrente"],
            ["4. OPEX Operación y Soporte", "Coordinación de verificación documental OSAL, soporte y mantenimiento", "Meses", "12", "$550.000", "$6.600.000", "Operativo Recurrente"],
            ["5. OPEX Marketing y Campo", "Pauta digital segmentada, material QR y transporte a veredas de la Sabana", "Meses", "12", "$150.000", "$1.800.000", "Operativo Recurrente"],
            ["6. OPEX Legal y Contable", "Honorarios Contador Público (cierres, estados financieros y declaración RTE)", "Anual", "1", "$2.400.000", "$2.400.000", "Operativo Recurrente"],
            ["6. OPEX Legal y Contable", "Renovación anual matrícula ESAL, gastos bancarios y papelería legal", "Anual", "1", "$720.000", "$720.000", "Operativo Recurrente"]
        ],
        "note": "Nota. Total CAPEX Valorizado: $18.450.000 COP ($16.200.000 en especie + $2.250.000 en efectivo). Total OPEX Año 1: $14.100.000 COP."
    }),

    # =========================================================================
    # ANEXO K
    # =========================================================================
    ("H2", "Anexo K. Cronograma de implementación"),
    ("P", "En la Tabla K1 se presenta el cronograma detallado de ejecución de las dieciséis semanas del proyecto bajo las cuatro fases de la metodología RUP (Inicio, Elaboración, Construcción y Transición), el cual complementa el plan de operación mensual posdespliegue presentado en la Tabla 20 (Sección 5.8.2)."),
    ("TABLE", {
        "title": "Tabla K1. Cronograma ejecutado de 16 semanas para la investigación, diseño, desarrollo del MVP y estructuración del negocio",
        "headers": ["Fase RUP / Emprendimiento", "Actividad Específica Ejecutada", "Semanas", "Responsables", "Estado Final"],
        "rows": [
            ["Fase 1: Inicio (Inception)", "1.1. Revisión sistemática de literatura (16 artículos) y análisis de datos DANE/AFE.", "Sem 1 - 2", "Angélica Olier & Oscar Robayo", "100 % Completado"],
            ["Fase 1: Inicio (Inception)", "1.2. Trabajo de campo en fundaciones rurales y levantamiento de actores, RF y RNF.", "Sem 2 - 3", "Angélica Olier & Oscar Robayo", "100 % Completado"],
            ["Fase 2: Elaboración (Elaboration)", "2.1. Estructuración del Modelo de Negocio Canvas y estrategia de sostenibilidad.", "Sem 4", "Angélica Olier & Oscar Robayo", "100 % Completado"],
            ["Fase 2: Elaboración (Elaboration)", "2.2. Diseño de arquitectura LBRSA, casos de uso CU01-CU10 y prototipos UI/UX.", "Sem 5", "UI/UX: Angélica | Arq: Oscar", "100 % Completado"],
            ["Fase 2: Elaboración (Elaboration)", "2.3. Modelado relacional de base de datos normalizada hasta 5FN (34 tablas).", "Sem 6", "Oscar Robayo & Angélica Olier", "100 % Completado"],
            ["Fase 3: Construcción (Construction)", "3.1. Codificación del backend API REST en Python/Flask y modelos SQLAlchemy.", "Sem 7 - 9", "Oscar Robayo", "100 % Completado"],
            ["Fase 3: Construcción (Construction)", "3.2. Desarrollo del frontend en Angular 17, mapa Leaflet y asistente en 3 pasos.", "Sem 8 - 11", "Angélica Olier & Oscar Robayo", "100 % Completado"],
            ["Fase 3: Construcción (Construction)", "3.3. Integración de protocolo PGVTT, Ley 1581, certificados PDF y dashboard ODS.", "Sem 11 - 12", "Oscar Robayo & Angélica Olier", "100 % Completado"],
            ["Fase 4: Transición (Transition)", "4.1. Ejecución de los 15 casos de prueba QA (CP-01 a CP-15) y pruebas de latencia.", "Sem 13 - 14", "Angélica Olier & Oscar Robayo", "100 % Completado"],
            ["Fase 5: Cierre Documental", "5.1. Estructuración de planes organizacional, operativo, marketing, financiero y riesgos.", "Sem 15", "Angélica Olier & Oscar Robayo", "100 % Completado"],
            ["Fase 5: Cierre Documental", "5.2. Consolidación del informe final en normas APA 7 y verificación de anexos A-L.", "Sem 16", "Angélica Olier & Oscar Robayo", "100 % Completado"]
        ],
        "note": "Nota. Elaboración propia conforme al plan de trabajo del proyecto de grado."
    }),

    # =========================================================================
    # ANEXO L
    # =========================================================================
    ("H2", "Anexo L. Otros soportes pertinentes (Guía de ejecución y certificado tributario)"),
    ("P", "Para efectos de verificación técnica y reproducción local del Producto Mínimo Viable por parte de los jurados evaluadores, en la Tabla L1 se especifican los comandos de inicialización del backend y del frontend, así como las credenciales de prueba preconfiguradas para cada uno de los roles del sistema. Asimismo, en el directorio docs/capturas_mvp/Certificado_Tributario_DIAN_Ejemplo.pdf del repositorio del proyecto se adjunta un ejemplar íntegro del Certificado de Donación en formato PDF generado automáticamente por el endpoint /api/donaciones/1/certificado conforme a los artículos 125-1 y 125-2 del Estatuto Tributario."),
    ("TABLE", {
        "title": "Tabla L1. Credenciales de prueba por rol (RBAC) y comandos de puesta en marcha del MVP Conexión Solidaria",
        "headers": ["Rol del Sistema", "Correo Electrónico de Prueba", "Contraseña", "Ruta / Vista Principal a Verificar"],
        "rows": [
            ["Superadministrador del Sistema", "admin@conexionsolidaria.org", "AdminSolidario2026*", "/superadmin (Validación OSAL, auditoría y parámetros)"],
            ["Administrador OSAL (FARASAN Cogua)", "contacto@farasancogua.org", "Farasan2026*", "/dashboard (Gestión de campañas, confirmación de donaciones y KPIs)"],
            ["Donante Ciudadano / Corporativo", "donante@correo.com", "Donante2026*", "/necesidades y /dashboard (Reporte de aporte y descarga de PDF)"],
            ["Voluntario Universitario", "voluntario@ucundinamarca.edu.co", "Voluntario2026*", "/voluntariado (Postulación a brigadas veredales activas)"],
            ["Visitante Público (Sin autenticación)", "Acceso libre sin login", "No requiere", "/mapa (Exploración georreferenciada por municipio y ODS)"]
        ],
        "note": "Nota. Para iniciar el backend: ejecutar 'python run.py' en la carpeta backend/ (puerto 5000). Para iniciar el frontend: ejecutar 'npx ng serve --port 4200' en la carpeta frontend/ (http://localhost:4200)."
    })
]
