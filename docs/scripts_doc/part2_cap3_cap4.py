# -*- coding: utf-8 -*-
"""
Contenido académico completo de los Capítulos 3 y 4 del documento final de grado:
CONEXIÓN SOLIDARIA. TECNOLOGÍA PARA EL CAMBIO SOCIAL
Autores: Angélica Rosa Olier Quiroga y Oscar Giovanni Robayo Olaya
Universidad de Cundinamarca - Extensión Chía (2026)
"""

CAPITULO_3_Y_4 = [
    # =========================================================================
    # CAPÍTULO 3. DIAGNÓSTICO Y ESTUDIO DE MERCADO
    # =========================================================================
    ("H1", "CAPÍTULO 3. DIAGNÓSTICO Y ESTUDIO DE MERCADO"),

    ("H2", "3.1. Contexto de las organizaciones sociales participantes"),
    ("P", "El trabajo diagnóstico se enfocó en las Organizaciones Sin Ánimo de Lucro (OSAL) que operan en zonas rurales y municipales de la Sabana Centro y Sabana Norte de Cundinamarca. A pesar de que los cascos urbanos de municipios como Chía, Cajicá o Zipaquirá han tenido un gran crecimiento comercial e industrial, en sus veredas y sectores periféricos siguen operando pequeñas fundaciones que atienden a población vulnerable con recursos muy limitados."),

    ("H3", "3.1.1. Caracterización de las organizaciones y Análisis de Participación"),
    ("P", "Siguiendo el diseño metodológico mixto y el Análisis de Participación documentado en el portafolio investigativo del proyecto, la caracterización se realizó en dos niveles complementarios. En primer lugar, se analizaron en profundidad y se les aplicó la encuesta diagnóstica de 14 ítems a cuatro fundaciones reales de la región, cuyas misiones institucionales reflejan la diversidad del tercer sector local:"),
    ("UL", [
        "1. Fundación Machetá Casa de los Abuelos Campesinos (Machetá - Contacto: Inés Camelo, 3112089943, abuelitosmacheta@gmail.com): Trabaja para ofrecer a los adultos mayores del campo una vejez con calidad de vida y respeto por su dignidad humana, proporcionando a los residentes una vivienda digna, atención psicosocial y física, alimentación balanceada, cuidados médicos con personal especializado y actividades sociales, culturales, recreativas y deportivas con el fin de mantenerlos activos física y mentalmente, todo esto como un programa piloto de atención a este segmento de la población. La fundación invita a participar de las diferentes actividades pensadas en el desarrollo permanente de esta obra, honrando la vida de quienes sembraron nuestra tierra y merecen visibilidad por parte de una Colombia que todos los días construye solidaridad con acciones como ésta.",
        "2. Fundación Campamentos de Vida Nueva (Simijaca - Contacto: Padre César, 3107173205, www.campamentosdevidanueva.org): Realiza su misión en dos campos específicos: en localidades donde se conforman las llamadas Comunidades SHEMA y a través de la llamada Ruta campamentaria, la cual consiste en un servicio de internado para quienes padecen adicciones y dificultades psicoemocionales y desean por propia voluntad comenzar un proceso de recuperación para abrazar una vida nueva. Su propósito es brindar a las personas excluidas y marginadas de la sociedad o en condiciones de tribulaciones especiales en su vida un proceso de acogida, acompañamiento y formación integral permanente con el fin de contribuir a la restauración de sus vidas y la recuperación de su dignidad humana.",
        "3. Fundación Patitas Campesinas (La Calera - Contacto: 3118854757, patitascampesinas@gmail.com, patitascampesinas.org): Su misión se basa en disminuir el maltrato animal en sus modalidades de abandono, negligencia, castigo físico y muerte (prácticas comunes en la zona rural) mediante campañas masivas de esterilización canina y felina, así como en el rescate y bienestar animal. Trabaja en la rehabilitación física y emocional de los caninos y felinos albergados (con el fin de entregar en adopción animales estables) y en contribuir con información que ayude a la construcción de una sociedad con más educación, consciencia y respeto hacia los animales, mediante la judicialización de casos violatorios de la ley de protección animal vigentes en el país en situaciones que atenten contra su integridad.",
        "4. Fundación Mis Gotitas de Amor (Cajicá - Contacto: 3133934744, misgotitasdeamor2022@gmail.com): Orientada a brindar una educación informal caracterizada por privilegiar un enfoque de apoyo temprano al desarrollo cognoscitivo, físico, social y emocional del niño(a) y familiarizar a los niños(as) de temprana edad con la instrucción organizada fuera del entorno familiar, en donde aprenden a mejorar su lenguaje y sus habilidades sociales, desarrollan sus destrezas de lógica y articulan sus procesos de reflexión a través de un aprendizaje visualmente estimulante y verbalmente variado. Se trata de asumir una pedagogía centrada en el placer de aprender que supere la enseñanza impuesta, exponiendo a los niños a conceptos alfabéticos y matemáticos y a la exploración del mundo que los rodea con actividades diseñadas para mejorar la motricidad, la interacción social, la autonomía y la preparación para la educación preescolar."
    ]),
    ("P", "En segundo lugar, a partir de esta línea base se parametrizaron cinco organizaciones referentes de la Sabana en la base de datos de producción para probar todos los módulos del MVP. La Tabla 6 resume los datos de estas organizaciones."),
    ("TABLE", {
        "title": "Tabla 6. Matriz de caracterización de las organizaciones sociales referentes en la Sabana Centro y Norte de Cundinamarca",
        "headers": ["Código / Sigla", "Organización y Municipio", "Línea de Acción / Objeto Social", "Población / Meta Atendida", "Situación Tecnológica y Operativa Diagnosticada"],
        "rows": [
            ["OSAL-01 (FARASAN)", "Fundación Hogar Geriátrico San Antonio (Cogua - Vereda Rodamontal)", "Cuidado integral, alimentación, alojamiento y salud primaria para el adulto mayor vulnerable.", "28 adultos mayores residentes en condición de abandono o pobreza extrema.", "Registros contables y de donaciones en cuadernos físicos; sin sitio web; uso esporádico de WhatsApp personal; alta necesidad de insumos médicos y pañales."],
            ["OSAL-02 (FUNHUELLAS)", "Fundación Huellas de la Sabana (Cajicá - Vereda Chuntame)", "Rescate, esterilización, rehabilitación veterinaria y adopción responsable de fauna callejera.", "Más de 85 caninos y felinos rescatados en albergue rural.", "Difusión reactiva en redes sociales sin métricas ni seguimiento; escasez recurrente de alimento concentrado y voluntarios para jornadas de limpieza y paseo."],
            ["OSAL-03 (ASOMAYOR)", "Asociación Semillas de Esperanza y Rehabilitación (Zipaquirá - Sector Rural San Jorge)", "Prevención de adicciones, apoyo psicosocial, comedores comunitarios y formación en oficios.", "45 jóvenes y familias campesinas y periféricas en vulnerabilidad.", "Ausencia de sistema de información; recepción de donaciones por voz a voz; dificultad para reclutar profesionales voluntarios (psicología y docencia)."],
            ["OSAL-04 (FUNDAULA)", "Fundación Aula Viva para la Primera Infancia (Chía - Vereda Fagua / Tíquiza)", "Refuerzo escolar, nutrición infantil, ludoteca rural y alfabetización digital básica.", "60 niños y niñas de primera infancia de familias trabajadoras rurales.", "Sin portal web ni directorio de necesidades; control de asistencia de voluntarios en hojas sueltas; requerimiento de kits escolares y equipos de cómputo."],
            ["OSAL-05 (CORPOJUAICA)", "Corporación Ambiental Guardianes de Juaica y el Páramo (Tabio / Tenjo - Sector Rural)", "Restauración ecológica de quebradas, vivero comunitario nativo y educación ambiental.", "Comunidades veredales de Tabio, Tenjo y Subachoque (ecosistemas altoandinos).", "Convocatorias de siembra difundidas por cadenas informales de mensajería; sin control previo de cupos de voluntarios ni inventario sistematizado de herramientas."]
        ],
        "note": "Nota. Elaboración propia a partir del trabajo de campo cualitativo (Olier & Robayo, 2025) y la matriz de caracterización territorial (Anexo C)."
    }),

    ("H3", "3.1.2. Poblaciones beneficiarias"),
    ("P", "Las organizaciones caracterizadas atienden de forma directa a grupos poblacionales de especial protección constitucional en el entorno rural cundinamarqués: adultos mayores sin red de apoyo familiar ni pensión (ODS 1, 2 y 3); niños, niñas y adolescentes de veredas con rezago escolar o inseguridad alimentaria (ODS 2 y 4); jóvenes en procesos de resocialización y superación de adicciones (ODS 3 y 10); comunidades campesinas vinculadas a la conservación de fuentes hídricas (ODS 11 y 15); y fauna doméstica en condición de abandono o maltrato.En conjunto, tan solo estas cinco entidades impactan de manera directa a más de 220 beneficiarios permanentes y de forma indirecta a sus núcleos familiares veredales."),

    ("H3", "3.1.3. Ubicación y ámbito de actuación"),
    ("P", "El ámbito geográfico de actuación del proyecto comprende dieciocho municipios de las provincias de Sabana Centro y Sabana Norte (Almeidas) en el departamento de Cundinamarca: Cajicá, Chía, Chocontá, Cogua, Gachancipá, Guatavita, Machetá, Manta, Nemocón, Sesquilé, Sopó, Suesca, Tabio, Tenjo, Tibirita, Tocancipá, Villapinzón y Zipaquirá. Este corredor se caracteriza por una dualidad territorial: mientras los ejes viales principales concentran parques industriales, zonas francas y campus universitarios con alta conectividad, las veredas montañosas donde se ubican las sedes operativas de las fundaciones presentan vías terciarias de difícil acceso, señal móvil intermitente y baja visibilidad ante el público urbano."),

    ("H2", "3.2. Identificación del grupo objetivo"),
    ("P", "Dado que Conexión Solidaria opera bajo un modelo de plataforma multilateral que conecta oferta y demanda de solidaridad social, el estudio de mercado segmenta e identifica cuatro grupos objetivo interdependientes (Buyer Personas), cuyas características y motivaciones definen el diseño funcional del servicio."),

    ("H3", "3.2.1. Organizaciones sociales beneficiarias"),
    ("P", "Constituyen el usuario beneficiario central de la plataforma. Corresponden a fundaciones, asociaciones y corporaciones sin ánimo de lucro legalmente constituidas (o en proceso de formalización documental) que operan en los municipios de Sabana Centro y Norte, con nóminas inferiores a diez personas, presupuesto anual limitado y carencia de portal web o software administrativo propio (AFE, 2018). Su perfil de usuario típico (Buyer Persona 1: Directora de Fundación Rural) corresponde a líderes comunitarios entre 35 y 65 años, con alta vocación social pero tiempo escaso y competencias digitales básicas, que requieren una interfaz intuitiva desde su teléfono móvil para publicar necesidades y recibir ayudas sin trámites complejos."),

    ("H3", "3.2.2. Donantes potenciales"),
    ("P", "Comprenden dos subsegmentos: (a) Personas naturales (ciudadanos residentes en las cabeceras urbanas de Chía, Cajicá, Zipaquirá, Sopó o Bogotá D.C., entre 25 y 60 años, empleados o profesionales independientes con ingresos medios y altos) que desean apoyar causas locales con dinero o bienes en especie (alimentos, medicamentos, ropa, materiales), pero que exigen verificar la existencia legal de la fundación y conocer el destino final de su aporte; y (b) Personas jurídicas (pequeñas, medianas y grandes empresas ubicadas en el corredor industrial de Tocancipá, Gachancipá, Zipaquirá y Chía) que buscan canalizar recursos de Responsabilidad Social Empresarial (RSE) hacia fundaciones verificadas que les expidan oportunamente el certificado de donación para el beneficio fiscal del Estatuto Tributario (Congreso de la República de Colombia, 1989, 2016)."),

    ("H3", "3.2.3. Voluntarios potenciales"),
    ("P", "Este segmento (Buyer Persona 3: Joven Universitario o Profesional Solidario) está integrado principalmente por estudiantes de educación superior (de instituciones con presencia en la región como la Universidad de Cundinamarca, Universidad de La Sabana, Universidad Militar Nueva Granada, UNIMINUTO, entre otras) y jóvenes profesionales entre 18 y 35 años que buscan oportunidades estructuradas para realizar voluntariado social, ambiental, logístico o profesional (horas de práctica social, brigadas de fin de semana o asesoría virtual), valorando la claridad en horarios, ubicación en mapa y certificación de su participación."),

    ("H3", "3.2.4. Aliados estratégicos y financiadores"),
    ("P", "Conforman el grupo de actores institucionales que viabilizan la sostenibilidad económica y operativa de Conexión Solidaria sin cobrar a las fundaciones beneficiarias: empresas patrocinadoras con presupuestos de RSE y marketing con causa, alcaldías municipales y secretarías de desarrollo social interesadas en contar con un directorio transparente del tercer sector local, universidades aliadas mediante semilleros y consultorios técnicos, y fondos nacionales o internacionales de cooperación para la inclusión digital (BID, 2020; Martínez et al., 2020)."),

    ("H2", "3.3. Diseño de los instrumentos de investigación"),
    ("P", "Para garantizar la rigurosidad del diagnóstico y evitar la transcripción en texto plano de cuestionarios extensos dentro del cuerpo del capítulo, los dos instrumentos digitales aplicados en línea mediante Google Forms se presentan a través de sus matrices técnicas de operacionalización de variables (Tablas 6A-1 y 6A-2) junto con la Ficha Técnica oficial del levantamiento (Tabla 6A) y las evidencias visuales de los formularios en el Anexo A:"),
    ("UL", [
        "Instrumento Digital 1 — Encuesta de percepción e interés sobre las organizaciones sociales y la plataforma Conexión Solidaria (Comunidad / Potenciales Donantes y Voluntarios): Formulario web estructurado en tres secciones y nueve preguntas cerradas, disponible en línea en https://forms.gle/FbrAEsHmz2sQWa4A6, difundido mediante invitación comunitaria en WhatsApp («Como parte de nuestro proyecto de grado de emprendimiento en Ingeniería de Sistemas de la Universidad de Cundinamarca, estamos formulando la creación de una fundación tecnológica orientada a entregar software gratuito para hacer sostenibles a las fundaciones sociales locales y rurales»), con el cual se recolectaron n = 170 respuestas válidas.",
        "Instrumento Digital 2 — Encuesta de diagnóstico para fundaciones y organizaciones sociales (OSAL): Formulario web estructurado en cinco secciones y catorce preguntas, disponible en línea en https://forms.gle/t9MoqpGDwrZzbntW7, aplicado a los líderes y representantes de las cuatro fundaciones diagnosticadas en la región (Gotitas de Amor en Cajicá, Casa de los Abuelos en Machetá, Campamentos de Nueva Vida en Simijaca y Patitas Campesinas en La Calera), complementado con entrevista semiestructurada y observación directa en campo."
    ]),
    ("TABLE", {
        "title": "Tabla 6A-1. Matriz de operacionalización del Instrumento 1: Encuesta a Comunidad, Potenciales Donantes y Voluntarios (https://forms.gle/FbrAEsHmz2sQWa4A6)",
        "headers": ["Sección del Formulario", "N.° y Pregunta Exacta del Instrumento", "Tipo de Control / Escala", "Opciones de Respuesta Parametrizadas", "Variable Analítica"],
        "rows": [
            ["Sección 1: Perfil General y Ubicación", "1. Rango de edad:", "Selección única (Radio button)", "Menor de 18 años | 18 a 25 años | 26 a 35 años | 36 a 50 años | Más de 50 años.", "Caracterización etaria del usuario solidario."],
            ["Sección 1: Perfil General y Ubicación", "2. Ocupación principal:", "Selección única con opción abierta", "Estudiante | Empleado(a) | Independiente / Emprendedor(a) | Desempleado(a) / En búsqueda de empleo | Otro (Retirado/a).", "Capacidad de aporte económico o de tiempo."],
            ["Sección 1: Perfil General y Ubicación", "3. ¿En qué municipio reside principalmente?", "Lista desplegable (Dropdown)", "Chía | Cajicá | Zipaquirá | Sopó | Tabio | Tenjo | Cota | Cogua | Nemocón | Tocancipá | Gachancipá | Bogotá D.C. | Otro municipio.", "Distribución territorial en la Sabana e influencia."],
            ["Sección 1: Perfil General y Ubicación", "4. ¿En qué tipo de zona reside?", "Selección única (Radio button)", "Urbana (Casco urbano / centro) | Rural / Periurbana (Vereda o sector campestre).", "Validación de contexto urbano vs. rural/veredal."],
            ["Sección 2: Conocimiento y Causas de Interés", "5. ¿Conoce fundaciones u organizaciones sociales activas en su municipio o entorno cercano?", "Selección única (Escala ordinal)", "Sí, conozco varias y sé qué actividades realizan | Conozco algunas de nombre, pero no sé en detalle sus actividades | Casi no tengo conocimiento de organizaciones locales | No conozco ninguna.", "Índice de visibilidad de las OSAL locales."],
            ["Sección 2: Conocimiento y Causas de Interés", "6. ¿Cuáles causas sociales o áreas de impacto despiertan mayor interés en usted?", "Casillas de verificación (Selección múltiple)", "Infancia y juventud | Adulto mayor | Cuidado y protección animal | Medio ambiente y sostenibilidad | Desarrollo comunitario y rural | Educación y formación técnica | Salud y bienestar general | Otro.", "Priorización de categorías y ODS en el catálogo."],
            ["Sección 3: Intención de Participación", "7. En el último año, ¿cómo ha participado o apoyado causas sociales?", "Casillas de verificación (Selección múltiple)", "Donaciones de dinero (únicas o recurrentes) | Donación de bienes materiales o insumos (ropa, alimentos, herramientas) | Voluntariado presencial (tiempo y mano de obra en campo) | Voluntariado profesional/remoto | Difusión de campañas en redes sociales | No he participado activamente.", "Hábitos reales de donación y voluntariado."],
            ["Sección 3: Intención de Participación", "8. ¿Qué motivación o condición considera indispensable para donar o hacer voluntariado en una fundación?", "Selección única (Factor determinante)", "Transparencia total en el uso de los fondos y recursos | Claridad en las actividades o tareas específicas que se van a realizar | Cercanía comunitaria o geográfica | Facilidad para realizar el aporte de forma digital.", "Requerimiento de confianza (PGVTT y hash SHA-256)."],
            ["Sección 3: Intención de Participación", "9. ¿Estaría dispuesto(a) a utilizar una plataforma web/móvil que centralice fundaciones locales para postularse a voluntariados o hacer donaciones directas?", "Selección única (Escala de adopción)", "Totalmente dispuesto(a) | Probablemente sí | Indeciso(a) | No me interesaría.", "Tasa de aceptación del MVP Conexión Solidaria."]
        ],
        "note": "Nota. Estructura extraída directamente del formulario oficial aplicado en Google Forms (https://forms.gle/FbrAEsHmz2sQWa4A6), cuyos resultados (n = 170) se analizan en la Sección 3.4.3."
    }),
    ("TABLE", {
        "title": "Tabla 6A-2. Matriz de operacionalización del Instrumento 2: Encuesta Diagnóstica de Fundaciones y Organizaciones Sociales (https://forms.gle/t9MoqpGDwrZzbntW7)",
        "headers": ["Sección del Formulario", "N.° y Pregunta Exacta del Instrumento", "Tipo de Control / Escala", "Opciones de Respuesta Parametrizadas", "Requerimiento del MVP Vinculado"],
        "rows": [
            ["Sección 1: Caracterización y Ubicación", "1. Nombre de la fundación u organización:", "Texto corto abierto", "Respuesta abierta nominal (identificación de la entidad social).", "Registro institucional OSAL (RF01)."],
            ["Sección 1: Caracterización y Ubicación", "2. ¿En qué municipio se encuentra la sede principal o base operativa de la organización?", "Lista desplegable (Dropdown)", "Chía | Cajicá | Zipaquirá | Sopó | Tabio | Tenjo | Cota | Cogua | Nemocón | Tocancipá | Gachancipá | Bogotá D.C. | Otro municipio.", "Georreferenciación municipal (RF03)."],
            ["Sección 1: Caracterización y Ubicación", "3. ¿Cuál es el entorno geográfico principal donde desarrollan sus actividades?", "Selección única (Radio button)", "Exclusivamente en casco urbano | Principalmente en zonas rurales / veredales | Mixto (tanto en veredas como en casco urbano) | Regional (en varios municipios de la Sabana).", "Arquitectura ligera para zonas rurales (RNF01)."],
            ["Sección 1: Caracterización y Ubicación", "4. Tipo de organización:", "Selección única", "Fundación comunitaria / de base local | Fundación independiente / filantrópica | Asociación rural / agropecuaria | Colectivo social sin personería jurídica formal | Otro.", "Tipología jurídica ESAL (RF01)."],
            ["Sección 1: Caracterización y Ubicación", "5. ¿A qué grupo o tipo de población atiende o beneficia principalmente su labor?", "Casillas de verificación (Selección múltiple)", "Primera infancia, niñez y adolescencia | Juventud | Adultos mayores / Tercera edad | Mujeres / Madres cabeza de familia | Familias y hogares en vulnerabilidad | Comunidades rurales/campesinas | Personas con discapacidad | Población migrante | Comunidad general | Animales en abandono o rescate.", "Alineación con categorías y 9 ODS (RF03, RF10)."],
            ["Sección 2: Gestión de Comunicaciones", "6. ¿A través de qué canales comunican habitualmente sus actividades, necesidades o convocatorias?", "Casillas de verificación (Selección múltiple)", "Redes sociales (Facebook, Instagram, TikTok, etc.) | Canales de mensajería (WhatsApp, Telegram) | Sitio web institucional | Medios comunitarios tradicionales (radio local, carteleras, perifoneo) | Correo electrónico | No contamos con un canal de comunicación continuo.", "Perfil web público gratuito (RF03)."],
            ["Sección 2: Gestión de Comunicaciones", "7. ¿Con qué frecuencia publican información sobre su labor?", "Selección única", "Diariamente | Varias veces a la semana | Quincenal o mensualmente | Solo cuando hay un evento o necesidad urgente.", "Módulo de campañas permanentes y urgentes (RF04, RF11)."],
            ["Sección 2: Gestión de Comunicaciones", "8. ¿Cómo perciben la respuesta y el compromiso del público ante sus publicaciones o llamados a participar?", "Escala lineal Likert (1 a 5)", "1 (Muy baja / Nula interacción) | 2 | 3 | 4 | 5 (Muy alta y constante respuesta).", "Visibilidad y alcance regional (RF03)."],
            ["Sección 2: Gestión de Comunicaciones", "9. ¿Miden o analizan de alguna forma el alcance o resultados de sus comunicaciones digitales?", "Selección única", "Sí, revisamos métricas básicas de redes sociales periódicamente | Solo revisamos comentarios y mensajes directamente | No analizamos métricas por falta de tiempo o herramientas especializadas.", "Tablero de métricas e impacto social (RF10)."],
            ["Sección 3: Mecanismos de Apoyo", "10. ¿Cómo recibe apoyo tu organización actualmente para sostenerse?", "Casillas de verificación (Selección múltiple)", "Donaciones económicas de personas naturales | Donaciones en especie / insumos (alimentos, insumos, ropa) | Subvenciones, convenios o fondos públicos | Alianzas con empresas privadas | Aporte voluntario no remunerado de miembros | Venta de productos o servicios propios.", "Modelo gratuito 0 % comisión (Canvas) y donaciones duales (RF07)."],
            ["Sección 4: Jerarquización de Dificultades", "11. Ordene los siguientes desafíos de su labor según su nivel de dificultad (donde 1 es el Mayor obstáculo y 5 el Menor):", "Matriz de jerarquización (1 Mayor a 5 Menor)", "Filas evaluadas: (a) Falta de recursos económicos; (b) Reclutar y retener voluntarios; (c) Baja visibilidad pública; (d) Carga administrativa; (e) Medir e informar impacto.", "Priorización de módulos del MVP (Sección 3.5.5)."],
            ["Sección 5: Validación de la Plataforma", "12. Si contaran con una plataforma gratuita diseñada para visibilizar sus causas, publicar necesidades específicas y captar donaciones o voluntarios, ¿qué tan interesados estarían en utilizarla?", "Selección única (Escala de adopción)", "Muy interesados (la adoptaríamos de inmediato) | Moderadamente interesados (depende de la facilidad de uso) | Poco interesados | No interesados.", "Validación de adopción por parte de las OSAL."],
            ["Sección 5: Validación de la Plataforma", "13. ¿Qué funcionalidad considerarías más valiosa dentro de esta plataforma? (Seleccione hasta 2 opciones):", "Casillas de verificación (Máximo 2)", "Módulo para publicar necesidades concretas de donaciones (dinero o insumos) | Módulo de reclutamiento y agenda de voluntarios por áreas/horarios | Perfil institucional verificado para generar confianza y legitimidad | Panel con métricas simples sobre interacción y alcance.", "Módulos centrales del MVP (RF01, RF04, RF05, RF10)."],
            ["Sección 5: Validación de la Plataforma", "14. Datos de contacto (Opcional):", "Texto largo abierto", "Nombre del representante, teléfono móvil / WhatsApp, correo electrónico o página web para vinculación al piloto.", "Vinculación directa al piloto (Tabla 6B y Anexo B)."]
        ],
        "note": "Nota. Estructura extraída directamente del formulario oficial aplicado a las fundaciones en Google Forms (https://forms.gle/t9MoqpGDwrZzbntW7), cuyos resultados (n = 4) se analizan en la Sección 3.4.2."
    }),

    ("H3", "3.3.1. Diseño y ficha técnica de la encuesta"),
    ("P", "Los dos cuestionarios estructurados se diseñaron empleando preguntas cerradas de opción múltiple y escalas tipo Likert (de 1 a 5) para facilitar su diligenciamiento en menos de cinco minutos desde dispositivos móviles, evitando el abandono por parte de los encuestados (Hernández Sampieri et al., 2014). La Encuesta 1 indaga la percepción e interés de las personas sobre las organizaciones sociales y la plataforma Conexión Solidaria (conocimiento local, causas de interés, formas de participación, condiciones para donar o hacer voluntariado y disposición de uso), mientras que la Encuesta 2 operacionaliza las variables diagnósticas de las OSAL (canales actuales, periodicidad de difusión, fuentes de financiamiento, jerarquización de obstáculos operativos, priorización funcional del MVP y datos de contacto). En la Tabla 6A se presenta la ficha técnica oficial de la encuesta aplicada a los potenciales usuarios."),
    ("TABLE", {
        "title": "Tabla 6A. Ficha técnica de la encuesta de percepción e interés sobre las organizaciones sociales y la plataforma Conexión Solidaria",
        "headers": ["Elemento", "Descripción"],
        "rows": [
            ["Nombre del instrumento", "Encuesta de percepción e interés sobre las organizaciones sociales y la plataforma Conexión Solidaria."],
            ["Proyecto", "Conexión Solidaria: Tecnología para el Cambio Social."],
            ["Objetivo", "Identificar el nivel de conocimiento de las personas sobre las fundaciones y organizaciones sociales de su entorno, sus intereses frente a las causas sociales, sus formas de participación y su disposición a utilizar una plataforma digital para realizar donaciones o vincularse como voluntarios."],
            ["Población objetivo", "Personas potencialmente interesadas en apoyar organizaciones sociales mediante donaciones, voluntariado u otras formas de participación."],
            ["Cobertura geográfica", "Principalmente municipios de la Sabana Centro y Norte de Cundinamarca, con participación de personas de Bogotá D. C. y otros municipios."],
            ["Tamaño de la muestra", "170 respuestas registradas."],
            ["Tipo de muestreo", "No probabilístico por conveniencia y participación voluntaria."],
            ["Medio de aplicación", "Formulario digital compartido mediante WhatsApp."],
            ["Canal de difusión", "Grupo de WhatsApp de intercambio comunitario y apoyo a emprendimientos de la zona norte de Bogotá y municipios cercanos."],
            ["Periodo de recolección", "Del 28 de septiembre al 16 de octubre de 2026."],
            ["Tipo de instrumento", "Cuestionario estructurado con preguntas cerradas y opciones de selección múltiple."],
            ["Número de preguntas", "9 preguntas, además del registro automático de la fecha y hora de respuesta."],
            ["Variables consultadas", "Rango de edad, ocupación, municipio de residencia, entorno geográfico, conocimiento de organizaciones sociales, intereses en causas sociales, participación en actividades sociales, condiciones para donar o realizar voluntariado y disposición de uso de la plataforma."],
            ["Finalidad de la información", "Obtener información para caracterizar a los posibles usuarios y orientar la propuesta de valor y las funcionalidades de Conexión Solidaria."],
            ["Procesamiento de datos", "Consolidación de las respuestas en una hoja de cálculo y análisis descriptivo de las variables consultadas."]
        ],
        "note": "Nota. Elaboración propia para la caracterización de usuarios potenciales del proyecto Conexión Solidaria (2026)."
    }),
    ("P_BOLD", "Observación metodológica"),
    ("P", "La encuesta utilizó un muestreo no probabilístico por conveniencia, debido a que fue difundida mediante un grupo de WhatsApp y respondida voluntariamente por sus participantes. Por esta razón, los resultados permiten identificar tendencias y percepciones de las personas encuestadas, pero no deben interpretarse como representativos de toda la población de los municipios consultados."),

    ("H3", "3.3.2. Diseño de las entrevistas y actividades de diagnóstico"),
    ("P", "Para la ejecución del diagnóstico empírico en terreno con los directores de las fundaciones rurales, se diseñó un guion de entrevista semiestructurada acompañado de una ficha de observación no participante validada mediante juicio de expertos dentro del espacio académico de Ciencia, Tecnología e Innovación III. El guion abordó cinco ejes temáticos: (1) historia, objeto social y población atendida por la fundación; (2) procesos administrativos y contables utilizados para registrar ingresos, gastos e inventarios de donaciones; (3) mecanismos actuales de convocatoria y coordinación de voluntarios; (4) tenencia de equipos de cómputo, calidad de conexión a internet en la vereda y manejo de redes sociales o sitio web; y (5) expectativas frente a una herramienta digital gratuita."),

    ("H3", "3.3.3. Población consultada y criterios de selección"),
    ("P", "La población efectivamente consultada en el estudio diagnóstico abarcó los dos lados del ecosistema social regional: (1) del lado de la oferta institucional, las cuatro fundaciones encuestadas y caracterizadas en Cundinamarca —Gotitas de Amor (Mis Gotitas de Amor) en Cajicá, Casa de los Abuelos (Abuelos Campesinos) en Machetá, Campamentos de Nueva Vida (Campamentos de Vida Nueva) en Simijaca y Patitas Campesinas en La Calera—, seleccionadas por atender líneas de acción distintas en zonas veredales y municipales; y (2) del lado de la demanda solidaria ciudadana, una muestra de n = 170 personas registradas mediante muestreo no probabilístico por conveniencia y participación voluntaria, residentes principalmente en municipios de la Sabana Centro y Norte de Cundinamarca (Chía con 61,8 %, Zipaquirá, Cota y otros municipios cercanos con 18,8 %) y Bogotá D.C. (19,4 %), distribuida entre habitantes de casco urbano (54,7 %) y residentes de veredas o sectores rurales/campestres (45,3 %)."),

    ("H3", "3.3.4. Procedimiento de recolección de información"),
    ("P", "El procedimiento de recolección se ejecutó en cuatro etapas: primero, se procesaron las bases agregadas nacionales de la Encuesta de Investigación y Desarrollo del DANE (2021) y del estudio gremial de la AFE (2018); segundo, se aplicó el cuestionario diagnóstico de 14 variables y la matriz de caracterización a las cuatro fundaciones participantes (archivo Respuestas_Encuesta_Fundaciones_Conexion_Solidaria.xlsx, con hojas 'Respuestas Encuesta' y 'Detalle por Fundación'); tercero, del 28 de septiembre al 16 de octubre de 2026 se aplicó el formulario digital de la Encuesta de percepción e interés sobre las organizaciones sociales y la plataforma Conexión Solidaria difundido a través de un grupo de WhatsApp de intercambio comunitario y apoyo a emprendimientos de la zona norte de Bogotá y municipios cercanos, obteniendo n = 170 respuestas válidas completas con registro automático de fecha y hora (archivo 150_Respuestas_Conexion_Solidaria.xlsx, véase Sección 3.4.3 y Anexo B); y cuarto, se parametrizaron cinco perfiles operativos en la base de datos del MVP para validar sus requerimientos funcionales."),

    ("H2", "3.4. Presentación y análisis de resultados"),
    ("P", "A continuación se presentan los resultados cuantitativos y cualitativos obtenidos en el estudio diagnóstico, separando el análisis de las cifras oficiales del DANE (2021) y la AFE (2018) frente a lo observado directamente en las fundaciones rurales entrevistadas."),

    ("H3", "3.4.1. Resultados del análisis cuantitativo sectorial y del diagnóstico"),
    ("P", "Para el marco del estudio se analizó el informe de la Encuesta de Investigación y Desarrollo en Colombia, realizada por el Departamento Administrativo Nacional de Estadística (DANE, 2021), revisando aspectos como la financiación fragmentada, la orientación a proyectos prácticos y la vulnerabilidad operativa. De este análisis se obtuvieron resultados relevantes para la investigación, donde el eje central es la fragilidad institucional y de procesos en las entidades Privadas Sin Ánimo de Lucro (PSAL), las cuales señalan serias dificultades para la obtención y destinación de recursos a investigación y desarrollo en este tipo de organizaciones (véase Figura 1)."),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\RESULTADOS_p2_img1_726x508.jpeg",
        "caption": "Figura 1. Número de empresas e instituciones investigadas en actividades de I+D según sector nacional",
        "note": "Nota. Tomado del Informe de la Encuesta de Investigación y Desarrollo (DANE, 2021), procesado en el análisis diagnóstico del proyecto (Olier & Robayo, 2025)."
    }),
    ("P", "Se evidencia que el 36 % de las PSAL que no invirtieron en I+D fue debido a que no cuentan con los recursos financieros para hacerlo, y que el 14 % indicó que no cuentan con el personal técnico calificado para llevarlo a cabo (véase Figura 2). Asimismo, como referente nacional para organizaciones privadas sin ánimo de lucro (PSAL), los datos del DANE muestran un patrón de vulnerabilidad operativa y dependencia de recursos externos (véase Figura 3). A diferencia de los demás sectores, las fundaciones son el sector con menor inversión en Investigación y Desarrollo. Estos aspectos se relacionan directamente con lo observado en las cuatro fundaciones rurales, entre los cuales resaltan las limitaciones de recursos, los procesos manuales y una adopción incipiente de TIC que restringe la gestión de información, la comunicación y el acceso a financiación."),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\RESULTADOS_p3_img1_820x714.jpeg",
        "caption": "Figura 2. Porcentaje de instituciones que no ejecutaron actividades de I+D según razones reportadas por sector (Total Nacional)",
        "note": "Nota. El 36 % de las PSAL reporta carencia de recursos financieros y el 14 % falta de personal técnico calificado. Fuente: DANE (2021)."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\RESULTADOS_p4_img1_889x461.jpeg",
        "caption": "Figura 3. Distribución de montos de inversión en I+D intramuros según origen de financiamiento y sector",
        "note": "Nota. Se evidencia la vulnerabilidad financiera y la dependencia de recursos externos en el sector PSAL. Fuente: DANE (2021)."
    }),
    ("P", "Por su parte, la Asociación de Fundaciones Familiares y Empresariales (AFE, 2018; Villar Gómez, 2018) realizó un estudio basado en una muestra de fundaciones afiliadas donde evalúa la estabilidad de sus fuentes de ingreso, colaboración y gestión en relación con los Objetivos de Desarrollo Sostenible y el trabajo en contextos locales. Como muestran las Figuras 4 y 5, mientras las fundaciones empresariales manejan presupuestos altos, las fundaciones independientes o comunitarias operan con gastos anuales muy bajos y un número reducido de voluntarios."),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\RESULTADOS_p5_img1_625x224.jpeg",
        "caption": "Figura 4. Porcentaje de fundaciones en Colombia según monto de gasto anual por tipo de fundación",
        "note": "Nota. Tomado de Las fundaciones en Colombia: Características, tendencias y desafíos (AFE, 2018; Villar Gómez, 2018)."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\RESULTADOS_p5_img2_647x299.jpeg",
        "caption": "Figura 5. Porcentaje de fundaciones en Colombia según número de voluntarios vinculados por tipo de fundación",
        "note": "Nota. Se evidencia el bajo volumen de voluntariado formalizado en fundaciones pequeñas. Fuente: AFE (2018)."
    }),

    ("H3", "3.4.2. Análisis de las necesidades de las organizaciones (Resultados de la Encuesta a Fundaciones)"),
    ("P", "Se aplicó el instrumento diagnóstico de 14 ítems, entrevistas y observación de campo a cuatro entidades sin ánimo de lucro de Cundinamarca: Gotitas de Amor (Mis Gotitas de Amor) en Cajicá, Casa de los Abuelos (Abuelos Campesinos) en Machetá, Campamentos de Nueva Vida (Campamentos de Vida Nueva) en Simijaca y Patitas Campesinas en La Calera. Aunque en su objeto social atienden causas distintas (primera infancia, adulto mayor campesino, juventud/familias y fauna rescatada), en su situación administrativa, comunicativa y financiera presentan patrones muy similares, ya que operan con recursos sumamente limitados."),
    ("P", "Dicha gestión administrativa y financiera es precaria y no cuentan con sistemas formales de información para gestionar donaciones o voluntariado. Al examinar las respuestas consolidadas de la encuesta y el detalle por fundación (véase Tabla 6B y desglose completo en el Anexo B), se identifican seis hallazgos empíricos directos:"),
    ("UL", [
        "1. Entorno geográfico y naturaleza organizacional (Preguntas 2, 3 y 4): El 75 % de las entidades encuestadas (3 de 4: Gotitas de Amor, Casa de los Abuelos y Patitas Campesinas) corresponde a fundaciones comunitarias de base local y el 25 % restante (Campamentos de Nueva Vida) a una fundación independiente filantrópica. En cuanto a su entorno de operación, el 50 % opera en modalidad mixta tanto en veredas como en casco urbano (Machetá y Simijaca), el 25 % principalmente en zonas rurales y veredales (La Calera) y el 25 % en casco urbano municipal (Cajicá).",
        "2. Canales de comunicación y frecuencia de publicación (Preguntas 6 y 7): Ninguna de las cuatro fundaciones reporta su sitio web como canal activo de difusión de necesidades o convocatorias en la pregunta 6. Gotitas de Amor (Cajicá) reporta que no cuenta con un canal de comunicación continuo y publica únicamente cuando ocurre un evento o necesidad urgente; Casa de los Abuelos (Machetá) depende de medios comunitarios tradicionales (radio local, carteleras y perifoneo) con frecuencia quincenal o mensual; Campamentos de Nueva Vida (Simijaca) utiliza canales de mensajería (WhatsApp y Telegram) de forma quincenal o mensual; y Patitas Campesinas (La Calera) emplea redes sociales (Facebook, Instagram, TikTok) varias veces a la semana.",
        "3. Respuesta del público y medición de métricas (Preguntas 8 y 9): En una escala de 1 (muy baja) a 5 (muy alta), la respuesta percibida del público alcanza un promedio general de apenas 2,75 puntos: tanto Gotitas de Amor (Cajicá) como Campamentos de Nueva Vida (Simijaca) califican la respuesta ciudadana con un 2, Casa de los Abuelos (Machetá) con un 3, y Patitas Campesinas (La Calera) con un 4. Respecto al análisis de métricas digitales, el 50 % (Cajicá y Simijaca) afirma que no analiza métricas por falta de tiempo o herramientas especializadas, el 25 % (Machetá) solo revisa comentarios y mensajes directamente, y apenas el 25 % (La Calera) revisa métricas básicas de redes sociales.",
        "4. Fuentes actuales de sostenimiento (Pregunta 10): El 100 % de las fundaciones encuestadas (4 de 4) depende de donaciones económicas de personas naturales y del aporte voluntario no remunerado de sus propios miembros o de la comunidad; el 75 % (Cajicá, Machetá y La Calera) recibe donaciones en especie o insumos (alimentos, ropa, materiales); solo el 25 % (Casa de los Abuelos en Machetá) ha accedido a subvenciones o convenios públicos; y ninguna (0 %) cuenta con alianzas financiadoras del sector empresarial privado.",
        "5. Jerarquización de desafíos operativos (Pregunta 11, escala de 1 Mayor obstáculo a 5 Menor obstáculo): La falta de recursos económicos se posiciona como el obstáculo número 1 (Mayor) en el 75 % de las fundaciones (Cajicá, Machetá y La Calera) y número 2 en Simijaca (promedio de severidad: 1,25). La baja visibilidad pública ocupa el puesto número 1 (Mayor obstáculo) para Campamentos de Nueva Vida en Simijaca, el puesto 2 para Casa de los Abuelos en Machetá y el puesto 3 en Cajicá y La Calera (promedio: 2,25). La dificultad para reclutar y retener voluntarios se ubica en el puesto 2 para Cajicá y La Calera y en el puesto 3 para Machetá y Simijaca (promedio: 2,50). Por su parte, la carga administrativa (promedio: 4,25) y la medición de impacto (promedio: 4,75) se ubican en los lugares 4 y 5, evidenciando que la urgencia inmediata de las fundaciones es conseguir recursos, visibilidad y voluntarios.",
        "6. Validación de interés y funcionalidades prioritarias del MVP (Preguntas 12 y 13): El 100 % de las fundaciones encuestadas (4 de 4) respondió estar «Muy interesados (la adoptaríamos de inmediato)» frente a una plataforma gratuita como Conexión Solidaria. Al elegir las dos funcionalidades más valiosas, el 75 % (Gotitas de Amor, Campamentos de Nueva Vida y Patitas Campesinas) seleccionó el «Módulo para publicar necesidades concretas de donaciones (dinero o insumos)»; el 75 % (Gotitas de Amor, Casa de los Abuelos y Patitas Campesinas) seleccionó el «Módulo de reclutamiento y agenda de voluntarios por áreas/horarios»; y el 50 % (Casa de los Abuelos y Campamentos de Nueva Vida) priorizó el «Perfil institucional verificado para generar confianza y legitimidad»."
    ]),
    ("TABLE", {
        "title": "Tabla 6B. Consolidado de respuestas de la encuesta diagnóstica aplicada a las cuatro fundaciones participantes",
        "headers": ["Variable / Ítem de la Encuesta", "Gotitas de Amor (Cajicá)", "Casa de los Abuelos (Machetá)", "Campamentos de Nueva Vida (Simijaca)", "Patitas Campesinas (La Calera)"],
        "rows": [
            ["Entorno geográfico y Tipo de OSAL", "Casco urbano / Comunitaria de base local.", "Mixto (veredas y urbano) / Comunitaria de base local.", "Mixto (veredas y urbano) / Independiente filantrópica.", "Principalmente zonas rurales-veredales / Comunitaria local."],
            ["Población beneficiada", "Primera infancia, niñez, adolescencia y familias vulnerables.", "Adultos mayores, familias vulnerables y comunidades campesinas.", "Familias en vulnerabilidad, juventud y comunidad general.", "Animales en abandono/rescate y comunidades rurales."],
            ["Canales y frecuencia de publicación", "Sin canal continuo / Solo en evento o urgencia.", "Radio local, carteleras y perifoneo / Quincenal o mensual.", "Mensajería (WhatsApp, Telegram) / Quincenal o mensual.", "Redes sociales (Facebook, Instagram, TikTok) / Varias veces por semana."],
            ["Respuesta del público (1-5) y Métricas", "Nivel 2 / No analiza métricas por falta de tiempo o herramientas.", "Nivel 3 / Solo revisa comentarios y mensajes directos.", "Nivel 2 / No analiza métricas por falta de tiempo o herramientas.", "Nivel 4 / Revisa métricas básicas de redes periódicamente."],
            ["Fuentes de apoyo actuales", "Personas naturales (dinero y especie) y aporte voluntario de miembros.", "Personas naturales (dinero y especie), convenios públicos y miembros.", "Personas naturales (dinero) y aporte voluntario de miembros.", "Personas naturales (dinero y especie) y aporte voluntario de miembros."],
            ["Ranking de desafíos (1 Mayor a 5 Menor)", "1. Recursos económicos; 2. Voluntarios; 3. Visibilidad; 4. Carga admin.; 5. Medir impacto.", "1. Recursos económicos; 2. Visibilidad; 3. Voluntarios; 4. Carga admin.; 5. Medir impacto.", "1. Baja visibilidad; 2. Recursos económicos; 3. Voluntarios; 4. Medir impacto; 5. Carga admin.", "1. Recursos económicos; 2. Voluntarios; 3. Visibilidad; 4. Carga admin.; 5. Medir impacto."],
            ["Interés en plataforma gratuita", "Muy interesados (adopción inmediata).", "Muy interesados (adopción inmediata).", "Muy interesados (adopción inmediata).", "Muy interesados (adopción inmediata)."],
            ["Funcionalidades más valiosas elegidas", "Módulo de necesidades (dinero/insumos) y Módulo de agenda de voluntarios.", "Módulo de agenda de voluntarios y Perfil institucional verificado.", "Perfil institucional verificado y Módulo de necesidades (dinero/insumos).", "Módulo de necesidades (dinero/insumos) y Módulo de agenda de voluntarios."],
            ["Datos de contacto institucionales", "3133934744 / misgotitasdeamor2022@gmail.com", "Inés Camelo / 3112089943 / abuelitosmacheta@gmail.com", "Padre César / 3107173205 / www.campamentosdevidanueva.org", "3118854757 / patitascampesinas@gmail.com / patitascampesinas.org"]
        ],
        "note": "Nota. Datos primarios extraídos textualmente de las hojas 'Respuestas Encuesta' y 'Detalle por Fundación' del instrumento Respuestas_Encuesta_Fundaciones_Conexion_Solidaria.xlsx (Olier & Robayo, 2026). Tabulación íntegra de las 14 preguntas en el Anexo B."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\encuesta_fundaciones_desafios_y_modulos.png",
        "caption": "Figura 5B. Índice de criticidad de los desafíos operativos y funcionalidades más valiosas en las 4 fundaciones encuestadas",
        "note": "Nota. Procesamiento gráfico a partir de Respuestas_Encuesta_Fundaciones_Conexion_Solidaria.xlsx (n = 4 fundaciones en Cajicá, Machetá, Simijaca y La Calera)."
    }),

    ("H3", "3.4.3. Análisis de las necesidades de donantes y voluntarios (Resultados de la Encuesta Ciudadana, n = 170)"),
    ("P", "Para la obtención de donaciones o de voluntarios, las fundaciones consultadas lo hacen de forma personal, dependiendo únicamente de su mercado natural (familiares, vecinos o conocidos cercanos), sin planes ni protocolos de respuesta a donantes o aliados. Con el fin de contrastar esta realidad frente a la percepción de la ciudadanía de la región, se procesaron las n = 170 respuestas recolectadas en la Encuesta de Comunidad (archivo 150_Respuestas_Conexion_Solidaria.xlsx), cuyos hallazgos cuantitativos (véanse Tabla 6C y Figuras 5C, 5D y 5E) confirman la existencia de una alta demanda solidaria insatisfecha por falta de visibilidad y transparencia:"),
    ("UL", [
        "1. Perfil sociodemográfico y territorial de los encuestados (Preguntas 1 a 4, n = 170): El 70,6 % de la muestra corresponde a adultos jóvenes y de mediana edad en plena etapa productiva —35,9 % entre 26 y 35 años (61 personas) y 34,7 % entre 36 y 50 años (59 personas)—, complementados por un 14,7 % de jóvenes entre 18 y 25 años (25 personas) y un 14,7 % de mayores de 50 años (25 personas). En ocupación, el 56,5 % son empleados (96 personas), el 18,2 % trabajadores independientes o emprendedores (31 personas) y el 11,8 % estudiantes universitarios (20 personas). Geográficamente, el 61,8 % reside en Chía (105 personas), el 19,4 % en Bogotá D.C. con vínculo en el corredor norte (33 personas) y el 18,8 % restante en Zipaquirá, Cota y otros municipios de la Sabana (32 personas). Destaca que el 54,7 % habita en casco urbano (93 personas) y el 45,3 % reside directamente en zona rural o periurbana veredal (77 personas).",
        "2. Evidencia empírica de la invisibilidad de las fundaciones locales (Pregunta 5, n = 170): Casi dos tercios de los ciudadanos encuestados (el 64,7 %, equivalente a 110 de las 170 personas) desconocen las actividades de las fundaciones de su entorno: el 28,8 % (49 personas) afirma que «casi no tengo conocimiento de organizaciones locales», el 24,7 % (42 personas) señala que «conozco algunas de nombre, pero no sé en detalle sus actividades», y el 11,2 % (19 personas) manifiesta que «no conozco ninguna». Únicamente el 35,3 % (60 personas) conoce varias fundaciones y sus actividades (véase Figura 5C).",
        "3. Causas sociales de mayor interés y hábitos de participación (Preguntas 6 y 7, n = 170): En selección múltiple, las líneas de acción que despiertan mayor vocación de apoyo ciudadano son Infancia y juventud con el 56,5 % de los encuestados (96 menciones), Adulto mayor con el 38,2 % (65 menciones), Desarrollo comunitario y rural con el 35,3 % (60 menciones), Medio ambiente y sostenibilidad con el 32,9 % (56 menciones), Educación y formación técnica con el 32,9 % (56 menciones), Salud y bienestar con el 25,3 % (43 menciones) y Cuidado y protección animal con el 24,1 % (41 menciones). Durante el último año, el 79,4 % de la muestra participó en alguna actividad solidaria, liderando el voluntariado presencial en campo con el 35,3 % (60 personas), la donación de bienes materiales o insumos (ropa, alimentos, herramientas) con el 32,4 % (55 personas) y las donaciones de dinero con el 24,7 % (42 personas), además del voluntariado profesional/remoto (19,4 %) y la difusión en redes (18,8 %), mientras que un 20,6 % (35 personas) no participó activamente (véase Figura 5D).",
        "4. Condición indispensable para donar o hacer voluntariado (Pregunta 8, n = 170): El resultado más contundente para la arquitectura del software es que el 58,2 % de los ciudadanos (99 de 170 personas) exige como condición indispensable la «Transparencia total en el uso de los fondos y recursos», seguido por el 21,8 % (37 personas) que exige «Claridad en las actividades o tareas específicas que se van a realizar», el 10,6 % (18 personas) que prioriza la «Facilidad para realizar el aporte de forma digital» y el 9,4 % (16 personas) la «Cercanía comunitaria o geográfica». Es decir, el 80,0 % de la ciudadanía condiciona su ayuda a la transparencia de los recursos y a la claridad de las tareas, justificando de manera directa el protocolo de confirmación bilateral (PGVTT), los certificados PDF con hash SHA-256 y el agendamiento estructurado del MVP.",
        "5. Validación de intención de adopción de la plataforma Conexión Solidaria (Pregunta 9, n = 170): El 95,9 % de los encuestados (163 de las 170 personas) manifestó disposición positiva para utilizar la plataforma web/móvil Conexión Solidaria: el 52,9 % (90 personas) respondió estar «Totalmente dispuesto(a)» y el 42,9 % (73 personas) respondió «Probablemente sí», frente a solo un 4,1 % (7 personas) que indicó no estar interesado (véase Figura 5E)."
    ]),
    ("TABLE", {
        "title": "Tabla 6C. Resumen estadístico de las 170 respuestas de la Encuesta a Donantes y Voluntarios Potenciales",
        "headers": ["Pregunta / Variable Evaluada", "Categoría Principal / Respuesta", "Frecuencia (n = 170)", "Porcentaje (%)", "Requerimiento del MVP que Respalda"],
        "rows": [
            ["1. Rango de edad", "26-35 años (61) | 36-50 años (59) | 18-25 (25) | >50 (25)", "120 en 26-50 años", "70,6 % (26-50 años)", "Interfaz intuitiva multi-edad (RNF02, WCAG 2.2)."],
            ["2. Ocupación principal", "Empleado (96) | Independiente (31) | Estudiante (20)", "147 activos/estud.", "86,5 %", "Capacidad de donación y voluntariado universitario/profesional."],
            ["3 y 4. Municipio y Zona", "Chía (61,8 %) y Sabana/Bogotá (38,2 %) | Urbana vs. Rural", "93 Urb. / 77 Rural", "54,7 % Urb / 45,3 % Rur", "Arquitectura ligera para veredas (RNF01) y mapa regional (RF03)."],
            ["5. Conocimiento de OSAL", "Casi nulo (28,8 %), solo nombre (24,7 %) o nulo (11,2 %)", "110 de 170", "64,7 % desconoce", "Directorio público georreferenciado por municipio y causa (RF03)."],
            ["6. Causas de mayor interés", "Infancia (56,5 %), Adulto mayor (38,2 %), Rural (35,3 %), Amb. (32,9 %)", "96 / 65 / 60 / 56", "56,5 % a 24,1 %", "Alineación con los 9 ODS y filtros por categoría social (RF03, RF10)."],
            ["7. Apoyo en el último año", "Voluntariado campo (35,3 %), Insumos (32,4 %), Dinero (24,7 %)", "60 / 55 / 42", "35,3 % / 32,4 % / 24,7 %", "Módulos duales de donación (dinero/especie) y voluntariado (RF04-RF07)."],
            ["8. Condición indispensable", "Transparencia en fondos (58,2 %) y Claridad de tareas (21,8 %)", "99 y 37 de 170", "80,0 % consolidado", "Protocolo PGVTT, certificado PDF SHA-256 (RF08, RF09) y cupos (RF05)."],
            ["9. Disposición de uso MVP", "Totalmente dispuesto(a) (52,9 %) + Probablemente sí (42,9 %)", "163 de 170", "95,9 % aceptación", "Viabilidad comercial y de adopción comunitaria del emprendimiento."]
        ],
        "note": "Nota. Procesamiento estadístico del archivo maestro 150_Respuestas_Conexion_Solidaria.xlsx (n = 170 registros válidos). Tabulación completa en el Anexo B."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\encuesta_comunidad_1_perfil_y_conocimiento.png",
        "caption": "Figura 5C. Nivel de conocimiento sobre fundaciones locales y distribución por zona y edad de los encuestados (n = 170)",
        "note": "Nota. El 64,7 % de la ciudadanía desconoce en detalle las fundaciones de su municipio. Fuente: Encuesta de Comunidad (150_Respuestas_Conexion_Solidaria.xlsx)."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\encuesta_comunidad_2_causas_y_participacion.png",
        "caption": "Figura 5D. Causas sociales de mayor interés y modalidades de participación solidaria en el último año (n = 170)",
        "note": "Nota. Destacan el interés en infancia, adulto mayor y desarrollo rural, así como la preferencia por voluntariado presencial y donación en especie."
    }),
    ("IMAGE", {
        "path": r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales\encuesta_comunidad_3_condicion_y_adopcion.png",
        "caption": "Figura 5E. Condición indispensable para apoyar a una fundación e intención de uso de la plataforma Conexión Solidaria (n = 170)",
        "note": "Nota. El 58,2 % exige transparencia total en el uso de recursos y el 95,9 % (163 de 170) manifiesta disposición positiva de uso de la plataforma."
    }),

    ("H3", "3.4.4. Análisis comparativo de las organizaciones participantes"),
    ("P", "La Tabla 7 presenta el análisis comparativo entre los resultados obtenidos en las entrevistas a las fundaciones rurales y los datos de los informes del análisis cuantitativo (DANE, 2021; AFE, 2018)."),
    ("TABLE", {
        "title": "Tabla 7. Análisis comparativo triangular entre los hallazgos de las entrevistas en fundaciones rurales, el DANE y la AFE",
        "headers": ["Características", "Fundaciones rurales (Sabana)", "DANE (2021 / 2022)", "AFE Colombia (2018)"],
        "rows": [
            ["Capacidades internas", "Procesos manuales en papel; ausencia de sistemas de información y analítica.", "Reporta fundaciones sin ánimo de lucro con capacidades internas limitadas (14 % sin personal técnico) y uso de personal externo.", "Describe prácticas estratégicas en fundaciones consolidadas que las pequeñas no tienen."],
            ["Financiamiento", "Recursos escasos; dependencia de donaciones puntuales de su círculo cercano.", "El 36 % no invierte en I+D por falta de recursos propios; enfatiza dependencia de fuentes externas.", "Observa ingresos más estables en empresariales; los casos rurales se asemejan a independientes o comunitarias."],
            ["TIC / Transformación digital", "Sin sitio web; redes sociales precarias; sin CRM ni contabilidad digital.", "Evidencia brecha digital rural y sugiere necesidad de apoyo técnico y proyectos aplicados para modernizar.", "No caracteriza TIC rurales en detalle, pero muestra mayor formalización en entidades empresariales."],
            ["Evaluación / medición", "Sin indicadores periódicos ni reportes sistemáticos de impacto.", "La fragilidad operativa dificulta la medición de resultados.", "Se enfoca en la evaluación y transparencia promovida por la asociación."],
            ["Enfoque territorial / ODS", "Trabajo local intensivo; alto compromiso social con su comunidad.", "Registra orientación predominante a objetivos socioeconómicos.", "Destaca alineación del 94 % con los ODS y trabajo territorial."]
        ],
        "note": "Nota. Elaboración propia a partir del análisis comparativo de resultados del proyecto (Olier & Robayo, 2025)."
    }),

    ("H3", "3.4.5. Interpretación de los hallazgos"),
    ("P", "Los resultados confirmaron la existencia de una brecha digital amplia entre el sector empresarial y el sector privado sin ánimo de lucro, la cual se profundiza en las fundaciones rurales con acceso limitado a las TIC e invisibiliza su labor. En las fundaciones rurales estudiadas, la ausencia de sitio web, la gestión contable en papel y el uso esporádico de redes sociales sin métricas ni responsables revelan una inaccesibilidad a la tecnología que limita o nubla la visibilidad de sus programas, la transparencia de la gestión y la sostenibilidad financiera. Aunque las misiones son diversas, los patrones de gestión son muy similares: al no contar con sistemas de información, bases de datos estructuradas, indicadores periódicos de resultado o impacto y estrategias de comunicación, se encuentran limitadas para cumplir con su objetivo y ven reducido su alcance territorial."),
    ("P", "Se evidencia así una brecha digital operativa importante que compromete la sostenibilidad de las entidades sin ánimo de lucro rurales. Esto se debe a la ausencia de sistemas de información que apoyen su administración y de visibilidad web que aumente su alcance, aspectos que dificultan el acceso a financiación. Este patrón se alinea con el diagnóstico del DANE, donde se expone que el subsector compuesto por asociaciones privadas sin ánimo de lucro demanda apoyo externo y proyectos aplicados, lo que contrasta con las prácticas de evaluación reportadas por la AFE en organizaciones empresariales más consolidadas. Esta diferencia muestra que las fundaciones analizadas corresponden a perfiles independientes o comunitarios con mayores vulnerabilidades operativas."),
    ("P", "Los resultados también indican que, pese a los recursos limitados, existe un capital social relevante descrito como compromiso comunitario, arraigo territorial y disposición a ayudar, siendo la base para futuras mejoras organizacionales acompañadas de capacidades técnicas que permitan medir y comunicar el valor social generado. En conjunto, la evidencia describe la necesidad social de la transformación digital —la organización de la información, la formalización de la comunicación y la adopción de herramientas digitales— como un requisito indispensable para mejorar la obtención de recursos y el cumplimiento del objeto social del tercer sector. La coherencia entre los hallazgos locales y los datos obtenidos del DANE y la AFE sugiere que se requieren apoyos para la tecnificación de la gestión de las fundaciones, estrategias de comunicación y exposición que se traduzcan en mejoras operativas y de sostenibilidad, y de esta manera puedan tener mayor probabilidad de generar un cambio social importante en su entorno."),

    ("H2", "3.5. Identificación de necesidades y problemas"),
    ("P", "Del trabajo de campo se desprenden las necesidades puntuales que debe resolver la plataforma Conexión Solidaria."),

    ("H3", "3.5.1. Necesidades comunes"),
    ("P", "Las organizaciones estudiadas comparten cuatro necesidades básicas: (1) tener una página o perfil web propio y verificado sin pagar hosting ni desarrollo; (2) contar con un listado claro donde publicar qué necesitan en dinero o en insumos físicos; (3) organizar la convocatoria de voluntarios con fechas y cupos definidos; y (4) llevar el registro de lo que reciben para entregar certificados de donación confiables."),

    ("H3", "3.5.2. Necesidades particulares"),
    ("P", "Cada fundación tiene requerimientos específicos según la población que atiende: los hogares de adulto mayor (como FARASAN en Cogua) necesitan sobre todo pañales, medicamentos, alimentos no perecederos y apoyo en salud; los albergues de rescate animal (como FUNHUELLAS en Cajicá) requieren concentrado, insumos veterinarios y voluntarios para jornadas de limpieza y adopción; las fundaciones de primera infancia (como FUNDAULA en Chía) buscan útiles escolares, equipos de cómputo y refuerzo escolar; y los colectivos ambientales (como CORPOJUAICA en Tabio) necesitan convocar grupos de voluntarios para jornadas de siembra en quebradas y páramos."),

    ("H3", "3.5.3. Dificultades actuales de comunicación y visibilidad"),
    ("P", "[[EDITAR]]El problema práctico de usar solo WhatsApp o redes sociales es que las publicaciones se pierden rápido y no llevan ningún control.[[/EDITAR]] Si una fundación pide veinte mercados o cincuenta kilos de concentrado en una historia de Instagram, a los dos días nadie sabe cuánto se ha recogido ni cuánto falta, y el director de la fundación termina gastando horas respondiendo los mismos mensajes por interno."),

    ("H3", "3.5.4. Dificultades de acceso a donaciones y voluntariado"),
    ("P", "Para los posibles donantes que viven fuera de la vereda, el principal freno es la desconfianza cuando no ven documentos legales ni soportes claros del destino de su ayuda. En el caso de los voluntarios, como no hay un sistema de agendamiento por cupos, hay fines de semana en los que no llega nadie y otros en los que asisten personas sin las habilidades que requería la jornada."),

    ("H3", "3.5.5. Priorización de necesidades"),
    ("P", "Tomando la escala de 1 a 5 definida en la Encuesta 2, las prioridades operativas para las OSAL rurales quedaron ordenadas así: en primer lugar (prioridad crítica), lograr visibilidad verificada y captar donaciones en especie y dinero sin cobro de comisiones; en segundo lugar, organizar el agendamiento de voluntarios por cupos y horarios; en tercer lugar, automatizar la emisión de certificados de donación; y en cuarto lugar, contar con indicadores básicos de impacto por ODS."),

    ("H2", "3.6. Análisis del mercado"),
    ("P", "Siguiendo la Guía ADOr006_V10 (Universidad de Cundinamarca, 2024), se dimensionó el mercado regional en la Sabana Centro y Norte para estimar cuántas organizaciones, ciudadanos y empresas pueden vincularse al proyecto."),

    ("H3", "3.6.1. Segmentación del mercado"),
    ("P", "La Tabla 8 presenta la cuantificación del mercado bajo el esquema TAM, SAM y SOM para los tres grupos de actores del modelo:"),
    ("TABLE", {
        "title": "Tabla 8. Segmentación y cuantificación del mercado objetivo (TAM, SAM y SOM) de Conexión Solidaria",
        "headers": ["Nivel de Mercado", "Segmento A: Organizaciones Sociales (OSAL)", "Segmento B: Donantes y Voluntarios Ciudadanos", "Segmento C: Empresas Aliadas (RSE / Patrocinio)"],
        "rows": [
            ["Mercado Total Disponible (TAM - Departamento de Cundinamarca)", "Más de 3.500 ESAL registradas en las Cámaras de Comercio con jurisdicción en Cundinamarca (CCB, 2023; Escobar Cazal & Escobar Reyes, 2017).", "Población mayor de 18 años con acceso a internet en Cundinamarca y Bogotá Norte (~1.800.000 personas).", "Total de medianas y grandes empresas registradas en Cundinamarca (~4.200 empresas)."],
            ["Mercado Disponible Servible (SAM - 18 Municipios Sabana Centro y Norte)", "Aproximadamente 420 fundaciones, asociaciones y corporaciones comunitarias activas en los 18 municipios de cobertura.", "Ciudadanos residentes y población universitaria en Sabana Centro y Norte (~380.000 habitantes urbanos y > 35.000 universitarios).", "Aproximadamente 650 empresas industriales, comerciales y de servicios ubicadas en el corredor Chía-Cajicá-Zipaquirá-Tocancipá."],
            ["Mercado Objetivo Alcanzable (SOM - Meta Operativa Años 1 a 3)", "Año 1: 25 OSAL verificadas; Año 2: 60 OSAL verificadas; Año 3: 120 OSAL verificadas (28,5 % del SAM regional).", "Año 1: 500 usuarios activos (donantes/voluntarios); Año 2: 1.500 usuarios; Año 3: 3.500 usuarios registrados.", "Año 1: 4 a 6 empresas patrocinadoras RSE; Año 2: 10 empresas; Año 3: 18 empresas aliadas."]
        ],
        "note": "Nota. Elaboración propia con base en proyecciones demográficas regionales (Sabana Centro Cómo Vamos, 2024; CCB, 2023)."
    }),

    ("H3", "3.6.2. Identificación de competidores y alternativas"),
    ("P", "En los dieciocho municipios de Sabana Centro y Norte no existe hoy una plataforma web gratuita dedicada a las fundaciones rurales. Las alternativas actuales son indirectas: redes sociales generales (Facebook, Instagram y WhatsApp), portales extranjeros de crowdfunding que cobran comisión en dólares (GoFundMe, GlobalGiving) y páginas temporales creadas solo cuando ocurre una emergencia natural."),

    ("H3", "3.6.3. Comparación de funcionalidades y servicios"),
    ("P", "Como se vio en la Tabla 3 (Sección 2.3.3), al comparar siete criterios prácticos —gratuidad para la OSAL, mapa de la Sabana, bajo consumo de datos para zonas rurales, donaciones en dinero e insumos, agenda de voluntariado con cupos, validación legal de la fundación y certificado de donación en PDF—, Conexión Solidaria es la única herramienta que integra los siete puntos en un mismo lugar."),

    ("H3", "3.6.4. Oportunidades de mercado"),
    ("P", "La región tiene tres condiciones muy favorables para este proyecto: la alta presencia de universidades en Chía, Cajicá y Zipaquirá con miles de estudiantes que buscan dónde hacer su práctica social o voluntariado; los parques industriales de Tocancipá, Gachancipá, Sopó y Zipaquirá con empresas que necesitan ejecutar programas de Responsabilidad Social Empresarial (RSE) con soporte tributario; y el interés de los habitantes de la Sabana por apoyar causas locales verificadas."),

    ("H3", "3.6.5. Diferenciación de Conexión Solidaria"),
    ("P", "Para las organizaciones sin ánimo de lucro en zonas rurales, el uso de TIC es especialmente importante, ya que pueden superar las barreras geográficas y lograr un mayor alcance a nivel regional y nacional, elementos esenciales para su autosuficiencia y éxito en la recaudación de fondos y apoyo comunitario. Lo que diferencia a Conexión Solidaria es que está pensada desde cero para la realidad de las veredas de la Sabana: no les cobra comisión ni mensualidades a las fundaciones, verifica los documentos legales de cada organización antes de publicarla en el mapa y funciona con fluidez incluso con datos móviles limitados."),

    ("H2", "3.7. Definición de los requerimientos del emprendimiento"),
    ("P", "En la fase de formulación y propuesta de la aplicación de comunicación se definió el desarrollo de una aplicación web para la gestión de voluntariado y donaciones en organizaciones sin ánimo de lucro dividida en dos grandes interfaces operativas:"),
    ("UL", [
        "1. Interfaz Fundaciones: (a) Información de la Fundación (causa u objetivo social, ubicación, tiempo de constitución, imágenes y reseña); (b) Agenda de Voluntariado (la fundación puede publicar sus necesidades de apoyo de voluntariado dando alternativas de franjas de horario para que los voluntarios puedan elegirlas y programarse); y (c) Gestión de Donaciones (las fundaciones necesitan apoyo financiero y en especie, y en la aplicación pueden publicar sus necesidades y recaudar las donaciones por parte de los usuarios).",
        "2. Interfaz Usuario (Donantes y Voluntarios): (a) Información de Intereses y Causas (el usuario puede filtrar la información de las fundaciones que van de acuerdo con sus intereses, municipios y causas); (b) Voluntariado y Servicio Social (los usuarios pueden agendarse como voluntarios y asistir a realizar horas de servicio social o apoyo comunitario, eligiendo la fundación a la que desean apoyar); y (c) Envío de Donaciones Económicas y en Especie (los usuarios pueden registrar y enviar donaciones a través de la aplicación con trazabilidad completa)."
    ]),
    ("P", "Para llevar esta propuesta al diseño ingenieril del sistema se aplicaron las cinco etapas de Design Thinking indicadas en la Guía de Emprendimiento (Universidad de Cundinamarca, 2024) en conjunto con la fase de Inicio de RUP:"),
    ("UL", [
        "1. Empatizar: Visitas, encuestas y entrevistas con los líderes de las cuatro fundaciones (Casa de los Abuelos en Machetá, Campamentos de Vida Nueva en Simijaca, Patitas Campesinas en La Calera y Mis Gotitas de Amor en Cajicá) para entender sus limitaciones de tiempo, presupuesto e internet.",
        "2. Definir: Identificación del problema central: las fundaciones rurales no logran conseguir suficientes donaciones ni voluntarios porque son invisibles fuera de su círculo cercano y no tienen cómo mostrar su gestión de forma estructurada.",
        "3. Idear: Planteamiento de una plataforma web gratuita donde converjan el mapa interactivo de fundaciones, el listado de necesidades con barra de avance, las convocatorias de voluntariado y los certificados de donación.",
        "4. Prototipar: Construcción del MVP en Angular y Python/Flask sobre una base de datos en 5FN con 34 tablas, desplegado en la nube en https://conexion-solidaria.onrender.com/login.",
        "5. Testear: Ejecución de quince casos de prueba funcional y de rendimiento con información real de las organizaciones de la Sabana."
    ]),

    ("H3", "3.7.1. Necesidades que atenderá la solución"),
    ("P", "El sistema resuelve cuatro tareas concretas: darle a cada fundación un perfil público verificado, mostrar sus necesidades de dinero o insumos con metas claras, permitir que los voluntarios se postulen según los cupos disponibles y generar el certificado en PDF de cada donación confirmada."),

    ("H3", "3.7.2. Requerimientos prioritarios del MVP"),
    ("P", "Los requerimientos implementados en el MVP son los doce Requerimientos Funcionales (RF01 a RF12) y los seis Requerimientos No Funcionales (RNF01 a RNF06) explicados en el marco ingenieril y detallados en el Anexo E."),

    ("H3", "3.7.3. Criterios de validación de la propuesta de valor"),
    ("P", "Para comprobar que el MVP cumple la propuesta de valor se midieron cinco indicadores: (1) el porcentaje de cobertura de las necesidades publicadas; (2) el tiempo de registro de una OSAL en tres pasos (menos de 5 minutos); (3) la velocidad de respuesta del servidor (menos de 57 ms y paquetes menores a 7,5 KB); (4) la generación del certificado PDF con código hash SHA-256 en el 100 % de las donaciones confirmadas; y (5) el reporte de impacto por cada uno de los 9 ODS."),

    ("H2", "3.8. Conclusiones del diagnóstico"),
    ("P", "El diagnóstico confirma que las pequeñas fundaciones rurales de la Sabana viven una brecha digital que frena su acceso a donaciones y voluntarios, tal como lo reflejan a nivel nacional el 36 % de falta de presupuesto y el 14 % de falta de personal técnico reportados por el DANE (2021). Esto demuestra la necesidad real de entregarles una plataforma web gratuita y fácil de manejar como Conexión Solidaria."),

    # =========================================================================
    # CAPÍTULO 4. MODELO DE NEGOCIO Y PROPUESTA DE VALOR
    # =========================================================================
    ("H1", "CAPÍTULO 4. MODELO DE NEGOCIO Y PROPUESTA DE VALOR"),

    ("H2", "4.1. Descripción del emprendimiento Conexión Solidaria"),
    ("P", "En este capítulo se presentan la identidad estratégica del emprendimiento, la ficha técnica del servicio, los nueve bloques del Modelo de Negocio Canvas y el esquema financiero que permite ofrecer la plataforma sin costo a las fundaciones rurales."),

    ("H3", "4.1.1. Concepto del emprendimiento"),
    ("P", "El proyecto Conexión Solidaria: Tecnología para el Cambio Social, formulado como Plan de Vida Emprendedor bajo el Acuerdo 012 de la Universidad de Cundinamarca, está enfocado en el fortalecimiento de Organizaciones Sin Ánimo de Lucro (OSAL) ubicadas en zonas rurales de la Sabana Norte y Centro del departamento de Cundinamarca. La propuesta contempla el desarrollo de una plataforma tecnológica accesible, orientada a facilitar la gestión de donaciones, voluntariado y comunicación comunitaria, permitiendo a las fundaciones publicar sus necesidades, promover sus proyectos sociales y fortalecer la interacción con donantes y voluntarios, a través de un modelo de emprendimiento social sostenible sin ánimo de lucro que permita a las OSAL acceder a la solución sin afectar su economía."),

    ("H3", "4.1.2. Misión"),
    ("P", "[[EDITAR]]Apoyar la gestión operativa, la visibilidad y el alcance comunitario de las Organizaciones Sin Ánimo de Lucro (OSAL) rurales de la Sabana Centro y Norte de Cundinamarca, por medio del desarrollo y entrega gratuita de una plataforma web sencilla y transparente que facilite la captación de donaciones, el agendamiento de voluntariado y el trabajo conjunto por el desarrollo sostenible.[[/EDITAR]]"),

    ("H3", "4.1.3. Visión"),
    ("P", "[[EDITAR]]Para el año 2029, ser la plataforma referente de conexión solidaria y apoyo tecnológico para el tercer sector en Cundinamarca, vinculando a más de ciento veinte fundaciones rurales verificadas con ciudadanos, universidades y empresas aliadas de la región.[[/EDITAR]]"),

    ("H3", "4.1.4. Principios y valores"),
    ("UL", [
        "Transparencia y verificación: Cada fundación registrada pasa por una revisión de sus documentos legales y cada donación tiene seguimiento de estado.",
        "Inclusión digital rural: El sistema se diseña para que cualquier líder comunitario pueda usarlo desde su celular sin necesitar conocimientos avanzados.",
        "Gratuidad para las OSAL: El uso de la plataforma para publicar causas, recibir donaciones, convocar voluntarios y expedir certificados no tiene ningún costo ni comisión para las fundaciones.",
        "Empatía y compromiso local: Valoración del trabajo silencioso que hacen las organizaciones veredales por su comunidad y su entorno.",
        "Protección de la información: Respeto estricto por la privacidad y el tratamiento legal de los datos personales de cada usuario."
    ]),

    ("H3", "4.1.5. Objetivos estratégicos"),
    ("UL", [
        "Objetivo Estratégico 1 (Cobertura Social): Vincular y verificar a 25 OSAL rurales en el Año 1, pasando a 60 en el Año 2 y a 120 en el Año 3 en los 18 municipios de la Sabana.",
        "Objetivo Estratégico 2 (Participación Ciudadana): Sumar en el primer año al menos 500 usuarios entre donantes y voluntarios, logrando cubrir más del 65 % de las necesidades publicadas.",
        "Objetivo Estratégico 3 (Sostenibilidad Financiera): Suscribir entre 5 y 16 convenios anuales de patrocinio RSE y subvenciones para cubrir todos los gastos de servidor y operación sin cobrar a las fundaciones.",
        "Objetivo Estratégico 4 (Desempeño Técnico): Mantener una disponibilidad en línea superior al 99 % y tiempos de respuesta menores a 200 ms."
    ]),

    ("H2", "4.2. Definición del servicio"),
    ("P", "El servicio principal se entrega a través de la aplicación web Conexión Solidaria, accesible desde cualquier navegador móvil o de computador sin necesidad de instalar programas adicionales."),

    ("H3", "4.2.1. Descripción de la plataforma digital"),
    ("P", "Conexión Solidaria reúne en un mismo sitio web un mapa interactivo de la Sabana Centro y Norte y un catálogo público de causas y convocatorias de voluntariado, junto con paneles internos según el rol de cada usuario (Administrador OSAL, Donante, Voluntario y Superadministrador)."),

    ("H3", "4.2.2. Servicios ofrecidos"),
    ("P", "La plataforma integra seis funciones principales detalladas en la Ficha Técnica del Servicio (Tabla 9), siguiendo la estructura de la Guía ADOr006_V10 (Universidad de Cundinamarca, 2024):"),
    ("TABLE", {
        "title": "Tabla 9. Ficha técnica del servicio digital Conexión Solidaria",
        "headers": ["Atributo Técnico / Comercial", "Especificación Detallada del Servicio"],
        "rows": [
            ["Nombre comercial del servicio", "Plataforma Web de Articulación Social Conexión Solidaria (Versión MVP 1.0)."],
            ["Categoría del emprendimiento", "Emprendimiento Social de Base Tecnológica (Software como Servicio Social - Social SaaS)."],
            ["Usuarios principales", "Organizaciones Sin Ánimo de Lucro (OSAL) rurales, Donantes (personas naturales y empresas), Voluntarios ciudadanos y Aliados institucionales."],
            ["Módulos y servicios incluidos", "(1) Micrositio y perfil institucional verificado para cada OSAL; (2) Mapa interactivo georreferenciado por municipio y ODS; (3) Publicación y control de metas de necesidades en dinero y especie; (4) Convocatoria y agendamiento de voluntariado por cupos; (5) Registro trazable de donaciones y emisión de certificado PDF con código hash; (6) Tablero de indicadores de impacto social."],
            ["Tecnología y arquitectura", "Frontend SPA en Angular 17 + Leaflet; Backend API REST en Python 3.12 / Flask; Base de datos relacional en 5FN (34 tablas) sobre SQLAlchemy (SQLite/MySQL); Seguridad JWT + PBKDF2-SHA256."],
            ["Desempeño y accesibilidad", "Optimizado para redes móviles rurales 3G/4G (latencia media < 57 ms; peso de respuesta JSON < 7,5 KB); diseño responsivo compatible con estándares WCAG 2.2 nivel AA."],
            ["Presentación y canal de entrega", "Servicio 100 % digital desplegado en producción en la nube (https://conexion-solidaria.onrender.com/login), accesible mediante navegador web (HTTPS) desde teléfonos inteligentes, tabletas o computadores sin requerir instalación de aplicativos pesados."],
            ["Condiciones económicas de acceso", "Servicio básico 100 % gratuito (tarifa $0 COP y comisión 0 %) para todas las OSAL rurales verificadas, donantes ciudadanos y voluntarios."]
        ],
        "note": "Nota. Elaboración propia siguiendo el formato de ficha técnica de servicio de la Guía ADOr006_V10 (Universidad de Cundinamarca, 2024)."
    }),

    ("H3", "4.2.3. Usuarios y beneficiarios"),
    ("P", "Es importante distinguir entre usuarios de la plataforma y beneficiarios finales: los usuarios directos son los representantes de las OSAL, los donantes, los voluntarios y las empresas aliadas que entran al sistema; los beneficiarios finales son los adultos mayores, niños, jóvenes en rehabilitación, familias campesinas y animales rescatados que reciben las ayudas y el tiempo de voluntariado gestionados por medio de la aplicación."),

    ("H3", "4.2.4. Alcance del servicio gratuito"),
    ("P", "Todas las funciones que necesita una fundación rural para operar en Conexión Solidaria son gratuitas de forma permanente: registro y validación de su perfil, aparición en el mapa de la Sabana, publicación de campañas y necesidades en dinero o especie, creación de convocatorias de voluntariado, recepción del 100 % de las donaciones sin descuentos, descarga de certificados en PDF y consulta del tablero de métricas."),

    ("H3", "4.2.5. Propuesta de valor"),
    ("P", "La propuesta de valor articula las dos interfaces centrales del sistema para beneficiar a los tres actores del ecosistema: en la Interfaz Fundaciones, las organizaciones rurales publican sin costo su causa social, su ubicación en el mapa, sus necesidades concretas de dinero o insumos y sus franjas de horario para voluntariado; en la Interfaz Usuario, los donantes y voluntarios filtran las fundaciones según sus intereses, agendan sus horas de servicio social o apoyo voluntario y registran sus donaciones conociendo el avance real de cada meta; y para las empresas aliadas, el sistema entrega reportes verificables de impacto por ODS junto con el certificado tributario de donación en PDF."),

    ("H2", "4.3. Modelo de negocio Canvas"),
    ("P", "A partir del diagnóstico del Capítulo 3 y siguiendo el modelo de Osterwalder y Pigneur (2010) aplicado a iniciativas sociales (Palacios Inocencio, 2021; Universidad de Cundinamarca, 2024), la Tabla 10 presenta los nueve bloques del Lienzo Canvas de Conexión Solidaria."),
    ("TABLE", {
        "title": "Tabla 10. Lienzo del Modelo de Negocio Social (Business Model Canvas) de Conexión Solidaria",
        "headers": ["Bloque del Lienzo Canvas", "Definición Estratégica Sustentada en el Diagnóstico", "Trazabilidad con el MVP y el Plan"],
        "rows": [
            ["1. Segmentos de Clientes y Beneficiarios", "• Beneficiarias directas (Usuarios sin costo): OSAL rurales y periféricas de los 18 municipios de Sabana Centro y Norte.\n• Usuarios solidarios: Ciudadanos donantes (dinero/especie) y voluntarios (estudiantes/profesionales).\n• Clientes financiadores (B2B/Institucional): Empresas del corredor industrial con presupuestos RSE, universidades y entidades públicas/cooperación.", "Sección 3.2 y 3.6; Roles RBAC del MVP (RF01, RF02)."],
            ["2. Propuesta de Valor", "• Para OSAL rurales: Plataforma web 100 % gratuita, ligera y sin comisiones para visibilizar causas, captar donaciones, agendar voluntarios y emitir certificados.\n• Para Donantes y Voluntarios: Directorio georreferenciado de fundaciones verificadas legalmente, con metas transparentes y trazabilidad del aporte.\n• Para Empresas RSE: Canal confiable de inversión social regional con reportes de impacto por ODS y certificados tributarios RTE.", "Sección 4.2.5; Mapa (RF03), Donaciones (RF07-RF09), Voluntariado (RF05-RF06) y Dashboard ODS (RF10)."],
            ["3. Canales", "• Canal digital principal: Aplicación web responsiva Conexión Solidaria (acceso móvil y escritorio).\n• Canales de difusión y atracción: Redes sociales institucionales, WhatsApp directo con líderes OSAL, oficinas de Proyección Social y Bienestar Universitario, y gremios empresariales de la Sabana.", "Sección 5.3; Interfaz Angular Mobile-First (RNF02)."],
            ["4. Relaciones con los Usuarios", "• Con OSAL rurales: Acompañamiento cercano en registro y verificación documental, soporte asistido y co-creación comunitaria.\n• Con Donantes y Voluntarios: Autoservicio digital transparente, notificaciones de estado del aporte y entrega inmediata de certificado verificable.\n• Con Aliados RSE: Atención ejecutiva personalizada y entrega de reportes consolidados de impacto territorial.", "Sección 5.2; Flujos de validación (CU01, CU06) y código hash SHA-256."],
            ["5. Fuentes de Ingresos y Financiación", "• Gratuidad total (0 % cobro) para las OSAL, donantes individuales y voluntarios.\n• Sostenibilidad operativa de la plataforma mediante cuatro fuentes institucionales: (1) Patrocinios corporativos RSE y sello de Empresa Aliada en la plataforma (55 %); (2) Subvenciones, convocatorias MinTIC/Gobernación y cooperación (25 %); (3) Convenios de analítica e impacto territorial con universidades/entidades (12 %); y (4) Aportes voluntarios de sostenimiento tecnológico (8 %).", "Secciones 4.4 y 5.6; Anexo I y Anexo J."],
            ["6. Recursos Clave", "• Tecnológicos: Código fuente del MVP (Angular + Flask), base de datos en 5FN (34 tablas), infraestructura cloud y dominio web.\n• Humanos: Equipo emprendedor de Ingeniería de Sistemas, red de practicantes/voluntarios universitarios y asesoría contable/jurídica ESAL.\n• Intangibles: Metodología de verificación documental PGVTT y alianzas académicas y comunitarias en la Sabana.", "Secciones 2.6, 5.1 y 5.4; Anexos F, G y H."],
            ["7. Actividades Clave", "• Desarrollo, mantenimiento evolutivo, ciberseguridad y operación cloud de la plataforma.\n• Verificación documental de legalidad de las OSAL (RUT, Cámara de Comercio) y auditoría de campañas.\n• Acompañamiento y alfabetización digital a líderes de fundaciones rurales.\n• Gestión comercial de alianzas RSE, convenios universitarios y difusión regional.", "Sección 5.2 y 5.8; Cronograma (Anexo K)."],
            ["8. Aliados Clave", "• Instituciones de Educación Superior de la región (Universidad de Cundinamarca y campus de Sabana Centro).\n• Empresas y parques industriales de Sabana Centro y Norte (programas RSE).\n• Cámaras de Comercio, alcaldías municipales y redes de fundaciones (AFE / colectivos locales).\n• Proveedores de infraestructura tecnológica cloud (Render, GitHub, Cloudflare).", "Secciones 1.6, 3.2.4 y 5.3.5."],
            ["9. Estructura de Costos", "• Estructura Lean de bajo costo operativo (Low-OPEX) gracias a tecnologías Open Source y arquitectura LBRSA:\n  - Costos de infraestructura cloud, base de datos, dominio y SSL ($2.580.000 COP Año 1).\n  - Costos de formalización jurídica ESAL, soporte técnico, difusión digital y acompañamiento territorial.\n  - Costo de desarrollo inicial cubierto como aporte intelectual del equipo emprendedor.", "Sección 5.6; Tablas financieras (Anexo I y Anexo J)."]
        ],
        "note": "Nota. Elaboración propia aplicando el modelo de Osterwalder y Pigneur (2010) a los hallazgos del diagnóstico regional."
    }),

    ("H3", "4.3.1. Segmentos de clientes y beneficiarios"),
    ("P", "El modelo separa claramente a las fundaciones rurales como beneficiarias sin costo (pues el 36 % no tiene recursos para invertir en tecnología), a los ciudadanos donantes y voluntarios como usuarios solidarios, y a las empresas con programas de RSE como los clientes institucionales que financian la operación del portal."),

    ("H3", "4.3.2. Propuesta de valor"),
    ("P", "La propuesta de valor responde directamente a lo hallado en terreno: le quita a las fundaciones la carga de llevar todo en papel o en chats sueltos, le da seguridad al ciudadano sobre a dónde va su ayuda y le permite a las empresas patrocinadoras demostrar su aporte a los ODS en la región."),

    ("H3", "4.3.3. Canales"),
    ("P", "El canal principal es la aplicación web Conexión Solidaria, que abre rápido desde cualquier teléfono sin ocupar memoria. Para llegar a las fundaciones y a la comunidad nos apoyamos en visitas y contacto por WhatsApp con los líderes veredales, convenios con las oficinas de Bienestar y Proyección Social de las universidades y reuniones directas con las áreas de sostenibilidad de las empresas."),

    ("H3", "4.3.4. Relaciones con los usuarios"),
    ("P", "Con los líderes de las fundaciones rurales el trato es cercano y asistido para ayudarles a subir su información sin complicaciones técnicas (Winocur, 2007; Escobar Cazal & Escobar Reyes, 2017). Con los donantes y voluntarios la relación se basa en cuentas claras: pueden ver en pantalla cuánto ha avanzado cada meta y descargar el certificado con código hash de su donación."),

    ("H3", "4.3.5. Fuentes de ingresos y financiación"),
    ("P", "Conexión Solidaria no les cobra mensualidades a las fundaciones ni se queda con ningún porcentaje de las donaciones que la gente les envía. Los gastos de mantener el sistema en línea se cubren con cuatro fuentes institucionales: patrocinios anuales de empresas aliadas (RSE), convocatorias y subvenciones de innovación social, convenios de reportes territoriales y aportes voluntarios dirigidos al sostenimiento técnico de la plataforma."),

    ("H3", "4.3.6. Recursos clave"),
    ("P", "Los recursos principales son el software ya construido (MVP en Angular y Flask con su base de datos de 34 tablas en 5FN), el servidor en la nube, el trabajo de ingeniería de los dos cofundadores y el proceso de revisión documental que respalda el sello de verificación de cada fundación."),

    ("H3", "4.3.7. Actividades clave"),
    ("P", "La operación diaria se concentra en cuatro tareas: revisar los documentos legales de las OSAL que piden entrar al sistema, mantener el servidor y la base de datos seguros y en línea, capacitar a los representantes de las fundaciones rurales y gestionar los convenios con universidades y empresas patrocinadoras."),

    ("H3", "4.3.8. Aliados clave"),
    ("P", "Los aliados principales (ODS 17) son la Universidad de Cundinamarca y demás universidades de la Sabana (por su aporte de voluntarios y practicantes), las empresas de los parques industriales de la provincia (como patrocinadoras RSE), las alcaldías municipales y las Cámaras de Comercio."),

    ("H3", "4.3.9. Estructura de costos"),
    ("P", "Al usar herramientas de código abierto y una arquitectura ligera, los gastos fijos de servidor, base de datos y dominio web son bajos ($2.580.000 COP al año en el Año 1). Así, la mayor parte del presupuesto se destina al soporte comunitario, la verificación de fundaciones y la difusión regional."),

    ("H2", "4.4. Estrategia de sostenibilidad del emprendimiento"),
    ("P", "Un punto clave en cualquier proyecto social es explicar de dónde sale el dinero para operar sin cobrarle a la población vulnerable y sin mezclar la plata de funcionamiento de la plataforma con las donaciones que van para las fundaciones."),

    ("H3", "4.4.1. Modelo de financiación"),
    ("P", "[[EDITAR]]El sostenimiento económico funciona por subsidio cruzado: las fundaciones rurales usan la plataforma totalmente gratis, mientras que los costos del servidor, el soporte y la verificación los cubren empresas patrocinadoras (RSE) y subvenciones que buscan apoyar el desarrollo social de la Sabana.[[/EDITAR]]"),

    ("H3", "4.4.2. Donaciones y aportes de aliados"),
    ("P", "Los recursos para sostener a Conexión Solidaria entran por tres vías: (a) Planes anuales de patrocinio RSE (Bronce, Plata y Oro) para empresas de la región que reciben presencia de marca en el portal y reportes de impacto; (b) convocatorias públicas o privadas de innovación social; y (c) aportes voluntarios para el mantenimiento tecnológico del portal."),

    ("H3", "4.4.3. Alianzas con empresas y otras instituciones"),
    ("P", "Además del apoyo económico, los convenios con las universidades de Chía, Cajicá y Zipaquirá permiten vincular estudiantes de práctica social de Ingeniería de Sistemas, Administración y Comunicación para apoyar el acompañamiento digital a las fundaciones rurales, manteniendo bajos los costos fijos."),

    ("H3", "4.4.4. Sostenibilidad de la operación tecnológica"),
    ("P", "Como el software fue desarrollado por el propio equipo emprendedor sobre tecnologías libres (Python, Flask, Angular y SQLAlchemy), no hay que pagar licencias por usuario en dólares. El costo mensual del servidor cloud y el dominio en el primer año es de apenas $215.000 COP mensuales ($2.580.000 COP al año), una cifra fácil de cubrir incluso en el escenario financiero más conservador."),

    ("H3", "4.4.5. Diferenciación entre recursos operativos y donaciones para las organizaciones beneficiarias"),
    ("P", "Siguiendo los principios de transparencia contable en entidades sin ánimo de lucro (Aliaga Bernal, 2009), la Tabla 11 deja en claro la separación total entre las donaciones para las fundaciones y los recursos operativos de Conexión Solidaria:"),
    ("TABLE", {
        "title": "Tabla 11. Matriz de separación contable, jurídica y operativa entre los recursos de Conexión Solidaria y las donaciones a las OSAL",
        "headers": ["Criterio de Separación", "Flujo 1: Donaciones para las OSAL Beneficiarias", "Flujo 2: Recursos Operativos de Conexión Solidaria"],
        "rows": [
            ["Titular y destinatario legal del recurso", "Cada Organización Sin Ánimo de Lucro (OSAL) rural registrada y verificada en la plataforma.", "La entidad gestora del emprendimiento Conexión Solidaria."],
            ["Origen de los recursos", "Ciudadanos donantes y empresas que seleccionan una campaña o necesidad específica de una fundación en el catálogo o mapa.", "Patrocinios corporativos RSE institucionales, subvenciones de innovación (Grants) y convenios de sostenibilidad del portal."],
            ["Canal de recepción y custodia", "Transferencia directa a la cuenta bancaria/billetera de la OSAL beneficiaria o entrega física directa de los insumos en especie en su sede.", "Cuenta bancaria institucional propia de Conexión Solidaria destinada exclusivamente al presupuesto operativo del sistema."],
            ["Comisión o retención por uso de la plataforma", "0 % (Cero comisión). El 100 % íntegro del dinero o de los bienes donados llega a la fundación beneficiaria.", "No aplica (constituye el ingreso propio para cubrir hosting, soporte, verificación y mantenimiento)."],
            ["Emisión del Certificado Tributario de Donación (RTE)", "Emitido a nombre y bajo el NIT de la OSAL beneficiaria receptora real del aporte (generado digitalmente a través del módulo RF09).", "Emitido por Conexión Solidaria únicamente a las empresas patrocinadoras que financian la operación de la plataforma."],
            ["Registro en la base de datos (5FN)", "Tablas transaccionales necesidades_recurso, donaciones_registradas, detalle_donacion_especie y certificados_donacion.", "Contabilidad administrativa interna de Conexión Solidaria (Presupuesto operativo Anexo J)."]
        ],
        "note": "Nota. Elaboración propia conforme a los principios contables de entidades no lucrativas (Aliaga Bernal, 2009) y el Estatuto Tributario colombiano."
    }),

    ("H2", "4.5. Innovación y diferenciación"),
    ("P", "Tomando como referencia el Manual de Oslo (OCDE & Eurostat, 2018) y la Guía ADOr006_V10 (Universidad de Cundinamarca, 2024), se puntualiza qué hace innovadora a la propuesta y cuál es su aporte desde la ingeniería."),

    ("H3", "4.5.1. Elementos innovadores de la propuesta"),
    ("P", "Según el Manual de Oslo (OCDE & Eurostat, 2018), el proyecto combina una innovación de servicio con una innovación de proceso aplicada al sector social rural. Sus cuatro puntos diferenciadores son: una arquitectura web de bajo consumo de datos pensada para veredas con mala señal; la unión en una sola plataforma de mapa por ODS, donaciones en dinero e insumos y agenda de voluntariado; la confirmación verificada de aportes con código hash SHA-256 en los certificados PDF; y un modelo sostenible que no les cobra nada a las fundaciones."),

    ("H3", "4.5.2. Ventajas frente a las alternativas existentes"),
    ("P", "A diferencia de Facebook o WhatsApp, aquí los pedidos de ayuda no se pierden en un chat, sino que tienen una meta numérica, una barra de avance y un certificado descargable. Y frente a páginas como GoFundMe, no se les descuenta comisión a las fundaciones y sí se pueden gestionar donaciones de alimentos o insumos físicos y turnos de voluntariado."),

    ("H3", "4.5.3. Aporte de conocimiento"),
    ("P", "[[EDITAR]]Desde la Ingeniería de Sistemas, el trabajo aporta un modelo de base de datos en Quinta Forma Normal (5FN) con 34 tablas diseñado específicamente para la operación legal y transaccional de las fundaciones en Colombia, junto con la demostración práctica de una arquitectura web ligera que responde en menos de 57 milisegundos.[[/EDITAR]]"),

    ("H3", "4.5.4. Potencial de escalabilidad y replicabilidad"),
    ("P", "Como los municipios y departamentos están parametrizados en tablas de catálogo dentro de la base de datos, el mismo sistema que hoy cubre los dieciocho municipios de Sabana Centro y Norte puede abrirse a otras provincias de Cundinamarca (como Ubaté, Gualivá o Sumapaz) simplemente agregando los nuevos municipios en el panel de administración."),

    ("H2", "4.6. Conclusiones del modelo de negocio"),
    ("P", "El modelo Canvas y el esquema de separación de cuentas muestran que es totalmente viable mantener en línea una plataforma moderna y gratuita para las fundaciones rurales de la Sabana, respaldada por patrocinios institucionales y costos operativos bajos.")
]

