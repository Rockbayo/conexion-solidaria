"""
Módulo de Seguridad Aplicada: Tríada CIA (Confidencialidad, Integridad, Disponibilidad)
y Principio de Mínimo Privilegio (PoLP / RBAC) sobre JWT para Flask.
"""
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from app.extensions import db
from app.models import LogAuditoria


def requiere_roles(*roles_permitidos: str):
    """
    Decorador de Principio de Mínimo Privilegio (RBAC).
    1. Exige un JWT válido firmado criptográficamente (Confidencialidad).
    2. Verifica que el usuario posea al menos uno de los roles autorizados para el recurso.
    3. Registra intentos de acceso no autorizado en logs_auditoria (Integridad / No Repudio).
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
            except Exception:
                return jsonify({
                    "error": "Autenticación requerida",
                    "mensaje_humano": "Debes iniciar sesión con tu cuenta para realizar esta operación en la plataforma."
                }), 401

            claims = get_jwt()
            roles_usuario = set(claims.get("roles") or [])
            identidad = get_jwt_identity()
            usuario_id = int(identidad) if identidad else None

            if roles_permitidos and not roles_usuario.intersection(set(roles_permitidos)):
                db.session.add(LogAuditoria(
                    usuario_id=usuario_id,
                    accion="ACCESO_DENEGADO_MINIMO_PRIVILEGIO",
                    entidad_afectada=request.path,
                    registro_id=None,
                    detalle=(
                        f"Bloqueado por Mínimo Privilegio. Roles usuario: {list(roles_usuario)} | "
                        f"Roles requeridos: {list(roles_permitidos)}"
                    ),
                    direccion_ip=request.remote_addr
                ))
                db.session.commit()
                return jsonify({
                    "error": "Permisos insuficientes (Principio de Mínimo Privilegio)",
                    "mensaje_humano": (
                        f"Tu perfil actual ({', '.join(roles_usuario) or 'Sin rol'}) no tiene privilegios "
                        f"para ejecutar esta operación exclusiva de: {', '.join(roles_permitidos)}."
                    )
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper
