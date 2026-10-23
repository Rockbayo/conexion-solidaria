"""
Semilla (Seeder) de Catálogos Base y los 5 Perfiles Operativos en Sabana Norte de Cundinamarca:
- SUPER_ADMIN (Superusuario de Plataforma: Parametrización y creación de Administradores)
- ADMIN (Administrador de la Plataforma: Gobernanza, usuarios y validación legal de OSAL)
- REPRESENTANTE_OSAL (Administrador de Fundación OSAL)
- DONANTE (Donante Solidario)
- VOLUNTARIO (Voluntario Rural)
"""
from datetime import date
from sqlalchemy import inspect, text
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models import (
    Rol, Usuario, UsuarioRol, Pais, Departamento, Municipio, Direccion,
    TipoDocumento, Persona, DocumentoIdentidad, FundacionOsal, DocumentoLegalOsal,
    Voluntario, CategoriaHabilidad, Habilidad, PerfilHabilidadVoluntario,
    OdsObjetivo, CategoriaCausa, Campana, TipoNecesidad, NecesidadCampana,
    Donante, UnidadMedida, MetodoPago, FranjaHoraria, ParametroSistema
)


def aplicar_migraciones_incrementales() -> None:
    """Garantiza que bases de datos creadas previamente cuenten con las columnas nuevas del modelo 5FN."""
    inspector = inspect(db.engine)
    tablas = set(inspector.get_table_names())

    if "usuarios" in tablas:
        cols = {c["name"] for c in inspector.get_columns("usuarios")}
        if "intentos_fallidos" not in cols:
            db.session.execute(text("ALTER TABLE usuarios ADD COLUMN intentos_fallidos INTEGER NOT NULL DEFAULT 0"))

    if "necesidades_campana" in tablas:
        cols = {c["name"] for c in inspector.get_columns("necesidades_campana")}
        if "unidad_medida_id" not in cols:
            db.session.execute(text("ALTER TABLE necesidades_campana ADD COLUMN unidad_medida_id INTEGER NULL"))

    if "recibos_tributarios" in tablas:
        cols = {c["name"] for c in inspector.get_columns("recibos_tributarios")}
        if "enviado_correo" not in cols:
            db.session.execute(text("ALTER TABLE recibos_tributarios ADD COLUMN enviado_correo BOOLEAN NOT NULL DEFAULT 0"))
        if "correo_destino" not in cols:
            db.session.execute(text("ALTER TABLE recibos_tributarios ADD COLUMN correo_destino VARCHAR(150) NULL"))
        if "fecha_envio_correo" not in cols:
            db.session.execute(text("ALTER TABLE recibos_tributarios ADD COLUMN fecha_envio_correo DATETIME NULL"))

    db.session.commit()


