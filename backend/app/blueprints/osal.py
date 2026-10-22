"""
Blueprint CU02 - Registro de OSAL (Formulario Wizard y Documentos Legales en 5FN).
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models import (
    Usuario, Rol, UsuarioRol, Persona, DocumentoIdentidad, TipoDocumento,
    Direccion, Municipio, FundacionOsal, DocumentoLegalOsal, LogAuditoria
)

osal_bp = Blueprint("osal", __name__, url_prefix="/api/osal")


@osal_bp.route("/registro", methods=["POST"])
def registrar_osal():
    """
    CU02: Registra una Organización Sin Ánimo de Lucro (OSAL) desde el Wizard de 3 pasos.
    Persiste en 5FN: usuarios, usuarios_roles, direcciones, personas, documentos_identidad,
    fundaciones_osal (estado_validacion='PENDIENTE') y documentos_legales_osal.
    """
    data = request.get_json(silent=True) or {}

    nit = (data.get("nit") or "").strip()
    razon_social = (data.get("razon_social") or "").strip()
    sigla = (data.get("sigla") or "").strip()
    mision = (data.get("mision") or "").strip()
    telefono_institucional = (data.get("telefono_institucional") or "").strip()
    fecha_constitucion_str = data.get("fecha_constitucion")

    # Ubicación rural en Sabana Norte
    municipio_id = data.get("municipio_id")
    vereda_o_barrio = (data.get("vereda_o_barrio") or "").strip()
    direccion_fisica = (data.get("direccion_fisica") or "").strip()
    indicaciones_rurales = (data.get("indicaciones_rurales") or "").strip()
    latitud = data.get("latitud")
    longitud = data.get("longitud")

    # Datos del representante legal
    correo_representante = (data.get("correo_electronico") or "").strip().lower()
    contrasena = data.get("contrasena") or "Solidaria2026*"
    nombres_rep = (data.get("nombres_representante") or "").strip()
    apellidos_rep = (data.get("apellidos_representante") or "").strip()
    numero_doc_rep = (data.get("numero_documento_representante") or "").strip()
    tipo_documento_id = data.get("tipo_documento_id")

    # Soportes legales cargados en el paso 3 del Wizard
    documentos_legales = data.get("documentos_legales") or []

    if not all([nit, razon_social, mision, telefono_institucional, municipio_id, vereda_o_barrio, direccion_fisica, correo_representante, nombres_rep, apellidos_rep]):
        return jsonify({
            "error": "Campos obligatorios faltantes",
            "mensaje_humano": "Faltan algunos datos importantes de tu fundación o ubicación veredal. Revisa los pasos del formulario."
        }), 400

    if FundacionOsal.query.filter_by(nit=nit).first():
        return jsonify({
            "error": "NIT duplicado",
            "mensaje_humano": f"Ya existe una fundación registrada con el NIT {nit}. Si eres su representante, inicia sesión."
        }), 409

    if Usuario.query.filter_by(correo_electronico=correo_representante).first():
        return jsonify({
            "error": "Correo duplicado",
            "mensaje_humano": f"El correo {correo_representante} ya está registrado en la plataforma."
        }), 409

    municipio = db.session.get(Municipio, int(municipio_id))
    if not municipio:
        return jsonify({
            "error": "Municipio inválido",
            "mensaje_humano": "Selecciona un municipio válido de la Sabana Norte de Cundinamarca."
        }), 400

    # Coordenadas por defecto al centro del municipio si el usuario rural no tiene GPS activo
    lat_final = float(latitud) if latitud is not None else float(municipio.latitud_centro or 4.9500)
    lon_final = float(longitud) if longitud is not None else float(municipio.longitud_centro or -74.0100)

    # 1. Crear dirección georreferenciada
    nueva_direccion = Direccion(
        municipio_id=municipio.id,
        vereda_o_barrio=vereda_o_barrio,
        direccion_fisica=direccion_fisica,
        indicaciones_rurales=indicaciones_rurales,
        latitud=lat_final,
        longitud=lon_final
    )
    db.session.add(nueva_direccion)
    db.session.flush()

    # 2. Crear usuario y asignar rol REPRESENTANTE_OSAL
    nuevo_usuario = Usuario(
        correo_electronico=correo_representante,
        hash_contrasena=generate_password_hash(contrasena),
        esta_activo=True
    )
    db.session.add(nuevo_usuario)
    db.session.flush()

    rol_osal = Rol.query.filter_by(codigo="REPRESENTANTE_OSAL").first()
    if rol_osal:
        db.session.add(UsuarioRol(usuario_id=nuevo_usuario.id, rol_id=rol_osal.id))

    # 3. Crear Persona y DocumentoIdentidad
    nueva_persona = Persona(
        usuario_id=nuevo_usuario.id,
        direccion_id=nueva_direccion.id,
        nombres=nombres_rep,
        apellidos=apellidos_rep,
        telefono_contacto=telefono_institucional
    )
    db.session.add(nueva_persona)
    db.session.flush()

    if numero_doc_rep:
        td = db.session.get(TipoDocumento, int(tipo_documento_id)) if tipo_documento_id else TipoDocumento.query.first()
        if td and not DocumentoIdentidad.query.filter_by(numero_documento=numero_doc_rep).first():
            db.session.add(DocumentoIdentidad(
                persona_id=nueva_persona.id,
                tipo_documento_id=td.id,
                numero_documento=numero_doc_rep
            ))

    # 4. Crear Fundación OSAL en estado PENDIENTE de validación
    fecha_const = None
    if fecha_constitucion_str:
        try:
            fecha_const = datetime.strptime(fecha_constitucion_str, "%Y-%m-%d").date()
        except ValueError:
            fecha_const = None

    nueva_fundacion = FundacionOsal(
        usuario_representante_id=nuevo_usuario.id,
        direccion_id=nueva_direccion.id,
        nit=nit,
        razon_social=razon_social,
        sigla=sigla or None,
        mision=mision,
        telefono_institucional=telefono_institucional,
        estado_validacion="PENDIENTE",
        fecha_constitucion=fecha_const
    )
    db.session.add(nueva_fundacion)
    db.session.flush()

    # 5. Registrar Documentos Legales en documentos_legales_osal
    if not documentos_legales:
        documentos_legales = [
            {"tipo_soporte": "RUT_DIAN", "nombre_archivo": f"RUT_{nit}.pdf"},
            {"tipo_soporte": "CERTIFICADO_EXISTENCIA_CAMARA", "nombre_archivo": f"CamaraComercio_{nit}.pdf"},
        ]

    soportes_creados = []
    for doc in documentos_legales:
        tipo_sop = (doc.get("tipo_soporte") or "SOPORTE_LEGAL").upper()
        nom_arch = doc.get("nombre_archivo") or f"{tipo_sop}_{nit}.pdf"
        soporte = DocumentoLegalOsal(
            fundacion_id=nueva_fundacion.id,
            tipo_soporte=tipo_sop,
            nombre_archivo=nom_arch,
            url_archivo=f"/uploads/osal/{nueva_fundacion.id}/{nom_arch}",
            estado_revision="EN_REVISION"
        )
        db.session.add(soporte)
        soportes_creados.append({"tipo_soporte": tipo_sop, "nombre_archivo": nom_arch, "estado_revision": "EN_REVISION"})

    # 6. Registrar en logs_auditoria
    db.session.add(LogAuditoria(
        usuario_id=nuevo_usuario.id,
        accion="REGISTRO_OSAL_PENDIENTE",
        entidad_afectada="fundaciones_osal",
        registro_id=nueva_fundacion.id,
        detalle=f"OSAL '{razon_social}' (NIT {nit}) registrada en {municipio.nombre} con estado PENDIENTE.",
        direccion_ip=request.remote_addr
    ))

    db.session.commit()

    return jsonify({
        "mensaje_humano": f"¡Gracias! Hemos recibido el registro de '{razon_social}' en {municipio.nombre}. Tu fundación quedó en estado PENDIENTE DE VALIDACIÓN mientras revisamos tus documentos legales.",
        "fundacion": {
            "id": nueva_fundacion.id,
            "nit": nueva_fundacion.nit,
            "razon_social": nueva_fundacion.razon_social,
            "sigla": nueva_fundacion.sigla,
            "municipio": municipio.nombre,
            "vereda_o_barrio": nueva_direccion.vereda_o_barrio,
            "estado_validacion": nueva_fundacion.estado_validacion,
            "documentos_legales": soportes_creados
        }
    }), 201


@osal_bp.route("", methods=["GET"])
def listar_fundaciones():
    """Retorna las fundaciones OSAL registradas con su dirección, municipio y soportes legales."""
    fundaciones = FundacionOsal.query.order_by(FundacionOsal.fecha_registro.desc()).all()
    resultado = []
    for f in fundaciones:
        resultado.append({
            "id": f.id,
            "nit": f.nit,
            "razon_social": f.razon_social,
            "sigla": f.sigla,
            "mision": f.mision,
            "telefono_institucional": f.telefono_institucional,
            "estado_validacion": f.estado_validacion,
            "municipio": f.direccion.municipio.nombre if (f.direccion and f.direccion.municipio) else "Sabana Norte",
            "vereda_o_barrio": f.direccion.vereda_o_barrio if f.direccion else "",
            "direccion_fisica": f.direccion.direccion_fisica if f.direccion else "",
            "latitud": float(f.direccion.latitud) if f.direccion else 4.95,
            "longitud": float(f.direccion.longitud) if f.direccion else -74.01,
            "total_documentos": len(f.documentos_legales)
        })
    return jsonify({"fundaciones": resultado}), 200
