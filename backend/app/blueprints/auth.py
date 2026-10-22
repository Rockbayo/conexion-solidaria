"""
Blueprint de Autenticación, Auto-Registro Ciudadano (Voluntario / Donante) y Gobernanza RBAC.
Aplica la Tríada CIA (Confidencialidad con Hash/JWT, Integridad 5FN y Auditoría) y Mínimo Privilegio.
"""
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.extensions import db
from app.models import (
    Usuario, Rol, UsuarioRol, Persona, DocumentoIdentidad, TipoDocumento,
    Direccion, Municipio, Voluntario, Donante, PerfilHabilidadVoluntario,
    Habilidad, LogAuditoria
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def construir_respuesta_sesion(usuario: Usuario, mensaje: str):
    roles = [ur.rol.codigo for ur in usuario.roles_asociados if ur.rol]
    nombre_mostrar = usuario.correo_electronico
    if usuario.persona:
        nombre_mostrar = f"{usuario.persona.nombres} {usuario.persona.apellidos}"

    fundacion = usuario.fundaciones_administradas[0] if usuario.fundaciones_administradas else None

    claims_adicionales = {
        "correo_electronico": usuario.correo_electronico,
        "nombre_mostrar": nombre_mostrar,
        "roles": roles,
        "fundacion_id": fundacion.id if fundacion else None,
        "fundacion_nombre": fundacion.razon_social if fundacion else None,
        "fundacion_estado": fundacion.estado_validacion if fundacion else None,
        "voluntario_id": usuario.persona.voluntario.id if (usuario.persona and usuario.persona.voluntario) else None,
        "donante_id": usuario.persona.donante.id if (usuario.persona and usuario.persona.donante) else None,
    }

    access_token = create_access_token(
        identity=str(usuario.id),
        additional_claims=claims_adicionales
    )

    return {
        "mensaje_humano": mensaje,
        "access_token": access_token,
        "usuario": {
            "id": usuario.id,
            "correo_electronico": usuario.correo_electronico,
            "nombre_mostrar": nombre_mostrar,
            "roles": roles,
            "fundacion_id": claims_adicionales["fundacion_id"],
            "fundacion_nombre": claims_adicionales["fundacion_nombre"],
            "fundacion_estado": claims_adicionales["fundacion_estado"],
            "voluntario_id": claims_adicionales["voluntario_id"],
            "donante_id": claims_adicionales["donante_id"],
        }
    }


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Autentica a un actor de la plataforma (ADMIN, REPRESENTANTE_OSAL, DONANTE o VOLUNTARIO),
    registra el evento en logs_auditoria y retorna un JWT firmado con sus privilegios exactos.
    """
    data = request.get_json(silent=True) or {}
    correo = (data.get("correo_electronico") or "").strip().lower()
    contrasena = data.get("contrasena") or ""

    if not correo or not contrasena:
        return jsonify({
            "error": "Datos incompletos",
            "mensaje_humano": "Por favor escribe tu correo electrónico y tu contraseña para ingresar."
        }), 400

    usuario = Usuario.query.filter_by(correo_electronico=correo).first()

    if not usuario or not check_password_hash(usuario.hash_contrasena, contrasena):
        log_fallo = LogAuditoria(
            usuario_id=usuario.id if usuario else None,
            accion="LOGIN_FALLIDO",
            entidad_afectada="usuarios",
            registro_id=usuario.id if usuario else None,
            detalle=f"Intento de acceso fallido para correo: {correo}",
            direccion_ip=request.remote_addr
        )
        db.session.add(log_fallo)
        db.session.commit()

        return jsonify({
            "error": "Credenciales inválidas",
            "mensaje_humano": "El correo o la contraseña no coinciden. Verifica tus datos e inténtalo de nuevo."
        }), 401

    if not usuario.esta_activo:
        return jsonify({
            "error": "Cuenta inactiva",
            "mensaje_humano": "Tu cuenta se encuentra temporalmente inactiva. Comunícate con la administración de la plataforma."
        }), 403

    roles = [ur.rol.codigo for ur in usuario.roles_asociados if ur.rol]
    usuario.ultimo_acceso = datetime.now(timezone.utc)

    db.session.add(LogAuditoria(
        usuario_id=usuario.id,
        accion="INGRESO_AL_SISTEMA",
        entidad_afectada="usuarios",
        registro_id=usuario.id,
        detalle="Inicio de sesión exitoso en la plataforma.",
        direccion_ip=request.remote_addr
    ))
    db.session.commit()

    nombre = f"{usuario.persona.nombres} {usuario.persona.apellidos}" if usuario.persona else usuario.correo_electronico
    return jsonify(construir_respuesta_sesion(usuario, f"Bienvenido(a), {nombre}.")), 200


@auth_bp.route("/registro-ciudadano", methods=["POST"])
def registrar_ciudadano():
    """
    Auto-Registro Público para Voluntarios y Donantes en la Sabana Norte.
    Aplica Mínimo Privilegio asignando exclusivamente el rol VOLUNTARIO o DONANTE,
    crea su registro en usuarios, personas, documentos_identidad, direcciones y en
    voluntarios (con habilidad inicial opcional) o donantes.
    """
    data = request.get_json(silent=True) or {}

    tipo_actor = (data.get("tipo_actor") or "VOLUNTARIO").strip().upper()
    if tipo_actor not in ("VOLUNTARIO", "DONANTE"):
        return jsonify({
            "error": "Rol no permitido en auto-registro",
            "mensaje_humano": "Solo puedes registrarte directamente como Voluntario o como Donante."
        }), 400

    nombres = (data.get("nombres") or "").strip()
    apellidos = (data.get("apellidos") or "").strip()
    correo = (data.get("correo_electronico") or "").strip().lower()
    contrasena = data.get("contrasena") or ""
    telefono = (data.get("telefono_contacto") or "").strip()
    tipo_documento_id = data.get("tipo_documento_id") or 1
    numero_documento = (data.get("numero_documento") or "").strip()
    municipio_id = data.get("municipio_id") or 6
    vereda_o_barrio = (data.get("vereda_o_barrio") or "Casco Urbano / Vereda").strip()
    direccion_fisica = (data.get("direccion_fisica") or "Sabana Norte").strip()

    if not all([nombres, apellidos, correo, contrasena, telefono, numero_documento]):
        return jsonify({
            "error": "Datos obligatorios incompletos",
            "mensaje_humano": "Por favor completa tus nombres, apellidos, documento, teléfono, correo y contraseña."
        }), 400

    if len(contrasena) < 6:
        return jsonify({
            "error": "Contraseña corta",
            "mensaje_humano": "Por favor escribe una contraseña de al menos 6 caracteres."
        }), 400

    if Usuario.query.filter_by(correo_electronico=correo).first():
        return jsonify({
            "error": "Correo ya registrado",
            "mensaje_humano": f"El correo {correo} ya tiene una cuenta activa. Inicia sesión con tus credenciales."
        }), 409

    if DocumentoIdentidad.query.filter_by(numero_documento=numero_documento).first():
        return jsonify({
            "error": "Documento duplicado",
            "mensaje_humano": f"El número de documento {numero_documento} ya se encuentra registrado en la plataforma."
        }), 409

    municipio = db.session.get(Municipio, int(municipio_id)) or Municipio.query.first()
    nueva_dir = Direccion(
        municipio_id=municipio.id,
        vereda_o_barrio=vereda_o_barrio,
        direccion_fisica=direccion_fisica,
        indicaciones_rurales="Registro ciudadano Sabana Norte",
        latitud=float(municipio.latitud_centro or 4.9500),
        longitud=float(municipio.longitud_centro or -74.0100)
    )
    db.session.add(nueva_dir)
    db.session.flush()

    nuevo_usuario = Usuario(
        correo_electronico=correo,
        hash_contrasena=generate_password_hash(contrasena),
        esta_activo=True,
        ultimo_acceso=datetime.now(timezone.utc)
    )
    db.session.add(nuevo_usuario)
    db.session.flush()

    rol_obj = Rol.query.filter_by(codigo=tipo_actor).first()
    if rol_obj:
        db.session.add(UsuarioRol(usuario_id=nuevo_usuario.id, rol_id=rol_obj.id))

    nueva_persona = Persona(
        usuario_id=nuevo_usuario.id,
        direccion_id=nueva_dir.id,
        nombres=nombres,
        apellidos=apellidos,
        telefono_contacto=telefono
    )
    db.session.add(nueva_persona)
    db.session.flush()

    td = db.session.get(TipoDocumento, int(tipo_documento_id)) or TipoDocumento.query.first()
    db.session.add(DocumentoIdentidad(
        persona_id=nueva_persona.id,
        tipo_documento_id=td.id,
        numero_documento=numero_documento
    ))

    if tipo_actor == "VOLUNTARIO":
        disp_horas = int(data.get("disponibilidad_horas_semana") or 6)
        biografia = (data.get("biografia_corta") or "Voluntario comprometido con el desarrollo rural de Sabana Norte.").strip()
        desplazamiento = bool(data.get("dispuesto_desplazamiento_rural", True))

        nuevo_vol = Voluntario(
            persona_id=nueva_persona.id,
            disponibilidad_horas_semana=disp_horas,
            biografia_corta=biografia,
            dispuesto_desplazamiento_rural=desplazamiento,
            activo=True
        )
        db.session.add(nuevo_vol)
        db.session.flush()

        habilidad_id = data.get("habilidad_inicial_id")
        if habilidad_id:
            hab = db.session.get(Habilidad, int(habilidad_id))
            if hab:
                db.session.add(PerfilHabilidadVoluntario(
                    voluntario_id=nuevo_vol.id,
                    habilidad_id=hab.id,
                    nivel_dominio=(data.get("nivel_dominio") or "INTERMEDIO").upper(),
                    anos_experiencia=int(data.get("anos_experiencia") or 1)
                ))
    else:
        tipo_donante = (data.get("tipo_donante") or "PERSONA_NATURAL").upper()
        empresa = (data.get("empresa_organizacion") or "").strip() or None
        nuevo_don = Donante(
            persona_id=nueva_persona.id,
            tipo_donante=tipo_donante,
            empresa_organizacion=empresa,
            requiere_certificado_tributario=True
        )
        db.session.add(nuevo_don)
        db.session.flush()

    db.session.add(LogAuditoria(
        usuario_id=nuevo_usuario.id,
        accion=f"REGISTRO_{tipo_actor}",
        entidad_afectada="usuarios",
        registro_id=nuevo_usuario.id,
        detalle=f"Inscripción completada como {tipo_actor.lower()} en {municipio.nombre}.",
        direccion_ip=request.remote_addr
    ))

    db.session.commit()

    return jsonify(
        construir_respuesta_sesion(
            nuevo_usuario,
            f"¡Tu cuenta de {tipo_actor.capitalize()} ha sido creada con éxito, {nombres}! Ya tienes sesión activa."
        )
    ), 201


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def obtener_perfil_actual():
    """Verifica el JWT activo y retorna el contexto del usuario autenticado y su auditoría."""
    usuario_id = int(get_jwt_identity())
    claims = get_jwt()
    usuario = db.session.get(Usuario, usuario_id)

    if not usuario:
        return jsonify({
            "error": "Usuario no encontrado",
            "mensaje_humano": "Tu sesión ha expirado. Por favor vuelve a iniciar sesión."
        }), 404

    roles_usuario = claims.get("roles", [])
    if "ADMIN" in roles_usuario:
        # El Administrador de la Plataforma audita toda la bitácora global
        ultimos_logs = LogAuditoria.query.order_by(LogAuditoria.fecha_evento.desc()).limit(15).all()
    else:
        ultimos_logs = (
            LogAuditoria.query
            .filter_by(usuario_id=usuario.id)
            .order_by(LogAuditoria.fecha_evento.desc())
            .limit(8)
            .all()
        )

    return jsonify({
        "usuario": {
            "id": usuario.id,
            "correo_electronico": usuario.correo_electronico,
            "nombre_mostrar": claims.get("nombre_mostrar", usuario.correo_electronico),
            "roles": roles_usuario,
            "ultimo_acceso": usuario.ultimo_acceso.isoformat() if usuario.ultimo_acceso else None,
            "fundacion_id": claims.get("fundacion_id"),
            "fundacion_nombre": claims.get("fundacion_nombre"),
            "fundacion_estado": claims.get("fundacion_estado"),
            "voluntario_id": claims.get("voluntario_id"),
            "donante_id": claims.get("donante_id"),
        },
        "auditoria_reciente": [
            {
                "id": log.id,
                "accion": log.accion,
                "entidad_afectada": log.entidad_afectada,
                "detalle": log.detalle,
                "direccion_ip": log.direccion_ip,
                "fecha_evento": log.fecha_evento.isoformat()
            }
            for log in ultimos_logs
        ]
    }), 200
