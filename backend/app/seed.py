"""
Semilla (Seeder) de Catálogos Base y los 4 Perfiles Operativos en Sabana Norte de Cundinamarca:
- ADMIN (Administrador de la Plataforma)
- REPRESENTANTE_OSAL (Administrador de Fundación OSAL)
- DONANTE (Donante Solidario)
- VOLUNTARIO (Voluntario Rural)
"""
from datetime import date
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models import (
    Rol, Usuario, UsuarioRol, Pais, Departamento, Municipio, Direccion,
    TipoDocumento, Persona, DocumentoIdentidad, FundacionOsal, DocumentoLegalOsal,
    Voluntario, CategoriaHabilidad, Habilidad, PerfilHabilidadVoluntario,
    OdsObjetivo, CategoriaCausa, Campana, TipoNecesidad, NecesidadCampana,
    Donante, UnidadMedida, MetodoPago
)


def seed_initial_data():
    """Inserta datos maestros de la Sabana Norte y cuentas demostrativas si la BD está vacía."""
    rol_admin = Rol.query.filter_by(codigo="ADMIN").first()
    if rol_admin is not None:
        # Asegurar que el usuario admin@conexion.org exista incluso en bases ya creadas
        if not Usuario.query.filter_by(correo_electronico="admin@conexion.org").first():
            u_admin = Usuario(
                correo_electronico="admin@conexion.org",
                hash_contrasena=generate_password_hash("Solidaria2026*"),
                esta_activo=True
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
            db.session.commit()
        return

    # 1. Roles del sistema (RBAC)
    rol_admin = Rol(codigo="ADMIN", nombre="Administrador de Plataforma", descripcion="Gobernanza, auditoría y validación legal de OSAL")
    rol_osal = Rol(codigo="REPRESENTANTE_OSAL", nombre="Administrador OSAL", descripcion="Gestión operativa de fundación rural, campañas y bodega")
    rol_donante = Rol(codigo="DONANTE", nombre="Donante Solidario", descripcion="Registro de aportes económicos/especie y certificados tributarios")
    rol_voluntario = Rol(codigo="VOLUNTARIO", nombre="Voluntario Rural", descripcion="Gestión de competencias y postulación a labores comunitarias")
    db.session.add_all([rol_admin, rol_osal, rol_donante, rol_voluntario])
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
    um_kg = UnidadMedida(simbolo="KG", nombre="Kilogramos")
    um_und = UnidadMedida(simbolo="UND", nombre="Unidades")
    um_kit = UnidadMedida(simbolo="KIT", nombre="Kits / Paquetes")
    db.session.add_all([um_kg, um_und, um_kit])

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

    # 7. Usuarios iniciales para los 4 roles del sistema
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
    db.session.add_all([user_admin, user_osal, user_donante, user_voluntario])
    db.session.flush()

    db.session.add_all([
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

    p_admin = Persona(usuario_id=user_admin.id, direccion_id=dir_cogua.id, nombres="Coordinación General", apellidos="Gobernanza Sabana Norte", telefono_contacto="3100000001", fecha_nacimiento=date(1982, 4, 10))
    p_osal = Persona(usuario_id=user_osal.id, direccion_id=dir_cogua.id, nombres="María Elena", apellidos="Garzón Bello", telefono_contacto="3114509876", fecha_nacimiento=date(1979, 5, 14))
    p_donante = Persona(usuario_id=user_donante.id, direccion_id=dir_tabio.id, nombres="Carlos Andrés", apellidos="Suárez Rico", telefono_contacto="3108876543", fecha_nacimiento=date(1985, 8, 22))
    p_vol = Persona(usuario_id=user_voluntario.id, direccion_id=dir_tabio.id, nombres="Laura Valentina", apellidos="Chacón Vega", telefono_contacto="3152349988", fecha_nacimiento=date(1998, 2, 10))
    db.session.add_all([p_admin, p_osal, p_donante, p_vol])
    db.session.flush()

    db.session.add_all([
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

    db.session.add(DocumentoLegalOsal(
        fundacion_id=fundacion_demo.id,
        tipo_soporte="RUT_DIAN",
        nombre_archivo="RUT_901458932-1.pdf",
        url_archivo="/uploads/osal/1/RUT_901458932-1.pdf",
        estado_revision="APROBADO"
    ))

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
        NecesidadCampana(campana_id=campana_demo.id, tipo_necesidad_id=tn_esp.id, descripcion_item="Kits de semillas nativas (maíz, quinua, hortalizas)", cantidad_requerida=120, cantidad_cubierta=35, prioridad="ALTA"),
        NecesidadCampana(campana_id=campana_demo.id, tipo_necesidad_id=tn_vol.id, descripcion_item="Talleres de compostaje y preparación de camas de siembra", cantidad_requerida=40, cantidad_cubierta=12, prioridad="ALTA"),
    ])

    db.session.commit()
