# -*- coding: utf-8 -*-
"""
Generador de:
1. Los 4 Audios MP3 de Sustentación y Entrenamiento (Fluid, Natural, Sin Tecnicismos de Código, Con los 12 RF, 6 RNF y 10 Casos de Uso).
2. El Audiolibro Completo Narrado del Documento Final de Grado (Capítulos 1 al 5 y Cierre) en un solo archivo MP3 consolidado y también por capítulos.

Voces Neuronales en Español de Colombia:
- Angélica: es-CO-SalomeNeural
- Oscar: es-CO-GonzaloNeural
- Jurado (Simulacro): es-MX-JorgeNeural
"""

import asyncio
import os
import re
import edge_tts

OUT_DIR = r"c:\Users\ingor\conexion-solidaria\docs\audios_sustentacion"
os.makedirs(OUT_DIR, exist_ok=True)

VOICE_ANGELICA = "es-CO-SalomeNeural"
VOICE_OSCAR = "es-CO-GonzaloNeural"
VOICE_JURADO = "es-MX-JorgeNeural"

# =============================================================================
# AUDIO 1: SUSTENTACIÓN FLUIDA - PARTE 1: EL PROBLEMA HUMANO, ENCUESTAS Y CANVAS
# =============================================================================
AUDIO_1_SEGMENTS = [
    (
        VOICE_ANGELICA,
        "Sustentación de proyecto de grado: Conexión Solidaria, Tecnología para el Cambio Social. "
        "Parte uno: El origen del proyecto, el diagnóstico en la Sabana de Cundinamarca, los resultados de nuestras encuestas y el Modelo de Negocio Social."
    ),
    (
        VOICE_ANGELICA,
        "Buenos días, respetados jurados evaluadores, ingenieros Jorge Iván Ortiz y Jairo Fernando Henao González, docentes y compañeros. "
        "Mi nombre es Angélica Rosa Olier Quiroga y, junto con mi compañero y cofundador Oscar Giovanni Robayo Olaya, les presentamos nuestro proyecto de grado en la Ruta de Emprendimiento e Innovación bajo el Acuerdo cero doce: Conexión Solidaria, Tecnología para el Cambio Social. "
        "Conexión Solidaria no nació simplemente como un requisito académico, sino de una experiencia personal. "
        "Participando en jornadas de voluntariado y recolección de ayudas en municipios de nuestra región, conocimos de cerca a pequeñas fundaciones rurales que trabajan todos los días por adultos mayores campesinos, niños de primera infancia, jóvenes en rehabilitación y animales abandonados. "
        "Nos impactó ver cómo hacen tanto con tan pocos recursos, pero sobre todo cómo su trabajo se queda invisible porque no cuentan con herramientas digitales ni con los medios para darse a conocer fuera de su vereda. "
        "Dentro del Modelo Educativo Digital Transmoderno, MEDIT, de la Universidad de Cundinamarca, nuestro Plan de Vida Emprendedor une la empatía ciudadana con la sostenibilidad ambiental del Cero Papel y el desarrollo de una plataforma web gratuita para estas organizaciones."
    ),
    (
        VOICE_ANGELICA,
        "Al investigar a fondo esta problemática en los dieciocho municipios de Sabana Centro y Sabana Norte de Cundinamarca, encontramos que lo que vimos en las veredas coincide con las cifras nacionales. "
        "Según el DANE, las entidades sin ánimo de lucro son el sector con mayor rezago tecnológico en Colombia: el treinta y seis por ciento no invierte en tecnología ni innovación por falta de recursos económicos, y el catorce por ciento porque no tiene personal técnico calificado. "
        "Además, según la Asociación de Fundaciones Familiares y Empresariales, AFE, la gran mayoría son organizaciones pequeñas de menos de diez personas y poco voluntariado formal, aunque el noventa y cuatro por ciento trabaja por cumplir los Objetivos de Desarrollo Sostenible en su comunidad. "
        "De ahí surgió nuestra pregunta central: ¿cómo crear una solución tecnológica sencilla y gratuita para las fundaciones rurales de la Sabana con acceso limitado a internet, que les permita comunicar sus causas, organizar a sus voluntarios y recibir donaciones transparentes, bajo un modelo de emprendimiento social que sea sostenible sin cobrarles a ellas?"
    ),
    (
        VOICE_OSCAR,
        "Para responder a esa pregunta, trazamos como objetivo general diseñar el plan de emprendimiento social para crear una fundación tecnológica que desarrolle y entregue gratuitamente este sistema de información a las fundaciones rurales de la Sabana Centro y Norte. "
        "Organizamos el proyecto en seis objetivos específicos acoplados con las cuatro fases de la metodología de ingeniería RUP: "
        "primero, diagnosticar el mercado y levantar los requerimientos en la fase de Inicio; "
        "segundo, diseñar el modelo estratégico Canvas; "
        "tercero, definir la arquitectura, los prototipos visuales, los casos de uso y la base de datos en la fase de Elaboración; "
        "cuarto, construir de forma modular el Producto Mínimo Viable en la fase de Construcción; "
        "quinto, validar su funcionamiento y rapidez en la fase de Transición; "
        "y sexto, estructurar los planes organizacional, operativo, de mercadeo y financiero para sostener el servicio en el tiempo."
    ),
    (
        VOICE_ANGELICA,
        "En nuestro estudio de campo aplicamos dos encuestas digitales en Google Forms para escuchar a las dos partes: a las fundaciones y a los ciudadanos. "
        "Por el lado de las organizaciones sociales, encuestamos y visitamos a cuatro fundaciones reales de Cundinamarca: "
        "la Fundación Mis Gotitas de Amor en Cajicá, que educa a niños de primera infancia; "
        "la Fundación Casa de los Abuelos Campesinos en Machetá, que cuida a adultos mayores del campo; "
        "la Fundación Campamentos de Vida Nueva en Simijaca, que acompaña a jóvenes en rehabilitación y familias vulnerables; "
        "y la Fundación Patitas Campesinas en La Calera, dedicada al rescate y esterilización de animales en zonas veredales. "
        "¿Qué encontramos en ellas? Primero, que ninguna utiliza una página web propia para publicar sus necesidades o buscar voluntarios; se defienden como pueden con radio local, perifoneo, cadenas de WhatsApp o redes sociales sin seguimiento, y la respuesta del público que perciben es baja, de apenas dos coma setenta y cinco sobre cinco. "
        "Segundo, el cien por ciento sobrevive gracias a donaciones de personas naturales y al trabajo voluntario, sin apoyo de empresas privadas. "
        "Tercero, al pedirles que ordenaran sus mayores dolores de cabeza de uno a cinco, el obstáculo número uno fue la falta de recursos económicos con uno coma veinticinco, seguido por la baja visibilidad pública con dos coma veinticinco y la dificultad para conseguir voluntarios con dos coma cincuenta. "
        "Y cuarto, el cien por ciento nos dijo que adoptaría de inmediato una plataforma gratuita como Conexión Solidaria, pidiendo sobre todo tres cosas: poder publicar necesidades concretas de dinero o insumos, una agenda para organizar voluntarios por horarios y un perfil verificado que dé confianza."
    ),
    (
        VOICE_ANGELICA,
        "Luego salimos a preguntarle a la comunidad. Aplicamos nuestra encuesta de percepción ciudadana por WhatsApp en municipios de la Sabana y el norte de Bogotá, logrando ciento setenta respuestas válidas, con una participación muy equilibrada: cincuenta y cuatro coma siete por ciento de zona urbana y cuarenta y cinco coma tres por ciento de veredas y zonas rurales. "
        "Los resultados de estas ciento setenta personas confirmaron exactamente el otro lado del problema: "
        "Primero, casi dos tercios de la gente, el sesenta y cuatro coma siete por ciento, no sabe qué actividades hacen las fundaciones de su propio municipio o no conoce ninguna. No es que la gente no quiera ayudar, es que no sabe que existen ni qué necesitan. "
        "Segundo, cuando la gente ayuda, no solo dona dinero: las dos formas de apoyo más frecuentes en el último año fueron el voluntariado presencial en campo con treinta y cinco coma tres por ciento y la donación de insumos físicos como alimentos, ropa o materiales con treinta y dos coma cuatro por ciento. "
        "Tercero, encontramos el dato más importante para diseñar nuestro software: el cincuenta y ocho coma dos por ciento de los ciudadanos exige transparencia total en el uso de los recursos para animarse a donar, y el veintiuno coma ocho por ciento exige claridad en las tareas que va a realizar como voluntario. Es decir, ocho de cada diez personas condicionan su ayuda a la confianza y al orden. "
        "Y cuarto, el noventa y cinco coma nueve por ciento, ciento sesenta y tres de las ciento setenta personas, afirmó que sí usaría Conexión Solidaria para donar o postularse como voluntario."
    ),
    (
        VOICE_ANGELICA,
        "Con estos hallazgos estructuramos nuestra propuesta de valor y el Modelo de Negocio Canvas, alineados con nueve Objetivos de Desarrollo Sostenible: cinco de forma directa por reducir la brecha digital y crear alianzas regionales, y cuatro a través de las causas de alimentación, salud, educación y medio ambiente de las fundaciones. "
        "¿Cómo logramos que la plataforma sea cien por ciento gratuita y sin comisiones para las fundaciones rurales, pero al mismo tiempo sostenible? "
        "Mediante un modelo de subsidio cruzado y una separación total de cuentas: "
        "Por un lado, el cien por ciento de las donaciones en dinero o en especie que hacen los ciudadanos va directo a la cuenta o a la sede de cada fundación rural, sin pasar por nosotros y sin descontarles un solo peso, y el certificado tributario sale a nombre de la fundación que recibe la ayuda. "
        "Por otro lado, los costos de mantener encendido el servidor, verificar la legalidad de las fundaciones y acompañarlas se cubren por cuatro fuentes institucionales: "
        "la principal son los planes anuales de patrocinio de Responsabilidad Social Empresarial, en niveles Bronce, Plata y Oro, para empresas del corredor industrial de la Sabana, quienes además obtienen un descuento tributario del veinticinco por ciento en su impuesto de renta al apoyar nuestra fundación; "
        "complementados con convocatorias de innovación social, convenios de reportes de impacto territorial con universidades y alcaldías, y aportes voluntarios de sostenimiento."
    ),
]

# =============================================================================
# AUDIO 2: SUSTENTACIÓN FLUIDA - PARTE 2: REQUISITOS, 10 CASOS DE USO, ARQUITECTURA, 5FN Y PRUEBAS
# =============================================================================
AUDIO_2_SEGMENTS = [
    (
        VOICE_OSCAR,
        "Sustentación de proyecto de grado: Conexión Solidaria. "
        "Parte dos: Requisitos funcionales y no funcionales, los diez casos de uso principales, cómo funciona la arquitectura entre el Frontend y el Backend, la base de datos de treinta y cuatro tablas y las pruebas en la nube."
    ),
    (
        VOICE_OSCAR,
        "Muchas gracias, Angélica. Pasaré ahora a explicar cómo convertimos todas esas necesidades de las fundaciones y de los ciudadanos en una solución de ingeniería de software real y funcional. "
        "En la fase de Inicio de la metodología RUP definimos cinco roles claros dentro de la plataforma: el Visitante público, el Donante, el Voluntario, el Administrador de cada fundación y el Superadministrador del sistema. "
        "A partir de las encuestas levantamos doce Requisitos Funcionales y seis Requisitos No Funcionales. "
        "Los seis Requisitos No Funcionales marcan la calidad del sistema: "
        "primero, rendimiento ultraligero para que la página cargue rápido incluso en veredas con señal celular tres G regular; "
        "segundo, facilidad de uso y accesibilidad visual con alto contraste bajo el estándar WCAG dos punto dos, pensado para líderes comunitarios que usan el celular y no son expertos en tecnología; "
        "tercero, separación limpia y modular entre la parte visual y el servidor; "
        "cuarto, integridad de la información en una base de datos sin datos repetidos; "
        "quinto, seguridad en contraseñas, sesiones y cumplimiento estricto de la Ley mil quinientos ochenta y uno de protección de datos personales; "
        "y sexto, portabilidad en la nube con muy bajo costo mensual de servidor."
    ),
    (
        VOICE_ANGELICA,
        "Por su parte, los doce Requisitos Funcionales se traducen en los diez Casos de Uso principales que cualquier usuario vive paso a paso dentro de Conexión Solidaria: "
        "En el Caso de Uso uno, que cumple el requisito funcional uno, el director de una fundación rural se registra en un asistente muy sencillo de solo tres pasos: primero pone los datos básicos y el NIT de la organización; segundo, ubica su municipio y vereda en el mapa de la Sabana; y tercero, selecciona qué Objetivos de Desarrollo Sostenible atiende, adjunta su RUT y Cámara de Comercio, y marca la autorización obligatoria de tratamiento de datos personales de la Ley mil quinientos ochenta y uno. "
        "Para proteger la confianza de los ciudadanos, la fundación no aparece publicada de inmediato: entra en estado Pendiente hasta que el administrador verifica sus documentos legales y le activa el sello de fundación verificada. "
        "En el Caso de Uso dos, requisito funcional dos, cada usuario inicia sesión segura y el sistema le habilita únicamente las pantallas y permisos que corresponden a su rol. "
        "En el Caso de Uso tres, requisito funcional tres, cualquier ciudadano entra al directorio y al mapa interactivo de la Sabana Centro y Norte, donde puede explorar los puntos georreferenciados de cada fundación y filtrar por municipio, por categoría social o por Objetivo de Desarrollo Sostenible."
    ),
    (
        VOICE_OSCAR,
        "Una vez la fundación está verificada, entran en acción los Casos de Uso cuatro y cinco, que responden a los requisitos funcionales cuatro y once: "
        "La fundación crea sus campañas sociales y publica sus necesidades específicas con una meta numérica clara: puede pedir tanto apoyo económico en pesos como insumos físicos en especie medidos por unidades concretas —por ejemplo, quinientos kilos de alimento concentrado, ochenta mercados campesinos, ciento veinte paquetes de pañales para adulto mayor o sesenta kits escolares—, indicando el nivel de urgencia o activando alertas de centros de acopio cuando ocurre una emergencia en el municipio. "
        "Luego vienen los Casos de Uso seis y siete, que cumplen los requisitos funcionales siete, ocho y nueve, y que resuelven el mayor freno que encontramos en la encuesta ciudadana, donde el cincuenta y ocho coma dos por ciento exigió transparencia en el uso de los recursos: "
        "¿Cómo funciona nuestro protocolo de confirmación bilateral de donaciones? "
        "Cuando un ciudadano decide donar dinero o insumos a una necesidad en la plataforma, registra su aporte y el sistema le entrega un código único de seguimiento en estado Pendiente. "
        "Pero atención a este detalle clave: en ese momento la barra de progreso de la fundación todavía NO sube. ¿Por qué? Para evitar que registros falsos o promesas no entregadas engañen a la comunidad. "
        "Solo cuando la fundación revisa que el dinero o los insumos físicos efectivamente llegaron a su sede y confirma la recepción en su panel, el sistema cambia el estado a Confirmada, actualiza automáticamente el porcentaje alcanzado de la meta, deja el registro en la bitácora de transparencia y habilita el Caso de Uso siete: la descarga inmediata del Certificado Tributario de Donación en formato PDF, el cual lleva impreso un sello digital único de verificación para efectos contables ante la DIAN."
    ),
    (
        VOICE_ANGELICA,
        "Del mismo modo, los Casos de Uso ocho y nueve cumplen los requisitos funcionales cinco y seis para organizar el voluntariado, que era la otra gran exigencia de claridad de la encuesta: "
        "En el Caso de Uso ocho la fundación publica una convocatoria de voluntariado especificando qué actividad se va a realizar, en qué vereda o municipio, en qué fecha y horario, qué habilidades se requieren y cuántos cupos exactos hay disponibles. "
        "En el Caso de Uso nueve el voluntario revisa la jornada y se postula; cuando la fundación aprueba su participación, el sistema descuenta automáticamente el cupo disponible en tiempo real para que nunca haya desorden ni sobrecupos en las brigadas. "
        "Finalmente, el Caso de Uso diez cubre los requisitos funcionales diez y doce: presenta el tablero de indicadores de impacto social en tiempo real —mostrando el porcentaje global de cobertura de necesidades y cuántas fundaciones y campañas están aportando a cada uno de los nueve Objetivos de Desarrollo Sostenible—, junto con el panel de gobernanza desde donde el Superadministrador aprueba nuevas fundaciones y audita la plataforma."
    ),
    (
        VOICE_OSCAR,
        "Ahora bien, ¿qué tecnologías usamos por detrás para construir todo esto y cómo se conecta el Frontend con el Backend? "
        "Pensando en la conectividad rural y en el bolsillo de la fundación, diseñamos un Monolito Modular Desacoplado con una arquitectura de bajo consumo de datos dividida en tres capas de código abierto: "
        "La primera capa es el Frontend, es decir, la interfaz visual que ve el usuario en su celular o computador. La desarrollamos en Angular diecisiete con carga diferida de pantallas, lo que significa que el celular solo descarga la sección que la persona está viendo en ese instante, e integramos los mapas interactivos con Leaflet y OpenStreetMap, que son libres, muy livianos y no cobran tarifas en dólares como Google Maps. "
        "La segunda capa es el Backend o servidor donde vive toda la lógica del negocio, desarrollado en Python con el framework Flask. Para que el código sea limpio y fácil de mantener, lo organizamos en seis módulos independientes llamados Blueprints, donde cada Blueprint atiende un bloque funcional del sistema: autenticación, fundaciones, necesidades, voluntariado, donaciones y tablero de indicadores. "
        "¿Y cómo se conectan el Frontend en Angular y el Backend en Flask? "
        "Se comunican a través de internet mediante servicios web REST que envían y reciben únicamente paquetes de texto JSON sumamente livianos, de menos de siete coma cinco kilobytes. "
        "Cuando el usuario inicia sesión, el servidor Flask verifica su contraseña encriptada y le entrega a Angular una llave digital temporal y segura llamada token JWT, que lleva firmado por dentro quién es el usuario y qué rol tiene. "
        "De ahí en adelante, cada vez que la persona hace clic en una pantalla de Angular, el navegador envía automáticamente esa llave digital en el encabezado de la petición; el servidor Flask revisa que la llave sea auténtica y que el rol tenga permiso antes de devolver o guardar cualquier dato."
    ),
    (
        VOICE_OSCAR,
        "La tercera capa es la Base de Datos. Para diseñarla utilizamos la herramienta MySQL Workbench, donde modelamos el diagrama Entidad-Relación, y para conectarla con Python usamos la herramienta SQLAlchemy, la cual protege automáticamente contra ataques de inyección de código y nos permite correr la misma base de datos tanto en SQLite y MySQL como en PostgreSQL en la nube. "
        "Llevamos el diseño de la base de datos hasta la Quinta Forma Normal con un total de treinta y cuatro tablas organizadas en cinco dominios: "
        "seis tablas para catálogos geográficos con los dieciocho municipios de la Sabana y sus coordenadas; "
        "seis tablas para catálogos institucionales, unidades de medida y los nueve Objetivos de Desarrollo Sostenible; "
        "seis tablas para usuarios, contraseñas encriptadas, roles y el registro exacto de fecha y hora en que cada usuario aceptó la Ley mil quinientos ochenta y uno de protección de datos; "
        "seis tablas para el perfil jurídico de las fundaciones, sus sedes veredales y sus documentos legales como el RUT y la Cámara de Comercio; "
        "y diez tablas transaccionales para las campañas, necesidades, donaciones, certificados PDF, convocatorias de voluntariado y bitácora de transparencia. "
        "Haber llegado hasta Quinta Forma Normal usando tablas puente significa que no repetimos información en ninguna parte y que una fundación puede tener varias sedes, varios ODS y múltiples campañas sin que jamás se crucen o corrompan los datos."
    ),
    (
        VOICE_OSCAR,
        "Para comprobar que la plataforma funciona de punta a punta en condiciones reales, en la fase de Transición desplegamos el Producto Mínimo Viable en la nube utilizando la plataforma Render con certificado de seguridad HTTPS activo. "
        "Cargamos en el sistema la información real de cinco organizaciones referentes de la Sabana: el hogar geriátrico FARASAN en Cogua, el albergue animal FUNHUELLAS en Cajicá, la asociación juvenil ASOMAYOR en Zipaquirá, la fundación infantil FUNDAULA en Chía y la corporación ambiental CORPOJUAICA en Tabio. "
        "Ejecutamos quince casos de prueba que evaluaron todos los casos de uso y restricciones de seguridad, aprobando el cien por ciento. "
        "Y en las pruebas de velocidad para zonas rurales, donde nuestra meta era que el servidor respondiera en menos de doscientos milisegundos, logramos un tiempo promedio real de respuesta de apenas diecinueve coma ocho milisegundos, con paquetes de datos menores a siete coma cinco kilobytes y certificados PDF de menos de tres kilobytes, garantizando que cualquier líder campesino o ciudadano pueda usar Conexión Solidaria desde su celular con total fluidez."
    ),
]

