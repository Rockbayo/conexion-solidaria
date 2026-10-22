"""
Blueprint CU01 - Autenticación y Seguridad (JWT + Auditoría 5FN).
"""
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.extensions import db
from app.models import Usuario, LogAuditoria

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    CU01: Autentica a un actor de la plataforma (OSAL, Donante, Voluntario o Admin),
    registra el evento en logs_auditoria y retorna un JWT firmado con sus roles.
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
        # Registrar intento fallido en logs_auditoria
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
            "mensaje_humano": "El correo o la contraseña no coinciden. Revisa con calma los datos e inténtalo de nuevo."
        }), 401

    if not usuario.esta_activo:
        return jsonify({
            "error": "Cuenta inactiva",
            "mensaje_humano": "Tu cuenta se encuentra temporalmente inactiva. Comunícate con el equipo de soporte comunitario."
        }), 403

    # Extraer roles desde la tabla normalizada usuarios_roles -> roles
    roles = [ur.rol.codigo for ur in usuario.roles_asociados if ur.rol]
    nombre_mostrar = usuario.correo_electronico
    if usuario.persona:
        nombre_mostrar = f"{usuario.persona.nombres} {usuario.persona.apellidos}"

    usuario.ultimo_acceso = datetime.now(timezone.utc)

    # Registrar auditoría de éxito
    log_exito = LogAuditoria(
        usuario_id=usuario.id,
        accion="LOGIN_EXITOSO",
        entidad_afectada="usuarios",
        registro_id=usuario.id,
        detalle=f"Inicio de sesión exitoso con roles: {', '.join(roles)}",
        direccion_ip=request.remote_addr
    )
    db.session.add(log_exito)
    db.session.commit()

    claims_adicionales = {
        "correo_electronico": usuario.correo_electronico,
        "nombre_mostrar": nombre_mostrar,
        "roles": roles,
        "fundacion_id": usuario.fundaciones_administradas[0].id if usuario.fundaciones_administradas else None,
        "voluntario_id": usuario.persona.voluntario.id if (usuario.persona and usuario.persona.voluntario) else None,
        "donante_id": usuario.persona.donante.id if (usuario.persona and usuario.persona.donante) else None,
    }

    access_token = create_access_token(
        identity=str(usuario.id),
        additional_claims=claims_adicionales
    )

    return jsonify({
        "mensaje_humano": f"¡Qué alegría tenerte de vuelta, {nombre_mostrar}!",
        "access_token": access_token,
        "usuario": {
            "id": usuario.id,
            "correo_electronico": usuario.correo_electronico,
            "nombre_mostrar": nombre_mostrar,
            "roles": roles,
            "fundacion_id": claims_adicionales["fundacion_id"],
            "voluntario_id": claims_adicionales["voluntario_id"],
            "donante_id": claims_adicionales["donante_id"],
        }
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def obtener_perfil_actual():
    """Verifica el JWT activo y retorna el contexto del usuario autenticado y sus últimos eventos de auditoría."""
    usuario_id = int(get_jwt_identity())
    claims = get_jwt()
    usuario = db.session.get(Usuario, usuario_id)

    if not usuario:
        return jsonify({
            "error": "Usuario no encontrado",
            "mensaje_humano": "Tu sesión ha expirado. Por favor vuelve a iniciar sesión."
        }), 404

    ultimos_logs = (
        LogAuditoria.query
        .filter_by(usuario_id=usuario.id)
        .order_by(LogAuditoria.fecha_evento.desc())
        .limit(5)
        .all()
    )

    return jsonify({
        "usuario": {
            "id": usuario.id,
            "correo_electronico": usuario.correo_electronico,
            "nombre_mostrar": claims.get("nombre_mostrar", usuario.correo_electronico),
            "roles": claims.get("roles", []),
            "ultimo_acceso": usuario.ultimo_acceso.isoformat() if usuario.ultimo_acceso else None,
            "fundacion_id": claims.get("fundacion_id"),
            "voluntario_id": claims.get("voluntario_id"),
            "donante_id": claims.get("donante_id"),
        },
        "auditoria_reciente": [
            {
                "id": log.id,
                "accion": log.accion,
                "detalle": log.detalle,
                "fecha_evento": log.fecha_evento.isoformat()
            }
            for log in ultimos_logs
        ]
    }), 200