def asegurar_datos_parametrizacion() -> None:
    """Asegura que el rol SUPER_ADMIN, las unidades de medida, franjas horarias y parámetros del sistema existan."""
    rol_super = Rol.query.filter_by(codigo="SUPER_ADMIN").first()
    if not rol_super:
        rol_super = Rol(
            codigo="SUPER_ADMIN",
            nombre="Superusuario de Plataforma",
            descripcion="Gobierno técnico, creación de administradores y parametrización maestra"
        )
        db.session.add(rol_super)
        db.session.flush()

    rol_admin = Rol.query.filter_by(codigo="ADMIN").first()

    # Asegurar cuenta superadmin@conexion.org
    u_super = Usuario.query.filter_by(correo_electronico="superadmin@conexion.org").first()
    if not u_super:
        u_super = Usuario(
            correo_electronico="superadmin@conexion.org",
            hash_contrasena=generate_password_hash("Solidaria2026*"),
            esta_activo=True,
            intentos_fallidos=0
        )
        db.session.add(u_super)
        db.session.flush()
        db.session.add(UsuarioRol(usuario_id=u_super.id, rol_id=rol_super.id))
        db.session.add(Persona(
            usuario_id=u_super.id,
            nombres="Dirección General",
            apellidos="Superusuario de Plataforma",
            telefono_contacto="3100000000"
        ))

    # Asegurar cuenta admin@conexion.org
    if rol_admin and not Usuario.query.filter_by(correo_electronico="admin@conexion.org").first():
        u_admin = Usuario(
            correo_electronico="admin@conexion.org",
            hash_contrasena=generate_password_hash("Solidaria2026*"),
            esta_activo=True,
            intentos_fallidos=0
        )
        db.session.add(u_admin)
        db.session.flush()
        db.session.add(UsuarioRol(usuario_id=u_admin.id, rol_id=rol_admin.id))
        db.session.add(Persona(
            usuario_id=u_admin.id,
            nombres="Coordinación General",
            apellidos="Gobernanza Sabana Norte",
            telefono_contacto="3100000001"
        ))

    # Unidades de medida completas (Moneda, Kilos, Litros, Unidades, Kits, Horas)
    unidades_base = [
        ("COP", "Pesos Colombianos ($ COP)"),
        ("KG", "Kilogramos (kg)"),
        ("LT", "Litros (L)"),
        ("UND", "Unidades (und)"),
        ("KIT", "Kits / Paquetes"),
        ("HORAS", "Horas de Voluntariado (h)"),
    ]
    for simbolo, nombre in unidades_base:
        um = UnidadMedida.query.filter_by(simbolo=simbolo).first()
        if not um:
            db.session.add(UnidadMedida(simbolo=simbolo, nombre=nombre))
        else:
            um.nombre = nombre
    db.session.flush()

    # Asignar unidad de medida a necesidades de campaña que aún no la tengan
    um_cop = UnidadMedida.query.filter_by(simbolo="COP").first()
    um_kit = UnidadMedida.query.filter_by(simbolo="KIT").first()
    um_horas = UnidadMedida.query.filter_by(simbolo="HORAS").first()
    for nec in NecesidadCampana.query.filter_by(unidad_medida_id=None).all():
        cod = nec.tipo_necesidad.codigo if nec.tipo_necesidad else "ESPECIE"
        if cod == "ECONOMICA" and um_cop:
            nec.unidad_medida_id = um_cop.id
        elif cod == "TIEMPO_VOLUNTARIADO" and um_horas:
            nec.unidad_medida_id = um_horas.id
        elif um_kit:
            nec.unidad_medida_id = um_kit.id

    # Franjas horarias de voluntariado
    franjas_base = [
        ("FIN_SEMANA_MANANA", "Fines de semana en la mañana (Sábados y Domingos 7:00 a.m. - 12:00 m.)", 5),
        ("FIN_SEMANA_TARDE", "Fines de semana en la tarde (Sábados y Domingos 1:00 p.m. - 5:00 p.m.)", 4),
        ("SABADO_COMPLETO", "Jornada completa de sábado (7:00 a.m. - 3:00 p.m.)", 8),
        ("ENTRE_SEMANA_MANANA", "Entre semana en la mañana (Lunes a Viernes 8:00 a.m. - 12:00 m.)", 4),
        ("ENTRE_SEMANA_TARDE", "Entre semana en la tarde (Lunes a Viernes 2:00 p.m. - 6:00 p.m.)", 4),
    ]
    for codigo, nombre, horas in franjas_base:
        if not FranjaHoraria.query.filter_by(codigo=codigo).first():
            db.session.add(FranjaHoraria(codigo=codigo, nombre=nombre, horas_sugeridas=horas, activa=True))

    # Parámetros globales del sistema
    parametros_base = [
        (
            "MONTO_MINIMO_DONACION_COP",
            "10000",
            "Importe mínimo permitido para registrar aportes monetarios en pesos colombianos ($ COP)",
            "NUMERO"
        ),
        (
            "MAX_INTENTOS_LOGIN",
            "5",
            "Número máximo de intentos fallidos de contraseña antes de bloquear preventivamente una cuenta",
            "NUMERO"
        ),
        (
            "NORMA_TRIBUTARIA_VIGENTE",
            "Artículos 125, 125-1, 125-2, 125-3 y 257 del Estatuto Tributario Nacional y Decreto 2150 de 2017",
            "Marco normativo colombiano impreso en los certificados tributarios de donación",
            "TEXTO"
        ),
        (
            "CORREO_SOPORTE_PLATAFORMA",
            "gobernanza@conexionsolidaria.org",
            "Correo institucional de soporte y notificaciones de Conexión Solidaria Sabana Norte",
            "TEXTO"
        ),
    ]
    for clave, valor, desc, tipo in parametros_base:
        if not ParametroSistema.query.filter_by(clave=clave).first():
            db.session.add(ParametroSistema(clave=clave, valor=valor, descripcion=desc, tipo_dato=tipo))

    db.session.commit()