# =============================================================================
# AUDIO 3: SUSTENTACIÓN FLUIDA - PARTE 3: OPERACIÓN, MARKETING, VIABILIDAD FINANCIERA Y CIERRE
# =============================================================================
AUDIO_3_SEGMENTS = [
    (
        VOICE_OSCAR,
        "Sustentación de proyecto de grado: Conexión Solidaria. "
        "Parte tres: Organización, operación diaria, estrategia de marketing, defensa clara y trazable del plan financiero a cinco años, gestión de riesgos y conclusiones."
    ),
    (
        VOICE_ANGELICA,
        "Un software excelente solo logra impacto social si detrás hay una organización sostenible que lo mantenga vivo. "
        "Por eso, en el Capítulo cinco estructuramos la creación formal de la Fundación Conexión Solidaria, con sede en Chía, inscrita en la Cámara de Comercio de Bogotá y acogida al Régimen Tributario Especial de la DIAN. "
        "Planteamos una estructura organizacional ágil y sin burocracia: una Asamblea y Junta Directiva, un contador público experto en entidades sin ánimo de lucro contratado por honorarios, la Dirección Ejecutiva y de Alianzas a mi cargo, la Dirección de Tecnología a cargo de Oscar, un analista de verificación documental por horas y el apoyo de estudiantes de práctica social universitaria en Ingeniería de Sistemas y Comunicación. "
        "En el día a día medimos los tiempos reales de nuestros seis procesos operativos: por ejemplo, revisar el RUT y la Cámara de Comercio de una fundación nueva nos toma treinta y cinco minutos más tres horas de acompañamiento personalizado para enseñarles a subir su primera campaña; publicar una campaña toma ocho minutos; gestionar una postulación de voluntariado nueve minutos; y confirmar una donación con su certificado PDF apenas seis minutos."
    ),
    (
        VOICE_ANGELICA,
        "En nuestro estudio de mercado y plan de marketing dimensionamos con realismo a cuántos actores podemos llegar en los dieciocho municipios de Sabana Centro y Norte: "
        "en la región operan cerca de cuatrocientas veinte fundaciones comunitarias, estudian más de treinta y cinco mil jóvenes universitarios y funcionan alrededor de seiscientas cincuenta medianas y grandes empresas en el corredor industrial de Chía, Cajicá, Zipaquirá, Sopó, Tocancipá y Gachancipá. "
        "Nuestra meta de crecimiento a cinco años es vincular y verificar a veinticinco fundaciones rurales en el primer año, pasar a sesenta en el segundo año, llegar a ciento veinte en el tercer año, ciento sesenta en el cuarto y doscientas fundaciones activas en el quinto año. "
        "Para las fundaciones, los donantes y los voluntarios el precio es siempre cero pesos. "
        "Y para las empresas aliadas del corredor industrial diseñamos tres planes anuales de patrocinio de Responsabilidad Social Empresarial: el Plan Bronce de un millón quinientos mil pesos al año, el Plan Plata de tres millones y el Plan Oro de cinco millones de pesos, con los cuales financian la operación de la plataforma a cambio de reportes verificables de impacto por ODS, jornadas de voluntariado corporativo y su certificado tributario con descuento del veinticinco por ciento en su impuesto de renta."
    ),
    (
        VOICE_OSCAR,
        "Esto nos lleva a uno de los puntos más importantes de nuestra sustentación, en el que atendimos con total rigor las recomendaciones de nuestros jurados evaluadores: la viabilidad económica y la Memoria de Cálculo Financiera a cinco años. "
        "En lugar de usar cifras cerradas o suposiciones generales, construimos un libro financiero formulado hoja por hoja a partir de datos públicos verificados de dos mil veintiséis: "
        "tomamos el salario mínimo legal vigente de dos mil veintiséis de un millón setecientos cincuenta mil novecientos cinco pesos con su factor prestacional de uno coma cincuenta y dos sobre ciento ochenta y dos horas mensuales; la inflación anual del DANE del seis coma treinta por ciento; la tasa de cambio del dólar TRM de tres mil trescientos nueve pesos; la Unidad de Valor Básico, UVB, de doce mil ciento diez pesos para las tarifas exactas de Cámara de Comercio; y los precios oficiales en dólares publicados por Render. "
        "¿Cuánto cuesta poner en marcha Conexión Solidaria en el Año cero? "
        "La inversión inicial total es de veintiocho millones quinientos dieciséis mil ciento nueve pesos, pero tiene una gran ventaja: el ochenta y ocho coma siete por ciento de esa inversión, es decir, veinticinco millones doscientos noventa y nueve mil cuarenta y siete pesos, ya lo pusimos nosotros dos como cofundadores en especie a través de las seiscientas cuarenta horas de ingeniería dedicadas a construir el software, más el uso de nuestros computadores e internet. "
        "Por lo tanto, el dinero en efectivo que se necesita en el Año cero para constituir legalmente la fundación en notaría y Cámara de Comercio, pagar al contador para el registro tributario, comprar el dominio punto org punto co, el primer mes de servidor y guardar una reserva para imprevistos y riesgos es de solo tres millones doscientos diecisiete mil sesenta y dos pesos."
    ),
    (
        VOICE_OSCAR,
        "¿Y cuánto cuesta operar la plataforma durante el primer año para atender a las primeras veinticinco fundaciones rurales? "
        "Los gastos operativos del Año uno suman dieciséis millones doscientos treinta y un mil ciento nueve pesos en total, lo que equivale a un millón trescientos cincuenta y dos mil pesos al mes. "
        "De ese valor anual, mantener encendida toda la infraestructura en la nube de Render con servidor web, base de datos PostgreSQL, ambiente de pruebas y dominio cuesta apenas tres millones doscientos treinta y tres mil novecientos treinta y cinco pesos al año —es decir, sesenta y dos dólares al mes, unos doscientos setenta mil pesos mensuales incluyendo IVA—. "
        "Los demás gastos del año corresponden a cinco millones noventa y cinco mil pesos para la verificación documental, visitas a las veredas y talleres de capacitación a las fundaciones —donde la mitad de las horas de acompañamiento las cubrimos con practicantes universitarios en convenio—; cinco millones cuatrocientos cincuenta y tres mil pesos para el contador público y gastos legales; un millón novecientos trece mil pesos para mercadeo y difusión; y quinientos treinta y cinco mil pesos para imprevistos y cuatro por mil. "
        "Durante los dos primeros años, Angélica y yo aportamos nuestra dirección ad honorem para no ahogar financieramente a la fundación en su despegue, y a partir del tercer año el flujo de caja empieza a reconocer progresivamente entre el veinte y el cincuenta por ciento de nuestras horas."
    ),
    (
        VOICE_OSCAR,
        "Ahora veamos los ingresos y el flujo de caja con total transparencia: "
        "En el primer año proyectamos contactar a sesenta empresas del corredor industrial con una tasa de éxito conservadora del cinco por ciento, lo que nos permite cerrar los primeros tres patrocinios empresariales RSE por seis millones novecientos mil pesos, que sumados a cuatro millones quinientos mil pesos de valor esperado en convocatorias de innovación y cuatrocientos mil pesos en aportes voluntarios, nos dan unos ingresos en el Año uno de once millones ochocientos mil pesos. "
        "Como en ese primer año de arranque los ingresos de once coma ocho millones cubren el setenta y dos coma siete por ciento de los dieciséis coma dos millones de gastos, se presenta un déficit inicial de cuatro millones cuatrocientos treinta y un mil ciento nueve pesos. "
        "Al revisar el flujo mes a mes del primer año, identificamos que el momento donde más caja se necesita es el mes seis, antes de que entren los patrocinios del segundo semestre. "
        "Por eso determinamos con exactitud matemática que la fundación necesita arrancar con un capital semilla total de ocho millones trescientos ochenta y dos mil seiscientos sesenta y un pesos, el cual alcanza para pagar la constitución legal, la reserva de riesgos y cubrir todo el faltante del primer año sin que la plataforma se detenga un solo día. "
        "¿Qué pasa del Año dos en adelante? "
        "A medida que pasamos de tres empresas patrocinadoras en el Año uno a siete en el Año dos y a trece en el Año tres —gracias a una renovación del setenta y cinco por ciento y a nuevos contactos comerciales—, y que se activan los convenios de reportes de impacto con universidades y alcaldías, los ingresos superan a los gastos: "
        "en el Año dos los ingresos llegan a veintiocho millones cuarenta y siete mil pesos cubriendo el ciento diecisiete coma dos por ciento de los egresos; "
        "en el Año tres suben a cuarenta y ocho millones treinta mil pesos cubriendo el ciento nueve por ciento; "
        "y en el Año cuatro alcanzan sesenta y seis millones doscientos cuatro mil pesos cubriendo el ciento tres coma siete por ciento, recuperando el capital en efectivo en dos coma ochenta y ocho años. "
        "Incluso descontando los flujos a cinco años con una tasa de interés exigente del veintitrés coma dieciocho por ciento anual —que suma el trece coma dieciocho por ciento de los bonos TES del Estado más diez puntos de riesgo—, la relación Beneficio Costo es de cero coma noventa y siete, y en el escenario optimista el Valor Presente Neto supera los veinticuatro millones de pesos."
    ),
    (
        VOICE_ANGELICA,
        "También conectamos nuestra matriz de diez riesgos directamente con las finanzas: calculamos el valor monetario esperado de riesgos técnicos, legales y operativos —como caídas de señal en veredas, intentos de registro de fundaciones sin documentos o demoras en confirmar donaciones—, y dejamos reservado en efectivo desde el día cero un fondo de contingencia de dos millones ciento setenta y seis mil trescientos noventa y seis pesos. "
        "En conclusión, respetados jurados, con este trabajo demostramos que cumplimos los seis objetivos específicos y que Conexión Solidaria es técnica, operativa, legal y financieramente viable bajo dos condiciones concretas y alcanzables: reunir el capital semilla inicial de ocho millones trescientos ochenta y dos mil seiscientos sesenta y un pesos y vincular entre tres y trece empresas patrocinadoras en los primeros tres años, lo que equivale a menos del dos por ciento de las empresas del corredor industrial de nuestra Sabana. "
        "Más que una página web, entregamos un puente tecnológico vivo, desplegado en la nube y probado con datos reales, que demuestra que los Ingenieros de Sistemas de la Universidad de Cundinamarca podemos poner nuestro conocimiento al servicio de la solidaridad y del desarrollo de nuestra región. Muchas gracias."
    ),
]

