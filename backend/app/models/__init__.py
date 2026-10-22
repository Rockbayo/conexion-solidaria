"""
Modelo de Base de Datos Relacional en Quinta Forma Normal (5FN) - 32 Tablas
Agrupadas en 7 Módulos Arquitectónicos para "Conexión Solidaria" (Sabana Norte de Cundinamarca).
Nomenclatura estricta: snake_case y llaves foráneas integrales.
"""
from datetime import datetime, timezone
from app.extensions import db


def utc_now():
    return datetime.now(timezone.utc)


# ==============================================================================
# MÓDULO 1: SEGURIDAD (4 Tablas: usuarios, roles, usuarios_roles, logs_auditoria)
# ==============================================================================

class Rol(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(40), unique=True, nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    usuarios_asociados = db.relationship("UsuarioRol", back_populates="rol", cascade="all, delete-orphan")


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    correo_electronico = db.Column(db.String(150), unique=True, nullable=False, index=True)
    hash_contrasena = db.Column(db.String(255), nullable=False)
    esta_activo = db.Column(db.Boolean, default=True, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=utc_now, nullable=False)
    ultimo_acceso = db.Column(db.DateTime, nullable=True)

    roles_asociados = db.relationship("UsuarioRol", back_populates="usuario", cascade="all, delete-orphan")
    logs = db.relationship("LogAuditoria", back_populates="usuario")
    persona = db.relationship("Persona", back_populates="usuario", uselist=False)
    fundaciones_administradas = db.relationship("FundacionOsal", back_populates="usuario_representante")


class UsuarioRol(db.Model):
    __tablename__ = "usuarios_roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)
    fecha_asignacion = db.Column(db.DateTime, default=utc_now, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("usuario_id", "rol_id", name="uq_usuario_rol"),
    )

    usuario = db.relationship("Usuario", back_populates="roles_asociados")
    rol = db.relationship("Rol", back_populates="usuarios_asociados")


class LogAuditoria(db.Model):
    __tablename__ = "logs_auditoria"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    accion = db.Column(db.String(100), nullable=False)
    entidad_afectada = db.Column(db.String(80), nullable=False)
    registro_id = db.Column(db.Integer, nullable=True)
    detalle = db.Column(db.Text, nullable=True)
    direccion_ip = db.Column(db.String(45), nullable=True)
    fecha_evento = db.Column(db.DateTime, default=utc_now, nullable=False)

    usuario = db.relationship("Usuario", back_populates="logs")


# ==============================================================================
# MÓDULO 2: GEOLOCALIZACIÓN (4 Tablas: paises, departamentos, municipios, direcciones)
# ==============================================================================

class Pais(db.Model):
    __tablename__ = "paises"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_iso = db.Column(db.String(3), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

    departamentos = db.relationship("Departamento", back_populates="pais")


class Departamento(db.Model):
    __tablename__ = "departamentos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pais_id = db.Column(db.Integer, db.ForeignKey("paises.id", ondelete="RESTRICT"), nullable=False)
    codigo_dane = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

    pais = db.relationship("Pais", back_populates="departamentos")
    municipios = db.relationship("Municipio", back_populates="departamento")


class Municipio(db.Model):
    __tablename__ = "municipios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey("departamentos.id", ondelete="RESTRICT"), nullable=False)
    codigo_dane = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    es_sabana_norte = db.Column(db.Boolean, default=True, nullable=False)
    latitud_centro = db.Column(db.Numeric(10, 7), nullable=True)
    longitud_centro = db.Column(db.Numeric(10, 7), nullable=True)

    departamento = db.relationship("Departamento", back_populates="municipios")
    direcciones = db.relationship("Direccion", back_populates="municipio")


class Direccion(db.Model):
    __tablename__ = "direcciones"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    municipio_id = db.Column(db.Integer, db.ForeignKey("municipios.id", ondelete="RESTRICT"), nullable=False)
    vereda_o_barrio = db.Column(db.String(120), nullable=False)
    direccion_fisica = db.Column(db.String(200), nullable=False)
    indicaciones_rurales = db.Column(db.String(255), nullable=True)
    latitud = db.Column(db.Numeric(10, 7), nullable=False)
    longitud = db.Column(db.Numeric(10, 7), nullable=False)

    municipio = db.relationship("Municipio", back_populates="direcciones")
    fundaciones = db.relationship("FundacionOsal", back_populates="direccion")
    personas = db.relationship("Persona", back_populates="direccion")


# ==============================================================================
# MÓDULO 3: PERFILES (5 Tablas: tipos_documento, personas, documentos_identidad,
#                     fundaciones_osal, documentos_legales_osal)
# ==============================================================================

class TipoDocumento(db.Model):
    __tablename__ = "tipos_documento"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sigla = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    aplica_persona_juridica = db.Column(db.Boolean, default=False, nullable=False)

    documentos_identidad = db.relationship("DocumentoIdentidad", back_populates="tipo_documento")


class Persona(db.Model):
    __tablename__ = "personas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), unique=True, nullable=False)
    direccion_id = db.Column(db.Integer, db.ForeignKey("direcciones.id", ondelete="SET NULL"), nullable=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    telefono_contacto = db.Column(db.String(30), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=True)

    usuario = db.relationship("Usuario", back_populates="persona")
    direccion = db.relationship("Direccion", back_populates="personas")
    documento_identidad = db.relationship("DocumentoIdentidad", back_populates="persona", uselist=False)
    voluntario = db.relationship("Voluntario", back_populates="persona", uselist=False)
    donante = db.relationship("Donante", back_populates="persona", uselist=False)


class DocumentoIdentidad(db.Model):
    __tablename__ = "documentos_identidad"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    persona_id = db.Column(db.Integer, db.ForeignKey("personas.id", ondelete="CASCADE"), unique=True, nullable=False)
    tipo_documento_id = db.Column(db.Integer, db.ForeignKey("tipos_documento.id", ondelete="RESTRICT"), nullable=False)
    numero_documento = db.Column(db.String(40), unique=True, nullable=False, index=True)
    fecha_expedicion = db.Column(db.Date, nullable=True)

    persona = db.relationship("Persona", back_populates="documento_identidad")
    tipo_documento = db.relationship("TipoDocumento", back_populates="documentos_identidad")


class FundacionOsal(db.Model):
    __tablename__ = "fundaciones_osal"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_representante_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False)
    direccion_id = db.Column(db.Integer, db.ForeignKey("direcciones.id", ondelete="RESTRICT"), nullable=False)
    nit = db.Column(db.String(30), unique=True, nullable=False, index=True)
    razon_social = db.Column(db.String(180), nullable=False)
    sigla = db.Column(db.String(60), nullable=True)
    mision = db.Column(db.Text, nullable=False)
    telefono_institucional = db.Column(db.String(30), nullable=False)
    estado_validacion = db.Column(db.String(30), default="PENDIENTE", nullable=False)  # PENDIENTE, APROBADA, RECHAZADA
    fecha_constitucion = db.Column(db.Date, nullable=True)
    fecha_registro = db.Column(db.DateTime, default=utc_now, nullable=False)

    usuario_representante = db.relationship("Usuario", back_populates="fundaciones_administradas")
    direccion = db.relationship("Direccion", back_populates="fundaciones")
    documentos_legales = db.relationship("DocumentoLegalOsal", back_populates="fundacion", cascade="all, delete-orphan")
    campanas = db.relationship("Campana", back_populates="fundacion")


class DocumentoLegalOsal(db.Model):
    __tablename__ = "documentos_legales_osal"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fundacion_id = db.Column(db.Integer, db.ForeignKey("fundaciones_osal.id", ondelete="CASCADE"), nullable=False)
    tipo_soporte = db.Column(db.String(80), nullable=False)  # RUT, CAMARA_COMERCIO, CERTIFICADO_EXISTENCIA
    nombre_archivo = db.Column(db.String(200), nullable=False)
    url_archivo = db.Column(db.String(255), nullable=False)
    estado_revision = db.Column(db.String(30), default="EN_REVISION", nullable=False)
    fecha_carga = db.Column(db.DateTime, default=utc_now, nullable=False)

    fundacion = db.relationship("FundacionOsal", back_populates="documentos_legales")


# ==============================================================================
# MÓDULO 4: VOLUNTARIADO (4 Tablas: voluntarios, categorias_habilidades,
#                         habilidades, perfil_habilidades_voluntario)
# ==============================================================================

class Voluntario(db.Model):
    __tablename__ = "voluntarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    persona_id = db.Column(db.Integer, db.ForeignKey("personas.id", ondelete="CASCADE"), unique=True, nullable=False)
    disponibilidad_horas_semana = db.Column(db.Integer, default=4, nullable=False)
    biografia_corta = db.Column(db.String(255), nullable=True)
    dispuesto_desplazamiento_rural = db.Column(db.Boolean, default=True, nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)

    persona = db.relationship("Persona", back_populates="voluntario")
    habilidades_perfil = db.relationship("PerfilHabilidadVoluntario", back_populates="voluntario", cascade="all, delete-orphan")
    postulaciones = db.relationship("PostulacionVoluntariado", back_populates="voluntario")


class CategoriaHabilidad(db.Model):
    __tablename__ = "categorias_habilidades"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    habilidades = db.relationship("Habilidad", back_populates="categoria")


class Habilidad(db.Model):
    __tablename__ = "habilidades"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias_habilidades.id", ondelete="RESTRICT"), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    categoria = db.relationship("CategoriaHabilidad", back_populates="habilidades")
    voluntarios_con_habilidad = db.relationship("PerfilHabilidadVoluntario", back_populates="habilidad")


class PerfilHabilidadVoluntario(db.Model):
    __tablename__ = "perfil_habilidades_voluntario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    voluntario_id = db.Column(db.Integer, db.ForeignKey("voluntarios.id", ondelete="CASCADE"), nullable=False)
    habilidad_id = db.Column(db.Integer, db.ForeignKey("habilidades.id", ondelete="RESTRICT"), nullable=False)
    nivel_dominio = db.Column(db.String(30), default="INTERMEDIO", nullable=False)  # BASICO, INTERMEDIO, AVANZADO
    anos_experiencia = db.Column(db.Integer, default=1, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("voluntario_id", "habilidad_id", name="uq_voluntario_habilidad"),
    )

    voluntario = db.relationship("Voluntario", back_populates="habilidades_perfil")
    habilidad = db.relationship("Habilidad", back_populates="voluntarios_con_habilidad")


# ==============================================================================
# MÓDULO 5: CATÁLOGO DE CAUSAS (5 Tablas: ods_objetivos, categorias_causas,
#                               campanas, tipos_necesidad, necesidades_campana)
# ==============================================================================

class OdsObjetivo(db.Model):
    __tablename__ = "ods_objetivos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero_ods = db.Column(db.Integer, unique=True, nullable=False)
    titulo = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    campanas = db.relationship("Campana", back_populates="ods")


class CategoriaCausa(db.Model):
    __tablename__ = "categorias_causas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    campanas = db.relationship("Campana", back_populates="categoria_causa")


class Campana(db.Model):
    __tablename__ = "campanas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fundacion_id = db.Column(db.Integer, db.ForeignKey("fundaciones_osal.id", ondelete="CASCADE"), nullable=False)
    categoria_causa_id = db.Column(db.Integer, db.ForeignKey("categorias_causas.id", ondelete="RESTRICT"), nullable=False)
    ods_id = db.Column(db.Integer, db.ForeignKey("ods_objetivos.id", ondelete="RESTRICT"), nullable=False)
    titulo = db.Column(db.String(160), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    meta_economica = db.Column(db.Numeric(14, 2), default=0, nullable=False)
    monto_recaudado = db.Column(db.Numeric(14, 2), default=0, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(30), default="ACTIVA", nullable=False)  # ACTIVA, PAUSADA, COMPLETADA

    fundacion = db.relationship("FundacionOsal", back_populates="campanas")
    categoria_causa = db.relationship("CategoriaCausa", back_populates="campanas")
    ods = db.relationship("OdsObjetivo", back_populates="campanas")
    necesidades = db.relationship("NecesidadCampana", back_populates="campana", cascade="all, delete-orphan")
    aportes = db.relationship("AporteTransaccional", back_populates="campana")


class TipoNecesidad(db.Model):
    __tablename__ = "tipos_necesidad"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(30), unique=True, nullable=False)  # ECONOMICA, ESPECIE, TIEMPO_VOLUNTARIADO
    nombre = db.Column(db.String(80), nullable=False)

    necesidades = db.relationship("NecesidadCampana", back_populates="tipo_necesidad")


class NecesidadCampana(db.Model):
    __tablename__ = "necesidades_campana"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campana_id = db.Column(db.Integer, db.ForeignKey("campanas.id", ondelete="CASCADE"), nullable=False)
    tipo_necesidad_id = db.Column(db.Integer, db.ForeignKey("tipos_necesidad.id", ondelete="RESTRICT"), nullable=False)
    descripcion_item = db.Column(db.String(200), nullable=False)
    cantidad_requerida = db.Column(db.Numeric(12, 2), default=1, nullable=False)
    cantidad_cubierta = db.Column(db.Numeric(12, 2), default=0, nullable=False)
    prioridad = db.Column(db.String(20), default="ALTA", nullable=False)

    campana = db.relationship("Campana", back_populates="necesidades")
    tipo_necesidad = db.relationship("TipoNecesidad", back_populates="necesidades")
    postulaciones = db.relationship("PostulacionVoluntariado", back_populates="necesidad_campana")


# ==============================================================================
# MÓDULO 6: TRANSACCIONES (8 Tablas: donantes, unidades_medida, metodos_pago,
#                          aportes_transaccionales, donaciones_economicas,
#                          donaciones_especie, trazabilidad_entregas, recibos_tributarios)
# ==============================================================================

class Donante(db.Model):
    __tablename__ = "donantes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    persona_id = db.Column(db.Integer, db.ForeignKey("personas.id", ondelete="CASCADE"), unique=True, nullable=False)
    tipo_donante = db.Column(db.String(30), default="PERSONA_NATURAL", nullable=False)  # PERSONA_NATURAL, EMPRESA
    empresa_organizacion = db.Column(db.String(150), nullable=True)
    requiere_certificado_tributario = db.Column(db.Boolean, default=True, nullable=False)

    persona = db.relationship("Persona", back_populates="donante")
    aportes = db.relationship("AporteTransaccional", back_populates="donante")


class UnidadMedida(db.Model):
    __tablename__ = "unidades_medida"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    simbolo = db.Column(db.String(15), unique=True, nullable=False)  # KG, UND, LT, CAJA
    nombre = db.Column(db.String(60), nullable=False)

    donaciones_especie = db.relationship("DonacionEspecie", back_populates="unidad_medida")


class MetodoPago(db.Model):
    __tablename__ = "metodos_pago"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(30), unique=True, nullable=False)  # TRANSFERENCIA, PSE, NEQUI, DAVIPLATA
    nombre = db.Column(db.String(80), nullable=False)

    donaciones_economicas = db.relationship("DonacionEconomica", back_populates="metodo_pago")


class AporteTransaccional(db.Model):
    __tablename__ = "aportes_transaccionales"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donante_id = db.Column(db.Integer, db.ForeignKey("donantes.id", ondelete="RESTRICT"), nullable=False)
    campana_id = db.Column(db.Integer, db.ForeignKey("campanas.id", ondelete="RESTRICT"), nullable=False)
    codigo_referencia = db.Column(db.String(50), unique=True, nullable=False, index=True)
    modalidad = db.Column(db.String(30), nullable=False)  # ECONOMICA, ESPECIE
    estado_aporte = db.Column(db.String(30), default="REPORTADO", nullable=False)  # REPORTADO, VERIFICADO, RECHAZADO
    url_comprobante = db.Column(db.String(255), nullable=True)
    observaciones = db.Column(db.String(255), nullable=True)
    fecha_aporte = db.Column(db.DateTime, default=utc_now, nullable=False)

    donante = db.relationship("Donante", back_populates="aportes")
    campana = db.relationship("Campana", back_populates="aportes")
    donacion_economica = db.relationship("DonacionEconomica", back_populates="aporte", uselist=False, cascade="all, delete-orphan")
    donacion_especie = db.relationship("DonacionEspecie", back_populates="aporte", uselist=False, cascade="all, delete-orphan")


class DonacionEconomica(db.Model):
    __tablename__ = "donaciones_economicas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aporte_id = db.Column(db.Integer, db.ForeignKey("aportes_transaccionales.id", ondelete="CASCADE"), unique=True, nullable=False)
    metodo_pago_id = db.Column(db.Integer, db.ForeignKey("metodos_pago.id", ondelete="RESTRICT"), nullable=False)
    monto = db.Column(db.Numeric(14, 2), nullable=False)
    moneda = db.Column(db.String(10), default="COP", nullable=False)
    referencia_bancaria = db.Column(db.String(80), nullable=True)

    aporte = db.relationship("AporteTransaccional", back_populates="donacion_economica")
    metodo_pago = db.relationship("MetodoPago", back_populates="donaciones_economicas")
    recibo_tributario = db.relationship("ReciboTributario", back_populates="donacion_economica", uselist=False, cascade="all, delete-orphan")


class DonacionEspecie(db.Model):
    __tablename__ = "donaciones_especie"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aporte_id = db.Column(db.Integer, db.ForeignKey("aportes_transaccionales.id", ondelete="CASCADE"), unique=True, nullable=False)
    unidad_medida_id = db.Column(db.Integer, db.ForeignKey("unidades_medida.id", ondelete="RESTRICT"), nullable=False)
    descripcion_articulos = db.Column(db.String(255), nullable=False)
    cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    estado_logistico_actual = db.Column(db.String(30), default="RECIBIDO", nullable=False)  # RECIBIDO, EN_BODEGA, ENTREGADO

    aporte = db.relationship("AporteTransaccional", back_populates="donacion_especie")
    unidad_medida = db.relationship("UnidadMedida", back_populates="donaciones_especie")
    trazabilidad = db.relationship("TrazabilidadEntrega", back_populates="donacion_especie", cascade="all, delete-orphan")


class TrazabilidadEntrega(db.Model):
    __tablename__ = "trazabilidad_entregas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donacion_especie_id = db.Column(db.Integer, db.ForeignKey("donaciones_especie.id", ondelete="CASCADE"), nullable=False)
    estado_logistico = db.Column(db.String(30), nullable=False)  # RECIBIDO, EN_BODEGA, ENTREGADO
    ubicacion_reportada = db.Column(db.String(150), nullable=False)
    observacion = db.Column(db.String(255), nullable=True)
    fecha_actualizacion = db.Column(db.DateTime, default=utc_now, nullable=False)

    donacion_especie = db.relationship("DonacionEspecie", back_populates="trazabilidad")


class ReciboTributario(db.Model):
    __tablename__ = "recibos_tributarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donacion_economica_id = db.Column(db.Integer, db.ForeignKey("donaciones_economicas.id", ondelete="CASCADE"), unique=True, nullable=False)
    numero_consecutivo = db.Column(db.String(40), unique=True, nullable=False)
    anio_gravable = db.Column(db.Integer, nullable=False)
    hash_verificacion = db.Column(db.String(120), unique=True, nullable=False)
    fecha_emision = db.Column(db.DateTime, default=utc_now, nullable=False)

    donacion_economica = db.relationship("DonacionEconomica", back_populates="recibo_tributario")


# ==============================================================================
# MÓDULO 7: ASIGNACIONES (2 Tablas: postulaciones_voluntariado, asignaciones_actividades)
# ==============================================================================

class PostulacionVoluntariado(db.Model):
    __tablename__ = "postulaciones_voluntariado"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    voluntario_id = db.Column(db.Integer, db.ForeignKey("voluntarios.id", ondelete="CASCADE"), nullable=False)
    necesidad_campana_id = db.Column(db.Integer, db.ForeignKey("necesidades_campana.id", ondelete="CASCADE"), nullable=False)
    motivacion = db.Column(db.String(255), nullable=False)
    disponibilidad_propuesta = db.Column(db.String(120), nullable=False)
    estado_postulacion = db.Column(db.String(30), default="POSTULADO", nullable=False)  # POSTULADO, ACEPTADO, RECHAZADO
    fecha_postulacion = db.Column(db.DateTime, default=utc_now, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("voluntario_id", "necesidad_campana_id", name="uq_voluntario_necesidad"),
    )

    voluntario = db.relationship("Voluntario", back_populates="postulaciones")
    necesidad_campana = db.relationship("NecesidadCampana", back_populates="postulaciones")
    asignacion = db.relationship("AsignacionActividad", back_populates="postulacion", uselist=False, cascade="all, delete-orphan")


class AsignacionActividad(db.Model):
    __tablename__ = "asignaciones_actividades"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    postulacion_id = db.Column(db.Integer, db.ForeignKey("postulaciones_voluntariado.id", ondelete="CASCADE"), unique=True, nullable=False)
    tarea_especifica = db.Column(db.String(200), nullable=False)
    horas_comprometidas = db.Column(db.Integer, default=4, nullable=False)
    horas_cumplidas = db.Column(db.Integer, default=0, nullable=False)
    estado_actividad = db.Column(db.String(30), default="ASIGNADA", nullable=False)  # ASIGNADA, EN_CURSO, FINALIZADA
    fecha_asignacion = db.Column(db.DateTime, default=utc_now, nullable=False)

    postulacion = db.relationship("PostulacionVoluntariado", back_populates="asignacion")