def seed_initial_data():
    """Inserta datos maestros de la Sabana Norte y cuentas demostrativas si la BD está vacía."""
    aplicar_migraciones_incrementales()

    rol_admin = Rol.query.filter_by(codigo="ADMIN").first()
    if rol_admin is not None:
        asegurar_datos_parametrizacion()
        return

    # 1. Roles del sistema (RBAC)
    rol_super = Rol(codigo="SUPER_ADMIN", nombre="Superusuario de Plataforma", descripcion="Gobierno técnico, creación de administradores y parametrización maestra")
    rol_admin = Rol(codigo="ADMIN", nombre="Administrador de Plataforma", descripcion="Gobernanza, usuarios, auditoría y validación legal de OSAL")
    rol_osal = Rol(codigo="REPRESENTANTE_OSAL", nombre="Administrador OSAL", descripcion="Gestión operativa de fundación rural, campañas y bodega")
    rol_donante = Rol(codigo="DONANTE", nombre="Donante Solidario", descripcion="Registro de aportes económicos/especie y certificados tributarios")
    rol_voluntario = Rol(codigo="VOLUNTARIO", nombre="Voluntario Rural", descripcion="Gestión de competencias y postulación a labores comunitarias")
    db.session.add_all([rol_super, rol_admin, rol_osal, rol_donante, rol_voluntario])
    db.session.flush()

    # 2. Geolocalización: Colombia -> Cundinamarca -> Municipios de Sabana Norte
    colombia = Pais(codigo_iso="COL", nombre="Colombia")
    db.session.add(colombia)
    db.session.flush()

    cundinamarca = Departamento(pais_id=colombia.id, codigo_dane="25", nombre="Cundinamarca")
    db.session.add(cundinamarca)
    db.session.flush()

    municipios_sabana = [
        Municipio(departamento_id=cundinamarca.id, codigo_dane="25175", nombre="Chía", es_sabana_norte=True, latitud_centro=4.8616, longitud_centro=-74.0325),
        Municipio(departamento_id=cundinamarca.id, codigo_dane="25126", nombre="Cajicá", es_sabana_norte=True, latitud_centro=4.9186, longitud_centro=-74.0279),
        Municipio(departamento_id=cundinamarca.id, codigo_dane="25899", nombre="Zipaquirá", es_sabana_norte=True, latitud_centro=5.0221, longitud_centro=-74.0042),
        Municipio(departamento_id=cundinamarca.id, codigo_dane="25785", nombre="Tabio", es_sabana_norte=True, latitud_centro=4.9173, longitud_centro=-74.0936),
        Municipio(departamento_id=cundinamarca.id, codigo_dane="25799", nombre="Tenjo", es_sabana_norte=True, latitud_centro=4.8722, longitud_centro=-74.1439),
        Municipio(departamento_id=cundinamarca.id, codigo_dane="25200", nombre="Cogua", es_sabana_norte=True, latitud_centro=5.0617, longitud_centro=-73.9806),
        Municipio(departamento_id=cundinamarca.id, codigo_dane="25758", nombre="Sopó", es_sabana_norte=True, latitud_centro=4.9089, longitud_centro=-73.9403),
        Municipio(departamento_id=cundinamarca.id, codigo_dane="25817", nombre="Tocancipá", es_sabana_norte=True, latitud_centro=4.9658, longitud_centro=-73.9136),
        Municipio(departamento_id=cundinamarca.id, codigo_dane="25295", nombre="Gachancipá", es_sabana_norte=True, latitud_centro=4.9911, longitud_centro=-73.8736),
        Municipio(departamento_id=cundinamarca.id, codigo_dane="25486", nombre="Nemocón", es_sabana_norte=True, latitud_centro=5.0678, longitud_centro=-73.8778),
    ]
    db.session.add_all(municipios_sabana)
    db.session.flush()

    # 3. Tipos de Documento
    td_cc = TipoDocumento(sigla="CC", nombre="Cédula de Ciudadanía", aplica_persona_juridica=False)
    td_ce = TipoDocumento(sigla="CE", nombre="Cédula de Extranjería", aplica_persona_juridica=False)
    td_nit = TipoDocumento(sigla="NIT", nombre="Número de Identificación Tributaria", aplica_persona_juridica=True)
    db.session.add_all([td_cc, td_ce, td_nit])

    # 4. Catálogo de Causas, ODS y Tipos de Necesidad
    ods_1 = OdsObjetivo(numero_ods=1, titulo="Fin de la Pobreza", descripcion="Erradicar la pobreza rural extrema")
    ods_2 = OdsObjetivo(numero_ods=2, titulo="Hambre Cero", descripcion="Seguridad alimentaria y agricultura campesina sostenible")
    ods_4 = OdsObjetivo(numero_ods=4, titulo="Educación de Calidad", descripcion="Educación rural inclusiva y equitativa")
    ods_15 = OdsObjetivo(numero_ods=15, titulo="Vida de Ecosistemas Terrestres", descripcion="Restauración de páramos y cuencas en Sabana Norte")
    db.session.add_all([ods_1, ods_2, ods_4, ods_15])

    cat_agro = CategoriaCausa(nombre="Soberanía Alimentaria y Huertas", descripcion="Apoyo a familias campesinas y comedores veredales")
    cat_edu = CategoriaCausa(nombre="Educación y Conectividad Veredal", descripcion="Escuelas rurales, bibliotecas y formación")
    cat_amb = CategoriaCausa(nombre="Conservación de Páramos y Agua", descripcion="Reforestación nativa en cuencas altas")
    db.session.add_all([cat_agro, cat_edu, cat_amb])

    tn_eco = TipoNecesidad(codigo="ECONOMICA", nombre="Apoyo Económico Monetario")
    tn_esp = TipoNecesidad(codigo="ESPECIE", nombre="Donación en Especie (Insumos / Alimentos / Herramientas)")
    tn_vol = TipoNecesidad(codigo="TIEMPO_VOLUNTARIADO", nombre="Tiempo y Talento de Voluntariado")
    db.session.add_all([tn_eco, tn_esp, tn_vol])

    # 5. Unidades de Medida y Métodos de Pago
    um_cop = UnidadMedida(simbolo="COP", nombre="Pesos Colombianos ($ COP)")
    um_kg = UnidadMedida(simbolo="KG", nombre="Kilogramos (kg)")
    um_lt = UnidadMedida(simbolo="LT", nombre="Litros (L)")
    um_und = UnidadMedida(simbolo="UND", nombre="Unidades (und)")
    um_kit = UnidadMedida(simbolo="KIT", nombre="Kits / Paquetes")
    um_horas = UnidadMedida(simbolo="HORAS", nombre="Horas de Voluntariado (h)")
    db.session.add_all([um_cop, um_kg, um_lt, um_und, um_kit, um_horas])

    mp_trans = MetodoPago(codigo="TRANSFERENCIA", nombre="Transferencia Bancaria / PSE")
    mp_nequi = MetodoPago(codigo="BILLETERA_MOVIL", nombre="Nequi / DaviPlata Rural")
    db.session.add_all([mp_trans, mp_nequi])

    # 6. Categorías de Habilidades y Habilidades
    ch_agro = CategoriaHabilidad(nombre="Agroecología y Campo", descripcion="Conocimientos técnicos agrícolas y ambientales")
    ch_edu = CategoriaHabilidad(nombre="Pedagogía y Salud Comunitaria", descripcion="Acompañamiento educativo y psicosocial")
    ch_log = CategoriaHabilidad(nombre="Logística y Gestión", descripcion="Transporte veredal, acopio y contabilidad")
    db.session.add_all([ch_agro, ch_edu, ch_log])
    db.session.flush()

    hab_1 = Habilidad(categoria_id=ch_agro.id, nombre="Manejo de Huertas Orgánicas", descripcion="Compostaje y siembra sin agroquímicos")
    hab_2 = Habilidad(categoria_id=ch_agro.id, nombre="Reforestación de Especies Nativas", descripcion="Viverismo y plantación en alta montaña")
    hab_3 = Habilidad(categoria_id=ch_edu.id, nombre="Tutoría Escolar Primaria Rural", descripcion="Refuerzo en lectura, matemáticas y tecnología")
    hab_4 = Habilidad(categoria_id=ch_log.id, nombre="Transporte y Distribución en Veredas", descripcion="Conducción 4x4 y entrega de acopios")
    db.session.add_all([hab_1, hab_2, hab_3, hab_4])
    db.session.flush()

    # 7. Usuarios iniciales para los 5 roles del sistema
    user_super = Usuario(
        correo_electronico="superadmin@conexion.org",
        hash_contrasena=generate_password_hash("Solidaria2026*"),
        esta_activo=True
    )
    user_admin = Usuario(
        correo_electronico="admin@conexion.org",
        hash_contrasena=generate_password_hash("Solidaria2026*"),
        esta_activo=True
    )
    user_osal = Usuario(
        correo_electronico="osal@sabananorte.org",
        hash_contrasena=generate_password_hash("Solidaria2026*"),
        esta_activo=True
    )
    user_donante = Usuario(
        correo_electronico="donante@conexion.org",
        hash_contrasena=generate_password_hash("Solidaria2026*"),
        esta_activo=True
    )
    user_voluntario = Usuario(
        correo_electronico="voluntario@conexion.org",
        hash_contrasena=generate_password_hash("Solidaria2026*"),
        esta_activo=True
    )
    db.session.add_all([user_super, user_admin, user_osal, user_donante, user_voluntario])
    db.session.flush()

    db.session.add_all([
        UsuarioRol(usuario_id=user_super.id, rol_id=rol_super.id),
        UsuarioRol(usuario_id=user_admin.id, rol_id=rol_admin.id),
        UsuarioRol(usuario_id=user_osal.id, rol_id=rol_osal.id),
        UsuarioRol(usuario_id=user_donante.id, rol_id=rol_donante.id),
        UsuarioRol(usuario_id=user_voluntario.id, rol_id=rol_voluntario.id),
    ])

    dir_cogua = Direccion(
        municipio_id=municipios_sabana[5].id,
        vereda_o_barrio="Vereda Quebrada Honda",
        direccion_fisica="Km 4 Vía Neusa - Escuela Vieja",
        indicaciones_rurales="Frente al tanque comunitario de acueducto veredal",
        latitud=5.0785,
        longitud=-73.9891
    )
    dir_tabio = Direccion(
        municipio_id=municipios_sabana[3].id,
        vereda_o_barrio="Vereda Lourdes",
        direccion_fisica="Finca El Manantial Lote 3",
        indicaciones_rurales="200m después del puente de piedra",
        latitud=4.9295,
        longitud=-74.0852
    )
    db.session.add_all([dir_cogua, dir_tabio])
    db.session.flush()

    p_super = Persona(usuario_id=user_super.id, direccion_id=dir_cogua.id, nombres="Dirección General", apellidos="Superusuario de Plataforma", telefono_contacto="3100000000", fecha_nacimiento=date(1980, 1, 15))
    p_admin = Persona(usuario_id=user_admin.id, direccion_id=dir_cogua.id, nombres="Coordinación General", apellidos="Gobernanza Sabana Norte", telefono_contacto="3100000001", fecha_nacimiento=date(1982, 4, 10))
    p_osal = Persona(usuario_id=user_osal.id, direccion_id=dir_cogua.id, nombres="María Elena", apellidos="Garzón Bello", telefono_contacto="3114509876", fecha_nacimiento=date(1979, 5, 14))
    p_donante = Persona(usuario_id=user_donante.id, direccion_id=dir_tabio.id, nombres="Carlos Andrés", apellidos="Suárez Rico", telefono_contacto="3108876543", fecha_nacimiento=date(1985, 8, 22))
    p_vol = Persona(usuario_id=user_voluntario.id, direccion_id=dir_tabio.id, nombres="Laura Valentina", apellidos="Chacón Vega", telefono_contacto="3152349988", fecha_nacimiento=date(1998, 2, 10))
    db.session.add_all([p_super, p_admin, p_osal, p_donante, p_vol])
    db.session.flush()

    db.session.add_all([
        DocumentoIdentidad(persona_id=p_super.id, tipo_documento_id=td_cc.id, numero_documento="80100100"),
        DocumentoIdentidad(persona_id=p_admin.id, tipo_documento_id=td_cc.id, numero_documento="80100200"),
        DocumentoIdentidad(persona_id=p_osal.id, tipo_documento_id=td_cc.id, numero_documento="52418902"),
        DocumentoIdentidad(persona_id=p_donante.id, tipo_documento_id=td_cc.id, numero_documento="79845123"),
        DocumentoIdentidad(persona_id=p_vol.id, tipo_documento_id=td_cc.id, numero_documento="1072654981"),
    ])

    fundacion_demo = FundacionOsal(
        usuario_representante_id=user_osal.id,
        direccion_id=dir_cogua.id,
        nit="901458932-1",
        razon_social="Fundación Agroecológica Raíces de Sabana Norte",
        sigla="FARASAN",
        mision="Fortalecer la soberanía alimentaria y restaurar microcuencas en las veredas de Cogua, Zipaquirá y Tabio.",
        telefono_institucional="3114509876",
        estado_validacion="APROBADA",
        fecha_constitucion=date(2019, 3, 15)
    )
    donante_demo = Donante(persona_id=p_donante.id, tipo_donante="PERSONA_NATURAL", requiere_certificado_tributario=True)
    voluntario_demo = Voluntario(persona_id=p_vol.id, disponibilidad_horas_semana=8, biografia_corta="Ingeniera agrónoma comprometida con las huertas veredales.", dispuesto_desplazamiento_rural=True)
    db.session.add_all([fundacion_demo, donante_demo, voluntario_demo])
    db.session.flush()

    db.session.add_all([
        DocumentoLegalOsal(
            fundacion_id=fundacion_demo.id,
            tipo_soporte="RUT_DIAN",
            nombre_archivo="RUT_901458932-1.pdf",
            url_archivo="/uploads/osal/1/RUT_901458932-1.pdf",
            estado_revision="APROBADO"
        ),
        DocumentoLegalOsal(
            fundacion_id=fundacion_demo.id,
            tipo_soporte="CERTIFICADO_EXISTENCIA_CAMARA",
            nombre_archivo="CamaraComercio_901458932-1.pdf",
            url_archivo="/uploads/osal/1/CamaraComercio_901458932-1.pdf",
            estado_revision="APROBADO"
        )
    ])

    db.session.add(PerfilHabilidadVoluntario(
        voluntario_id=voluntario_demo.id,
        habilidad_id=hab_1.id,
        nivel_dominio="AVANZADO",
        anos_experiencia=4
    ))

    campana_demo = Campana(
        fundacion_id=fundacion_demo.id,
        categoria_causa_id=cat_agro.id,
        ods_id=ods_2.id,
        titulo="Huertas Escolares Resilientes en Veredas de Cogua y Tabio",
        descripcion="Dotación de semillas nativas, herramientas e invernaderos comunitarios para 4 escuelas rurales.",
        meta_economica=15000000.00,
        monto_recaudado=3850000.00,
        fecha_inicio=date(2026, 1, 15),
        fecha_fin=date(2026, 12, 20),
        estado="ACTIVA"
    )
    db.session.add(campana_demo)
    db.session.flush()

    db.session.add_all([
        NecesidadCampana(campana_id=campana_demo.id, tipo_necesidad_id=tn_esp.id, unidad_medida_id=um_kit.id, descripcion_item="Kits de semillas nativas (maíz, quinua, hortalizas)", cantidad_requerida=120, cantidad_cubierta=35, prioridad="ALTA"),
        NecesidadCampana(campana_id=campana_demo.id, tipo_necesidad_id=tn_vol.id, unidad_medida_id=um_horas.id, descripcion_item="Talleres de compostaje y preparación de camas de siembra", cantidad_requerida=40, cantidad_cubierta=12, prioridad="ALTA"),
    ])

    db.session.commit()
    asegurar_datos_parametrizacion()