# =============================================================================
# AUDIO 4: SIMULACRO FLUIDO DE 12 PREGUNTAS Y RESPUESTAS DE JURADOS
# =============================================================================
AUDIO_4_SEGMENTS = [
    (
        VOICE_ANGELICA,
        "Audio cuatro: Simulacro de entrenamiento de preguntas y respuestas con el jurado evaluador, respondidas con un lenguaje fluido, claro y contundente, cubriendo tanto la ingeniería de software y casos de uso como la memoria de cálculo financiera."
    ),
    (
        VOICE_JURADO,
        "Pregunta uno del jurado: Ingenieros, explíquennos de forma clara cómo se conecta el Frontend con el Backend en su plataforma y cómo aseguran que un usuario normal no entre a las funciones de administrador."
    ),
    (
        VOICE_OSCAR,
        "Responde Oscar: Claro que sí, ingeniero. La parte visual o Frontend, que hicimos en Angular diecisiete, y el servidor o Backend, que hicimos en Python con Flask, están separados y se comunican por internet enviándose paquetes ligeros de datos en formato JSON. "
        "Para la seguridad usamos llaves digitales temporales llamadas tokens JWT y control de acceso por cinco roles: Visitante, Donante, Voluntario, Fundación y Superadministrador. "
        "Cuando una persona inicia sesión, el servidor verifica su contraseña encriptada y le entrega al navegador ese token digital que lleva firmado por dentro qué rol tiene el usuario. "
        "Cada vez que la persona pide ver una pantalla o guardar un dato, Angular envía automáticamente ese token; si alguien con rol de donante o visitante intenta abrir una función exclusiva de una fundación o del superadministrador, tanto los guardianes de ruta en Angular como la validación de seguridad en el servidor Flask bloquean el paso de inmediato."
    ),
    (
        VOICE_JURADO,
        "Pregunta dos del jurado: ¿Cómo están organizados los módulos del servidor y la base de datos, y por qué dicen que llegaron hasta Quinta Forma Normal con treinta y cuatro tablas?"
    ),
    (
        VOICE_OSCAR,
        "Responde Oscar: En el servidor Flask organizamos el código en seis módulos independientes llamados Blueprints, que corresponden a las seis áreas del sistema: autenticación, fundaciones, necesidades, voluntariado, donaciones y tablero de indicadores. "
        "Para la base de datos usamos MySQL Workbench en el diseño y SQLAlchemy para conectarla con Python, de modo que funciona igual en SQLite local o en PostgreSQL en la nube de Render. "
        "Llegamos hasta Quinta Forma Normal con treinta y cuatro tablas divididas en cinco grupos porque en este proyecto hay muchas relaciones múltiples: una fundación puede tener varias sedes veredales, aportar a varios Objetivos de Desarrollo Sostenible, abrir varias campañas y recibir muchas donaciones y postulaciones de voluntarios. "
        "Al usar tablas puente en Quinta Forma Normal evitamos por completo que se repita información o que al actualizar el dato de un municipio o de una fundación se dañen los registros históricos."
    ),
    (
        VOICE_JURADO,
        "Pregunta tres del jurado: ¿Cuáles son los requisitos funcionales y los casos de uso más importantes que programaron en el Producto Mínimo Viable y cómo evitan que se registren fundaciones o donaciones falsas?"
    ),
    (
        VOICE_ANGELICA,
        "Responde Angélica: Levantamos doce requisitos funcionales que se reflejan en diez casos de uso principales, y pusimos un doble filtro de confianza para evitar fraudes: "
        "El primer filtro está en el Caso de Uso uno, el registro de la fundación: la organización llena sus datos en tres pasos, acepta la cláusula obligatoria de protección de datos de la Ley mil quinientos ochenta y uno y sube su RUT y Cámara de Comercio, pero queda en estado Pendiente; no aparece en el mapa público hasta que el superadministrador verifica que sus documentos legales son reales. "
        "El segundo filtro está en los Casos de Uso seis y siete, que son el registro de donaciones y la emisión del certificado PDF: cuando un donante reporta que donó dinero o insumos físicos, la donación entra como Pendiente con un código de rastreo, pero la barra de avance de la meta no se mueve todavía. "
        "Solo cuando la fundación confirma desde su panel que efectivamente recibió el dinero o los mercados en su sede, el sistema suma el aporte a la meta y genera automáticamente el certificado tributario en PDF con un código hash digital único imposible de alterar."
    ),
    (
        VOICE_JURADO,
        "Pregunta cuatro del jurado: Ustedes destacan que la plataforma está pensada para zonas rurales con mala conectividad. ¿Qué hicieron técnicamente para que funcione bien en una vereda y cómo lo probaron?"
    ),
    (
        VOICE_OSCAR,
        "Responde Oscar: Aplicamos tres medidas prácticas pensadas para redes móviles rurales tres G: "
        "primero, en Angular activamos carga diferida para que el teléfono del líder campesino solo descargue la pantalla que está usando y usamos mapas vectoriales livianos de Leaflet y OpenStreetMap; "
        "segundo, en el servidor Flask configuramos las respuestas JSON para que envíen únicamente los datos limpios que necesita cada vista, sin arrastrar archivos pesados; "
        "y tercero, generamos los certificados PDF directamente en memoria con un peso de menos de tres kilobytes. "
        "Al medir el rendimiento real en las pruebas de calidad sobre los endpoints del sistema con datos de cinco fundaciones de la Sabana, el tiempo promedio de respuesta del servidor fue de diecinueve coma ocho milisegundos —diez veces más rápido que el límite de doscientos milisegundos que exigía nuestro requisito no funcional uno—, y el paquete de datos más grande pesó apenas siete coma cuarenta y dos kilobytes."
    ),
    (
        VOICE_JURADO,
        "Pregunta cinco del jurado: ¿Cómo conectaron los resultados de las ciento setenta encuestas ciudadanas y de las cuatro fundaciones con el diseño de la plataforma?"
    ),
    (
        VOICE_ANGELICA,
        "Responde Angélica: Cada módulo del software nació de un dato real de nuestras dos encuestas en Google Forms: "
        "Como el sesenta y cuatro coma siete por ciento de los ciento setenta ciudadanos nos dijo que no conoce qué hacen las fundaciones de su municipio y ninguna de las cuatro fundaciones encuestadas —en Cajicá, Machetá, Simijaca y La Calera— usa una página web propia para publicar necesidades, creamos el mapa interactivo y directorio por municipio y ODS. "
        "Como para las fundaciones el dolor número uno es la falta de recursos y en la encuesta ciudadana vimos que el treinta y dos coma cuatro por ciento dona insumos físicos y el treinta y cinco coma tres por ciento hace voluntariado presencial, diseñamos el catálogo para que reciba tanto dinero como insumos medidos por unidades y el módulo de voluntariado con descuento automático de cupos. "
        "Y como el cincuenta y ocho coma dos por ciento de las personas exigió transparencia total en el uso de los recursos para animarse a donar, implementamos la confirmación bilateral de donaciones y el certificado PDF con sello digital."
    ),
    (
        VOICE_JURADO,
        "Pregunta seis del jurado: En el concepto previo de evaluación observamos que las tablas financieras tenían cifras cerradas y les faltaba la memoria de cálculo. ¿Cómo corrigieron esa observación?"
    ),
    (
        VOICE_OSCAR,
        "Responde Oscar: Atendimos su observación reconstruyendo todo el plan financiero en el archivo anexo Memoria Calculo Conexion Solidaria punto xlsx, donde eliminamos cualquier cifra cerrada y conectamos quince hojas con fórmulas trazables. "
        "Ahora cada número parte de datos públicos verificados de dos mil veintiséis: el salario mínimo de un millón setecientos cincuenta mil novecientos cinco pesos con su factor prestacional de uno coma cincuenta y dos sobre ciento ochenta y dos horas al mes; la inflación anual del DANE del seis coma treinta por ciento; la tasa de cambio oficial del dólar de tres mil trescientos nueve pesos; el valor de la UVB de doce mil ciento diez pesos para liquidar los costos exactos de Cámara de Comercio; y la tarifa pública de sesenta y dos dólares mensuales del servidor y base de datos en Render. "
        "Así, cualquier jurado o lector puede abrir el Excel, rastrear de qué fórmula sale cada peso proyectado entre dos mil veintiséis y dos mil treinta y uno, y verificar los escenarios."
    ),
    (
        VOICE_JURADO,
        "Pregunta siete del jurado: En su memoria de cálculo vemos que el primer año tiene egresos de dieciséis coma dos millones e ingresos de once coma ocho millones, dejando un déficit de cuatro coma cuatro millones, y que piden un capital semilla de ocho millones trescientos ochenta y dos mil pesos. ¿Por qué el capital semilla es de ocho coma treinta y ocho millones y cómo se sostiene la fundación después?"
    ),
    (
        VOICE_OSCAR,
        "Responde Oscar: Esa es una de las mayores fortalezas de haber hecho el flujo de caja mes a mes con total realismo. "
        "En el Año cero necesitamos tres millones doscientos diecisiete mil sesenta y dos pesos en efectivo para constituir legalmente la fundación, comprar el dominio y dejar guardada la reserva de riesgos de dos coma diecisiete millones. "
        "Durante el Año uno, mientras contactamos a las primeras sesenta empresas del corredor industrial y cerramos los primeros tres patrocinios RSE, los gastos operativos mensuales van saliendo todos los meses y el punto más bajo de caja se da en el sexto mes del primer año, acumulando una necesidad máxima de efectivo de ocho millones trescientos ochenta y dos mil seiscientos sesenta y un pesos. "
        "Al contar con ese capital semilla de ocho coma treinta y ocho millones desde el arranque, la fundación cubre toda la inversión en efectivo y todo el primer año sin riesgo de iliquidez. "
        "Y a partir del Año dos la fundación se vuelve autosostenible: al pasar de tres a siete patrocinadores en el Año dos y a trece en el Año tres, los ingresos propios superan a los gastos cubriendo el ciento diecisiete por ciento en el Año dos y el ciento nueve por ciento en el Año tres, sin cobrarle jamás a las fundaciones rurales."
    ),
    (
        VOICE_JURADO,
        "Pregunta ocho del jurado: ¿Por qué una empresa privada de Tocancipá, Chía o Zipaquirá aceptaría pagarles un plan de patrocinio RSE de millón y medio, tres millones o cinco millones de pesos al año?"
    ),
    (
        VOICE_ANGELICA,
        "Responde Angélica: Porque para la empresa aliada tiene un beneficio económico directo y un beneficio de sostenibilidad regional: "
        "Primero, al estar calificada la Fundación Conexión Solidaria en el Régimen Tributario Especial de la DIAN, el artículo doscientos cincuenta y siete del Estatuto Tributario le permite a la empresa descontar directamente de su impuesto de renta el veinticinco por ciento del valor donado. "
        "Eso quiere decir que en un patrocinio promedio de dos millones trescientos mil pesos al año, la empresa se ahorra quinientos setenta y cinco mil pesos en impuestos y el costo neto real le queda en solo un millón setecientos veinticinco mil pesos al año, menos de ciento cuarenta y cuatro mil pesos al mes. "
        "Y segundo, recibe reportes verificables de impacto en nueve Objetivos de Desarrollo Sostenible para sus informes de responsabilidad social y un canal organizado para hacer voluntariado corporativo con sus trabajadores en las veredas vecinas. Además, nuestra meta de trece patrocinadores en el tercer año representa apenas el dos por ciento de las seiscientas cincuenta empresas del corredor industrial de la Sabana."
    ),
]


def clean_text_for_audiobook(text):
    """Limpia etiquetas y símbolos para que la narración en voz alta suene como un audiolibro fluido."""
    t = text.replace("[[EDITAR]]", "").replace("[[/EDITAR]]", "")
    t = re.sub(r"https?://\S+", "enlace web disponible en el documento", t)
    t = t.replace("c:\\Users\\ingor\\conexion-solidaria\\docs\\", "")
    t = t.replace("(véase ", "(ver ").replace("véanse ", "ver ")
    t = t.replace(" >= ", " mayor o igual a ").replace(" < ", " menor a ").replace(" > ", " mayor a ")
    t = t.replace("100 %", "cien por ciento").replace(" %", " por ciento")
    t = t.replace("5FN", "Quinta Forma Normal")
    t = t.replace("OSAL", "O S A L")
    t = t.replace("ESAL", "E S A L")
    t = t.replace("MEDIT", "M E D I T")
    t = t.replace("ADOr006_V10", "A D O r cero cero seis versión diez")
    return t.strip()


def build_audiobook_segments_from_thesis():
    """Extrae la totalidad de los Capítulos 1, 2, 3, 4, 5 y Cierre del proyecto de grado para narrarlos como audiolibro."""
    import sys
    sys.path.insert(0, r"c:\Users\ingor\conexion-solidaria\docs\scripts_doc")
    from part1_cap1_cap2 import CAPITULO_1_Y_2
    from part2_cap3_cap4 import CAPITULO_3_Y_4
    from part3_cap5_cierre import CAPITULO_5_Y_CIERRE

    all_main_blocks = CAPITULO_1_Y_2 + CAPITULO_3_Y_4 + CAPITULO_5_Y_CIERRE

    chapters = []
    current_chapter_title = "Preliminares"
    current_blocks = []

    for btype, content in all_main_blocks:
        if btype == "H1":
            if current_blocks:
                chapters.append((current_chapter_title, current_blocks))
            current_chapter_title = content
            current_blocks = [(btype, content)]
        else:
            current_blocks.append((btype, content))
    if current_blocks:
        chapters.append((current_chapter_title, current_blocks))

    chapter_audio_segments = []
    for ch_idx, (ch_title, blocks) in enumerate(chapters):
        segs = []
        # Alternamos voz por sección H2 para que el audiolibro sea dinámico y agradable de escuchar
        current_voice = VOICE_ANGELICA if ch_idx % 2 == 0 else VOICE_OSCAR
        buffer_texts = [f"Audiolibro del documento final de grado: Conexión Solidaria, Tecnología para el Cambio Social. {clean_text_for_audiobook(ch_title)}."]

        for btype, content in blocks:
            if btype == "H1":
                continue
            elif btype == "H2":
                # Vaciar buffer previo antes de cambiar de voz en cada subcapítulo H2
                if buffer_texts:
                    joined = " ".join(buffer_texts)
                    if len(joined) > 20:
                        segs.append((current_voice, joined))
                    buffer_texts = []
                current_voice = VOICE_OSCAR if current_voice == VOICE_ANGELICA else VOICE_ANGELICA
                buffer_texts.append(f"Sección {clean_text_for_audiobook(content)}.")
            elif btype == "H3":
                buffer_texts.append(f"Subsección {clean_text_for_audiobook(content)}.")
            elif btype in ("P", "P_BOLD"):
                buffer_texts.append(clean_text_for_audiobook(content))
            elif btype == "UL":
                for item in content:
                    buffer_texts.append(clean_text_for_audiobook(item))
            elif btype == "TABLE":
                tit = clean_text_for_audiobook(content["title"])
                note = clean_text_for_audiobook(content.get("note", ""))
                buffer_texts.append(f"A continuación se referencia la {tit}. {note}")
            elif btype == "IMAGE":
                cap = clean_text_for_audiobook(content["caption"])
                note = clean_text_for_audiobook(content.get("note", ""))
                buffer_texts.append(f"Se presenta la {cap}. {note}")
            elif btype == "REF":
                buffer_texts.append(f"El documento concluye con las {len(content)} referencias bibliográficas en formato APA séptima edición y los doce anexos técnicos y financieros del proyecto.")

            # Si el buffer supera ~2500 caracteres, lo empaquetamos en un segmento TTS para evitar timeouts
            curr_len = sum(len(x) for x in buffer_texts)
            if curr_len >= 2400:
                segs.append((current_voice, " ".join(buffer_texts)))
                buffer_texts = []

        if buffer_texts:
            segs.append((current_voice, " ".join(buffer_texts)))

        chapter_audio_segments.append((ch_title, segs))

    return chapter_audio_segments


