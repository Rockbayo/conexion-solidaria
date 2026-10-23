"""
Blueprint de Autenticación, Auto-Registro Ciudadano (Voluntario / Donante),
Resumen Personalizado por Rol y Administración de Usuarios RBAC (SUPER_ADMIN y ADMIN).
Aplica la Tríada CIA y el Principio de Mínimo Privilegio.
"""
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.extensions import db
from app.security import requiere_roles
from app.models import (
    Usuario, Rol, UsuarioRol, Persona, DocumentoIdentidad, TipoDocumento,
    Direccion, Municipio, Voluntario, Donante, PerfilHabilidadVoluntario,
    Habilidad, LogAuditoria, ParametroSistema
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
    Autentica a un actor de la plataforma (SUPER_ADMIN, ADMIN, REPRESENTANTE_OSAL, DONANTE o VOLUNTARIO),
    controla intentos fallidos según parametrización y retorna un JWT firmado con sus privilegios.
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

    param_max = ParametroSistema.query.filter_by(clave="MAX_INTENTOS_LOGIN").first()
    try:
        max_intentos = int(param_max.valor) if param_max else 5
    except ValueError:
        max_intentos = 5

    if usuario and not usuario.esta_activo:
        return jsonify({
            "error": "Cuenta bloqueada o inactiva",
            "mensaje_humano": "Tu cuenta se encuentra bloqueada o inactiva por seguridad. Solicita el restablecimiento de tu contraseña al Administrador de la Plataforma."
        }), 403

    if not usuario or not check_password_hash(usuario.hash_contrasena, contrasena):
        if usuario:
            usuario.intentos_fallidos = (usuario.intentos_fallidos or 0) + 1
            if usuario.intentos_fallidos >= max_intentos:
                usuario.esta_activo = False

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

        if usuario and not usuario.esta_activo:
            return jsonify({
                "error": "Cuenta bloqueada preventivamente",
                "mensaje_humano": f"Has superado el límite de {max_intentos} intentos fallidos. Tu cuenta fue bloqueada por seguridad; contacta al Administrador de la Plataforma para restablecer tu acceso."
            }), 403

        return jsonify({
            "error": "Credenciales inválidas",
            "mensaje_humano": "El correo o la contraseña no coinciden. Verifica tus datos e inténtalo de nuevo."
        }), 401

    usuario.intentos_fallidos = 0
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
    Aplica Mínimo Privilegio asignando exclusivamente el rol VOLUNTARIO o DONANTE.
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
        intentos_fallidos=0,
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
    """
    Verifica el JWT activo y retorna el contexto del usuario autenticado, su resumen operativo
    personalizado según su rol (Voluntario, Donante, OSAL o Admin) y su auditoría.
    """
    usuario_id = int(get_jwt_identity())
    claims = get_jwt()
    usuario = db.session.get(Usuario, usuario_id)

    if not usuario:
        return jsonify({
            "error": "Usuario no encontrado",
            "mensaje_humano": "Tu sesión ha expirado. Por favor vuelve a iniciar sesión."
        }), 404

    roles_usuario = [ur.rol.codigo for ur in usuario.roles_asociados if ur.rol]
    if "ADMIN" in roles_usuario or "SUPER_ADMIN" in roles_usuario:
        ultimos_logs = LogAuditoria.query.order_by(LogAuditoria.fecha_evento.desc()).limit(15).all()
    else:
        ultimos_logs = (
            LogAuditoria.query
            .filter_by(usuario_id=usuario.id)
            .order_by(LogAuditoria.fecha_evento.desc())
            .limit(8)
            .all()
        )

    # Construir resumen personalizado del rol
    resumen_voluntario = None
    resumen_donante = None
    fundacion = usuario.fundaciones_administradas[0] if usuario.fundaciones_administradas else None

    if usuario.persona and usuario.persona.voluntario:
        vol = usuario.persona.voluntario
        horas_comprometidas = sum(
            (p.asignacion.horas_comprometidas if p.asignacion else 0)
            for p in vol.postulaciones
            if p.estado_postulacion != "RECHAZADO"
        )
        horas_libres = max(0, int(vol.disponibilidad_horas_semana or 0) - int(horas_comprometidas))
        resumen_voluntario = {
            "voluntario_id": vol.id,
            "disponibilidad_horas_semana": vol.disponibilidad_horas_semana,
            "horas_comprometidas": horas_comprometidas,
            "horas_disponibles_restantes": horas_libres,
            "biografia_corta": vol.biografia_corta,
            "dispuesto_desplazamiento_rural": vol.dispuesto_desplazamiento_rural,
            "municipio": (
                usuario.persona.direccion.municipio.nombre
                if (usuario.persona.direccion and usuario.persona.direccion.municipio)
                else "Sabana Norte"
            ),
            "vereda": usuario.persona.direccion.vereda_o_barrio if usuario.persona.direccion else "",
            "competencias": [
                {
                    "id": ph.id,
                    "habilidad_nombre": ph.habilidad.nombre if ph.habilidad else "General",
                    "categoria_nombre": ph.habilidad.categoria.nombre if (ph.habilidad and ph.habilidad.categoria) else "Comunitaria",
                    "nivel_dominio": ph.nivel_dominio,
                    "anos_experiencia": ph.anos_experiencia,
                }
                for ph in vol.habilidades_perfil
            ],
            "postulaciones": [
                {
                    "id": p.id,
                    "labor_descripcion": p.necesidad_campana.descripcion_item if p.necesidad_campana else "Labor rural",
                    "campana_titulo": (
                        p.necesidad_campana.campana.titulo
                        if (p.necesidad_campana and p.necesidad_campana.campana)
                        else "Campaña Sabana Norte"
                    ),
                    "fundacion_nombre": (
                        p.necesidad_campana.campana.fundacion.razon_social
                        if (p.necesidad_campana and p.necesidad_campana.campana and p.necesidad_campana.campana.fundacion)
                        else "Fundación Sabana Norte"
                    ),
                    "disponibilidad_propuesta": p.disponibilidad_propuesta,
                    "estado_postulacion": p.estado_postulacion,
                    "horas_comprometidas": p.asignacion.horas_comprometidas if p.asignacion else 0,
                    "tarea_especifica": p.asignacion.tarea_especifica if p.asignacion else "",
                    "estado_actividad": p.asignacion.estado_actividad if p.asignacion else "ASIGNADA",
                }
                for p in vol.postulaciones
            ]
        }

    if usuario.persona and usuario.persona.donante:
        don = usuario.persona.donante
        total_cop = sum(
            float(a.donacion_economica.monto)
            for a in don.aportes
            if a.donacion_economica
        )
        resumen_donante = {
            "donante_id": don.id,
            "tipo_donante": don.tipo_donante,
            "empresa_organizacion": don.empresa_organizacion,
            "total_donado_cop": total_cop,
            "total_aportes": len(don.aportes),
            "aportes_recientes": [
                {
                    "id": a.id,
                    "codigo_referencia": a.codigo_referencia,
                    "modalidad": a.modalidad,
                    "campana_titulo": a.campana.titulo if a.campana else "Campaña Sabana Norte",
                    "fundacion_nombre": a.campana.fundacion.razon_social if (a.campana and a.campana.fundacion) else "Fundación Rural",
                    "fecha_aporte": a.fecha_aporte.isoformat() if a.fecha_aporte else None,
                    "monto_cop": float(a.donacion_economica.monto) if a.donacion_economica else None,
                    "donacion_economica_id": a.donacion_economica.id if a.donacion_economica else None,
                    "consecutivo_tributario": (
                        a.donacion_economica.recibo_tributario.numero_consecutivo
                        if (a.donacion_economica and a.donacion_economica.recibo_tributario)
                        else None
                    ),
                    "especie_detalle": (
                        f"{float(a.donacion_especie.cantidad):g} {a.donacion_especie.unidad_medida.simbolo if a.donacion_especie.unidad_medida else 'UND'} · {a.donacion_especie.descripcion_articulos}"
                        if a.donacion_especie
                        else None
                    ),
                    "estado_logistico": a.donacion_especie.estado_logistico_actual if a.donacion_especie else None,
                }
                for a in sorted(don.aportes, key=lambda x: x.id, reverse=True)
            ]
        }

    return jsonify({
        "usuario": {
            "id": usuario.id,
            "correo_electronico": usuario.correo_electronico,
            "nombre_mostrar": claims.get("nombre_mostrar", usuario.correo_electronico),
            "roles": roles_usuario,
            "ultimo_acceso": usuario.ultimo_acceso.isoformat() if usuario.ultimo_acceso else None,
            "fundacion_id": fundacion.id if fundacion else claims.get("fundacion_id"),
            "fundacion_nombre": fundacion.razon_social if fundacion else claims.get("fundacion_nombre"),
            "fundacion_estado": fundacion.estado_validacion if fundacion else claims.get("fundacion_estado"),
            "voluntario_id": claims.get("voluntario_id"),
            "donante_id": claims.get("donante_id"),
        },
        "resumen_voluntario": resumen_voluntario,
        "resumen_donante": resumen_donante,
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


# ==============================================================================
# ADMINISTRACIÓN DE USUARIOS Y CREDENCIALES (Roles: ADMIN y SUPER_ADMIN)
# ==============================================================================

@auth_bp.route("/usuarios", methods=["GET"])
@requiere_roles("ADMIN")
def listar_usuarios_sistema():
    """Retorna el directorio completo de usuarios para gobernanza administrativa."""
    usuarios = Usuario.query.order_by(Usuario.id.asc()).all()
    resultado = []

    for u in usuarios:
        roles = [ur.rol.codigo for ur in u.roles_asociados if ur.rol]
        nombre_completo = u.correo_electronico
        telefono = "Sin registro"
        documento = "N/A"
        municipio = "Sabana Norte"

        if u.persona:
            nombre_completo = f"{u.persona.nombres} {u.persona.apellidos}"
            telefono = u.persona.telefono_contacto or "Sin registro"
            if u.persona.documento_identidad:
                documento = u.persona.documento_identidad.numero_documento
            if u.persona.direccion and u.persona.direccion.municipio:
                municipio = u.persona.direccion.municipio.nombre

        resultado.append({
            "id": u.id,
            "correo_electronico": u.correo_electronico,
            "nombre_completo": nombre_completo,
            "telefono": telefono,
            "documento": documento,
            "municipio": municipio,
            "roles": roles,
            "esta_activo": u.esta_activo,
            "intentos_fallidos": u.intentos_fallidos or 0,
            "ultimo_acceso": u.ultimo_acceso.isoformat() if u.ultimo_acceso else None,
        })

    return jsonify({"usuarios": resultado}), 200


@auth_bp.route("/usuarios", methods=["POST"])
@requiere_roles("ADMIN")
def crear_usuario_administrado():
    """
    Permite a ADMIN o SUPER_ADMIN crear cuentas de usuario.
    Regla estricta de negocio: Solo SUPER_ADMIN puede crear usuarios con rol ADMIN o SUPER_ADMIN.
    """
    claims = get_jwt()
    roles_solicitante = set(claims.get("roles") or [])
    solicitante_id = int(get_jwt_identity())

    data = request.get_json(silent=True) or {}
    rol_destino = (data.get("rol_codigo") or "ADMIN").strip().upper()
    nombres = (data.get("nombres") or "").strip()
    apellidos = (data.get("apellidos") or "").strip()
    correo = (data.get("correo_electronico") or "").strip().lower()
    contrasena = data.get("contrasena") or ""
    telefono = (data.get("telefono_contacto") or "3100000000").strip()
    numero_documento = (data.get("numero_documento") or "").strip()
    municipio_id = int(data.get("municipio_id") or 6)

    if rol_destino in ("ADMIN", "SUPER_ADMIN") and "SUPER_ADMIN" not in roles_solicitante:
        return jsonify({
            "error": "Privilegio exclusivo de Superusuario",
            "mensaje_humano": "Solo el Superusuario de la Plataforma (SUPER_ADMIN) está autorizado para crear cuentas de Administrador."
        }), 403

    if not all([nombres, apellidos, correo, contrasena]):
        return jsonify({
            "error": "Datos incompletos",
            "mensaje_humano": "Por favor completa nombres, apellidos, correo electrónico y contraseña inicial."
        }), 400

    if len(contrasena) < 6:
        return jsonify({
            "error": "Contraseña corta",
            "mensaje_humano": "La contraseña inicial debe tener al menos 6 caracteres."
        }), 400

    if Usuario.query.filter_by(correo_electronico=correo).first():
        return jsonify({
            "error": "Correo duplicado",
            "mensaje_humano": f"Ya existe un usuario registrado con el correo {correo}."
        }), 409

    if numero_documento and DocumentoIdentidad.query.filter_by(numero_documento=numero_documento).first():
        return jsonify({
            "error": "Documento duplicado",
            "mensaje_humano": f"El número de documento {numero_documento} ya pertenece a otro usuario."
        }), 409

    municipio = db.session.get(Municipio, municipio_id) or Municipio.query.first()
    nueva_dir = Direccion(
        municipio_id=municipio.id,
        vereda_o_barrio="Sede Administrativa / Municipal",
        direccion_fisica=f"Jurisdicción {municipio.nombre}",
        indicaciones_rurales="Cuenta creada por administración",
        latitud=float(municipio.latitud_centro or 4.9500),
        longitud=float(municipio.longitud_centro or -74.0100)
    )
    db.session.add(nueva_dir)
    db.session.flush()

    nuevo_u = Usuario(
        correo_electronico=correo,
        hash_contrasena=generate_password_hash(contrasena),
        esta_activo=True,
        intentos_fallidos=0
    )
    db.session.add(nuevo_u)
    db.session.flush()

    rol_obj = Rol.query.filter_by(codigo=rol_destino).first()
    if not rol_obj:
        rol_obj = Rol(codigo=rol_destino, nombre=rol_destino, descripcion="Rol del sistema")
        db.session.add(rol_obj)
        db.session.flush()

    db.session.add(UsuarioRol(usuario_id=nuevo_u.id, rol_id=rol_obj.id))

    persona = Persona(
        usuario_id=nuevo_u.id,
        direccion_id=nueva_dir.id,
        nombres=nombres,
        apellidos=apellidos,
        telefono_contacto=telefono
    )
    db.session.add(persona)
    db.session.flush()

    if numero_documento:
        td = TipoDocumento.query.first()
        if td:
            db.session.add(DocumentoIdentidad(
                persona_id=persona.id,
                tipo_documento_id=td.id,
                numero_documento=numero_documento
            ))

    if rol_destino == "VOLUNTARIO":
        db.session.add(Voluntario(persona_id=persona.id, disponibilidad_horas_semana=6, biografia_corta="Voluntario registrado por administración", dispuesto_desplazamiento_rural=True, activo=True))
    elif rol_destino == "DONANTE":
        db.session.add(Donante(persona_id=persona.id, tipo_donante="PERSONA_NATURAL", requiere_certificado_tributario=True))

    db.session.add(LogAuditoria(
        usuario_id=solicitante_id,
        accion=f"CREAR_USUARIO_{rol_destino}",
        entidad_afectada="usuarios",
        registro_id=nuevo_u.id,
        detalle=f"Creado usuario {correo} con rol {rol_destino}.",
        direccion_ip=request.remote_addr
    ))
    db.session.commit()

    return jsonify({
        "mensaje_humano": f"Usuario '{nombres} {apellidos}' ({correo}) creado exitosamente con el perfil {rol_destino}.",
        "usuario_id": nuevo_u.id
    }), 201


@auth_bp.route("/usuarios/<int:target_id>/restablecer-clave", methods=["PUT"])
@requiere_roles("ADMIN")
def restablecer_clave_usuario(target_id: int):
    """Permite a ADMIN o SUPER_ADMIN restablecer la contraseña de un usuario y desbloquear su cuenta."""
    claims = get_jwt()
    roles_solicitante = set(claims.get("roles") or [])
    solicitante_id = int(get_jwt_identity())

    target = db.session.get(Usuario, target_id)
    if not target:
        return jsonify({
            "error": "Usuario no encontrado",
            "mensaje_humano": "No se encontró la cuenta de usuario seleccionada."
        }), 404

    roles_target = {ur.rol.codigo for ur in target.roles_asociados if ur.rol}
    if "SUPER_ADMIN" in roles_target and "SUPER_ADMIN" not in roles_solicitante:
        return jsonify({
            "error": "Operación restringida",
            "mensaje_humano": "Un Administrador no puede modificar las credenciales del Superusuario de la Plataforma."
        }), 403

    data = request.get_json(silent=True) or {}
    nueva_clave = (data.get("nueva_contrasena") or "").strip()
    if len(nueva_clave) < 6:
        return jsonify({
            "error": "Contraseña inválida",
            "mensaje_humano": "La nueva contraseña debe tener al menos 6 caracteres."
        }), 400

    target.hash_contrasena = generate_password_hash(nueva_clave)
    target.intentos_fallidos = 0
    target.esta_activo = True

    db.session.add(LogAuditoria(
        usuario_id=solicitante_id,
        accion="RESTABLECER_CONTRASENA_USUARIO",
        entidad_afectada="usuarios",
        registro_id=target.id,
        detalle=f"Contraseña restablecida y cuenta desbloqueada para {target.correo_electronico}.",
        direccion_ip=request.remote_addr
    ))
    db.session.commit()

    return jsonify({
        "mensaje_humano": f"La contraseña de {target.correo_electronico} fue restablecida y su cuenta quedó activa."
    }), 200


@auth_bp.route("/usuarios/<int:target_id>/estado", methods=["PUT"])
@requiere_roles("ADMIN")
def cambiar_estado_usuario(target_id: int):
    """Permite a ADMIN o SUPER_ADMIN activar o suspender/bloquear una cuenta de usuario."""
    claims = get_jwt()
    roles_solicitante = set(claims.get("roles") or [])
    solicitante_id = int(get_jwt_identity())

    target = db.session.get(Usuario, target_id)
    if not target:
        return jsonify({"error": "No encontrado", "mensaje_humano": "Usuario no encontrado."}), 404

    roles_target = {ur.rol.codigo for ur in target.roles_asociados if ur.rol}
    if "SUPER_ADMIN" in roles_target and "SUPER_ADMIN" not in roles_solicitante:
        return jsonify({
            "error": "Operación restringida",
            "mensaje_humano": "No tienes permisos para suspender al Superusuario de la Plataforma."
        }), 403

    data = request.get_json(silent=True) or {}
    nuevo_estado = bool(data.get("esta_activo", True))
    target.esta_activo = nuevo_estado
    if nuevo_estado:
        target.intentos_fallidos = 0

    accion_txt = "ACTIVAR_USUARIO" if nuevo_estado else "SUSPENDER_USUARIO"
    db.session.add(LogAuditoria(
        usuario_id=solicitante_id,
        accion=accion_txt,
        entidad_afectada="usuarios",
        registro_id=target.id,
        detalle=f"Estado de cuenta de {target.correo_electronico} actualizado a {'ACTIVO' if nuevo_estado else 'INACTIVO'}.",
        direccion_ip=request.remote_addr
    ))
    db.session.commit()

    return jsonify({
        "mensaje_humano": f"La cuenta {target.correo_electronico} ahora está {'Activa' if nuevo_estado else 'Suspendida'}."
    }), 200