async def render_audio(filename, segments, force_overwrite=True):
    out_path = os.path.join(OUT_DIR, filename)
    if not force_overwrite and os.path.exists(out_path) and os.path.getsize(out_path) > 100000:
        print(f"==> Audio ya existente, omitiendo: {out_path} ({os.path.getsize(out_path):,} bytes)\n")
        return out_path
    chunks = []
    for idx, (voice, text) in enumerate(segments):
        for attempt in range(5):
            try:
                comm = edge_tts.Communicate(text, voice, rate="+5%")
                audio_bytes = bytearray()
                async for chunk in comm.stream():
                    if chunk["type"] == "audio":
                        audio_bytes.extend(chunk["data"])
                if len(audio_bytes) > 0:
                    chunks.append(bytes(audio_bytes))
                    print(f"  [{filename}] Segmento {idx + 1}/{len(segments)} sintetizado ({len(audio_bytes):,} bytes)")
                    await asyncio.sleep(0.35)
                    break
            except Exception as e:
                print(f"  [Reintento {attempt + 1}/5 en segmento {idx + 1}]: {e}")
                await asyncio.sleep(2.0)

    with open(out_path, "wb") as f:
        for c in chunks:
            f.write(c)
    print(f"==> Audio MP3 guardado en: {out_path} ({os.path.getsize(out_path):,} bytes)\n")
    return out_path


def write_master_study_guide():
    md_path = os.path.join(OUT_DIR, "GUION_Y_GUIA_MAESTRA_SUSTENTACION_30_MIN.md")
    lines = [
        "# GUION FLUIDO Y NATURAL DE SUSTENTACIÓN (30 MINUTOS) + AUDIOLIBRO COMPLETO",
        "**Proyecto de Grado:** CONEXIÓN SOLIDARIA. TECNOLOGÍA PARA EL CAMBIO SOCIAL  ",
        "**Opción de Grado:** Ruta de Emprendimiento e Innovación (Acuerdo 012 de 2024 / Guía `ADOr006_V10`)  ",
        "**Autores:** Angélica Rosa Olier Quiroga y Oscar Giovanni Robayo Olaya  ",
        "**Jurados Evaluadores:** Ing. Jorge Iván Ortiz e Ing. Jairo Fernando Henao González  ",
        "",
        "---",
        "",
        "## LISTA DE AUDIOS MP3 EN ESTA CARPETA",
        "1. `01_Sustentacion_Fluida_Parte1_Problema_Encuestas_y_Canvas.mp3` *(Sustentación Parte 1: Origen, DANE/AFE, Encuestas n=4 y n=170, 9 ODS y Canvas)*",
        "2. `02_Sustentacion_Fluida_Parte2_Requisitos_CasosUso_Arquitectura_y_BD.mp3` *(Sustentación Parte 2: 5 Roles, 12 RF, 6 RNF, los 10 Casos de Uso, conexión Angular-Flask con 6 Blueprints, BD 5FN de 34 tablas y Pruebas QA)*",
        "3. `03_Sustentacion_Fluida_Parte3_Operacion_Marketing_Finanzas_y_Cierre.mp3` *(Sustentación Parte 3: Fundación RTE, Operación, Marketing 4P, Memoria de Cálculo Financiera a 5 años, Riesgos y Conclusiones)*",
        "4. `04_Simulacro_Fluido_Preguntas_y_Respuestas_Jurados.mp3` *(Simulacro Q&A: Las preguntas clave técnicas y financieras respondidas con naturalidad y claridad)*",
        "5. `05_AUDIOLIBRO_COMPLETO_CONEXION_SOLIDARIA.mp3` *(Lectura completa narrada de todos los capítulos del documento final de grado como audiolibro)*",
        "",
        "---",
        "",
        "## PARTE 1. EL PROBLEMA HUMANO, LAS ENCUESTAS (n=4 y n=170), LOS 9 ODS Y EL CANVAS",
        ""
    ]
    for voice, text in AUDIO_1_SEGMENTS:
        speaker = "Angélica" if voice == VOICE_ANGELICA else "Oscar"
        lines.append(f"**[{speaker}]:** {text}\n")

    lines.append("\n---\n\n## PARTE 2. LOS 12 REQUISITOS FUNCIONALES, 6 NO FUNCIONALES, 10 CASOS DE USO, CONEXIÓN FRONT-BACK Y BASE DE DATOS\n")
    for voice, text in AUDIO_2_SEGMENTS:
        speaker = "Angélica" if voice == VOICE_ANGELICA else "Oscar"
        lines.append(f"**[{speaker}]:** {text}\n")

    lines.append("\n---\n\n## PARTE 3. PLAN OPERATIVO, MARKETING, DEFENSA CLARA DE LA MEMORIA DE CÁLCULO FINANCIERA Y CONCLUSIONES\n")
    for voice, text in AUDIO_3_SEGMENTS:
        speaker = "Angélica" if voice == VOICE_ANGELICA else "Oscar"
        lines.append(f"**[{speaker}]:** {text}\n")

    lines.append("\n---\n\n## PARTE 4. SIMULACRO FLUIDO DE PREGUNTAS Y RESPUESTAS CON LOS JURADOS\n")
    for voice, text in AUDIO_4_SEGMENTS:
        if voice == VOICE_JURADO:
            speaker = "Jurado Evaluador"
        elif voice == VOICE_ANGELICA:
            speaker = "Angélica"
        else:
            speaker = "Oscar"
        lines.append(f"**[{speaker}]:** {text}\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"==> Guía maestra actualizada en: {md_path}")


async def main():
    # Limpiar audios viejos con nombres anteriores si existen
    old_files = [
        "01_Sustentacion_Parte1_Problema_Diagnostico_Encuestas_y_Canvas.mp3",
        "02_Sustentacion_Parte2_Ingenieria_Arquitectura_5FN_CasosUso_y_QA.mp3",
        "03_Sustentacion_Parte3_Planes_MemoriaCalculo_Financiera_Riesgos_y_Cierre.mp3",
        "04_Simulacro_12_Preguntas_Jurados_Tecnicas_y_Financieras.mp3",
    ]
    for old_f in old_files:
        p = os.path.join(OUT_DIR, old_f)
        if os.path.exists(p):
            try:
                os.remove(p)
                print("Eliminado audio versión anterior:", old_f)
            except Exception:
                pass

    write_master_study_guide()

    # 1. Generar los 4 audios fluidos de sustentación
    await render_audio("01_Sustentacion_Fluida_Parte1_Problema_Encuestas_y_Canvas.mp3", AUDIO_1_SEGMENTS, force_overwrite=True)
    await render_audio("02_Sustentacion_Fluida_Parte2_Requisitos_CasosUso_Arquitectura_y_BD.mp3", AUDIO_2_SEGMENTS, force_overwrite=True)
    await render_audio("03_Sustentacion_Fluida_Parte3_Operacion_Marketing_Finanzas_y_Cierre.mp3", AUDIO_3_SEGMENTS, force_overwrite=True)
    await render_audio("04_Simulacro_Fluido_Preguntas_y_Respuestas_Jurados.mp3", AUDIO_4_SEGMENTS, force_overwrite=True)

    # 2. Generar el Audiolibro Completo del documento (por capítulos y consolidado en un solo MP3)
    chapter_segments = build_audiobook_segments_from_thesis()
    chapter_mp3_paths = []
    for idx, (ch_title, segs) in enumerate(chapter_segments):
        safe_name = f"Audiolibro_Cap{idx + 1}.mp3"
        print(f"=== Sintetizando Capítulo {idx + 1} del Audiolibro: {ch_title} ({len(segs)} bloques) ===")
        ch_path = await render_audio(safe_name, segs, force_overwrite=True)
        chapter_mp3_paths.append(ch_path)

    # Unificar todos los capítulos en 05_AUDIOLIBRO_COMPLETO_CONEXION_SOLIDARIA.mp3
    full_audiobook_path = os.path.join(OUT_DIR, "05_AUDIOLIBRO_COMPLETO_CONEXION_SOLIDARIA.mp3")
    with open(full_audiobook_path, "wb") as out_f:
        for ch_p in chapter_mp3_paths:
            if os.path.exists(ch_p):
                with open(ch_p, "rb") as in_f:
                    out_f.write(in_f.read())
    print(f"==> AUDIOLIBRO COMPLETO CONSOLIDADO EN: {full_audiobook_path} ({os.path.getsize(full_audiobook_path):,} bytes)")


if __name__ == "__main__":
    asyncio.run(main())
