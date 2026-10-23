"""
Blueprint de Voluntariado y Asignaciones (5FN):
- CU05: Postulación Voluntariado (postulaciones_voluntariado, asignaciones_actividades, necesidades_campana)
- CU10: Perfil de Habilidades (voluntarios, categorias_habilidades, habilidades, perfil_habilidades_voluntario)
Aplica privacidad por rol (cada voluntario ve únicamente sus propias postulaciones) y validación de tope horario.
"""
from decimal import Decimal
from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app.extensions import db
from app.security import requiere_roles
from app.models import (
    Voluntario, Habilidad, PerfilHabilidadVoluntario,
    NecesidadCampana, PostulacionVoluntariado, AsignacionActividad, LogAuditoria
)

voluntariado_bp = Blueprint("voluntariado", __name__, url_prefix="/api/voluntariado")


@voluntariado_bp.route("/labores", methods=["GET"])
def listar_labores_voluntariado():
    """
    Lista las labores de voluntariado disponibles y las postulaciones aplicando Mínimo Privilegio:
    - VOLUNTARIO: Solo ve sus propias postulaciones y su cupo horario semanal disponible.
    - REPRESENTANTE_OSAL: Ve las postulaciones hechas a las campañas de su fundación.
    - ADMIN / SUPER_ADMIN: Ve todas las postulaciones de la región.
    """
    roles_usuario = set()
    voluntario_id_sesion = None
    fundacion_id_sesion = None

    try:
        verify_jwt_in_request(optional=True)
        claims = get_jwt() or {}
        roles_usuario = set(claims.get("roles") or [])
        voluntario_id_sesion = claims.get("voluntario_id")
        fundacion_id_sesion = claims.get("fundacion_id")
    except Exception:
        pass

    todas_nec = NecesidadCampana.query.order_by(NecesidadCampana.id.desc()).all()
    nec_vol = [n for n in todas_nec if n.tipo_necesidad and n.tipo_necesidad.codigo == "TIEMPO_VOLUNTARIADO"]
    necesidades = nec_vol if nec_vol else todas_nec

    labores = []
    for n in necesidades:
        campana = n.campana
        fundacion = campana.fundacion if campana else None
        municipio = (
            fundacion.direccion.municipio.nombre
            if (fundacion and fundacion.direccion and fundacion.direccion.municipio)
            else "Sabana Norte"
        )
        labores.append({
            "necesidad_id": n.id,
            "descripcion_item": n.descripcion_item,
            "tipo_codigo": n.tipo_necesidad.codigo if n.tipo_necesidad else "TIEMPO_VOLUNTARIADO",
            "horas_requeridas": float(n.cantidad_requerida or 0),
            "horas_cubiertas": float(n.cantidad_cubierta or 0),
            "prioridad": n.prioridad,
            "campana_titulo": campana.titulo if campana else "Campaña Rural",
            "fundacion_nombre": fundacion.razon_social if fundacion else "Fundación Sabana Norte",
            "municipio": municipio,
        })

    # Filtrado estricto de postulaciones por rol (Confidencialidad y Mínimo Privilegio)
    postulaciones_query = PostulacionVoluntariado.query.order_by(PostulacionVoluntariado.fecha_postulacion.desc())
    if "ADMIN" in roles_usuario or "SUPER_ADMIN" in roles_usuario:
        postulaciones = postulaciones_query.all()
    elif "REPRESENTANTE_OSAL" in roles_usuario and fundacion_id_sesion:
        todas_p = postulaciones_query.all()
        postulaciones = [
            p for p in todas_p
            if p.necesidad_campana and p.necesidad_campana.campana and p.necesidad_campana.campana.fundacion_id == int(fundacion_id_sesion)
        ]
    elif voluntario_id_sesion:
        postulaciones = postulaciones_query.filter_by(voluntario_id=int(voluntario_id_sesion)).all()
    else:
        postulaciones = []

    lista_postulaciones = []
    for p in postulaciones:
        vol_nombre = "Voluntario Solidario"
        if p.voluntario and p.voluntario.persona:
            vol_nombre = f"{p.voluntario.persona.nombres} {p.voluntario.persona.apellidos}"

        lista_postulaciones.append({
            "id": p.id,
            "voluntario_id": p.voluntario_id,
            "voluntario_nombre": vol_nombre,
            "necesidad_id": p.necesidad_campana_id,
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
            "motivacion": p.motivacion,
            "disponibilidad_propuesta": p.disponibilidad_propuesta,
            "estado_postulacion": p.estado_postulacion,
            "fecha_postulacion": p.fecha_postulacion.isoformat() if p.fecha_postulacion else None,
            "asignacion": {
                "tarea_especifica": p.asignacion.tarea_especifica,
                "horas_comprometidas": p.asignacion.horas_comprometidas,
                "estado_actividad": p.asignacion.estado_actividad
            } if p.asignacion else None
        })

    # Calcular resumen de disponibilidad del voluntario activo
    resumen_disponibilidad = {
        "disponibilidad_horas_semana": 8,
        "horas_comprometidas": 0,
        "horas_disponibles_restantes": 8
    }
    if voluntario_id_sesion:
        vol_obj = db.session.get(Voluntario, int(voluntario_id_sesion))
        if vol_obj:
            comprometidas = sum(
                (p.asignacion.horas_comprometidas if p.asignacion else 0)
                for p in vol_obj.postulaciones
                if p.estado_postulacion != "RECHAZADO"
            )
            disp_total = int(vol_obj.disponibilidad_horas_semana or 4)
            resumen_disponibilidad = {
                "disponibilidad_horas_semana": disp_total,
                "horas_comprometidas": int(comprometidas),
                "horas_disponibles_restantes": max(0, disp_total - int(comprometidas))
            }

    return jsonify({
        "labores": labores,
        "postulaciones": lista_postulaciones,
        "resumen_disponibilidad": resumen_disponibilidad
    }), 200


@voluntariado_bp.route("/postular", methods=["POST"])
@requiere_roles("VOLUNTARIO", "ADMIN")
def postular_a_labor():
    """
    Exclusivo para VOLUNTARIO o ADMIN (Mínimo Privilegio):
    Registra la postulación validando que las horas comprometidas no superen la disponibilidad semanal registrada.
    """
    data = request.get_json(silent=True) or {}
    identidad = get_jwt_identity()
    claims = get_jwt()
    usuario_id = int(identidad) if identidad else None

    voluntario_id = claims.get("voluntario_id") or data.get("voluntario_id")
    necesidad_id = data.get("necesidad_campana_id")
    motivacion = (data.get("motivacion") or "").strip()
    disponibilidad = (data.get("disponibilidad_propuesta") or "").strip()

    try:
        horas_comprometidas = int(data.get("horas_comprometidas") or 0)
    except (ValueError, TypeError):
        horas_comprometidas = 0

    voluntario = db.session.get(Voluntario, int(voluntario_id)) if voluntario_id else Voluntario.query.first()
    necesidad = db.session.get(NecesidadCampana, int(necesidad_id)) if necesidad_id else NecesidadCampana.query.first()

    if not voluntario or not necesidad or not motivacion or not disponibilidad:
        return jsonify({
            "error": "Datos incompletos",
            "mensaje_humano": "Por favor selecciona la actividad comunitaria, la franja horaria de la lista y escribe tu perfil de apoyo."
        }), 400

    if horas_comprometidas < 1:
        return jsonify({
            "error": "Horas inválidas",
            "mensaje_humano": "Debes comprometer al menos 1 hora para postularte a la actividad."
        }), 400

    existente = PostulacionVoluntariado.query.filter_by(
        voluntario_id=voluntario.id,
        necesidad_campana_id=necesidad.id
    ).first()

    if existente:
        return jsonify({
            "error": "Postulación ya existente",
            "mensaje_humano": "Ya tienes una inscripción activa en esta actividad comunitaria. Puedes elegir otra labor disponible o revisar tus asignaciones vigentes."
        }), 409

    # Validar que las horas comprometidas no superen la disponibilidad semanal registrada por el voluntario
    horas_ya_comprometidas = sum(
        (p.asignacion.horas_comprometidas if p.asignacion else 0)
        for p in voluntario.postulaciones
        if p.estado_postulacion != "RECHAZADO"
    )
    disp_maxima = int(voluntario.disponibilidad_horas_semana or 4)
    horas_restantes = max(0, disp_maxima - int(horas_ya_comprometidas))

    if horas_comprometidas > disp_maxima:
        return jsonify({
            "error": "Supera disponibilidad semanal",
            "mensaje_humano": f"No puedes comprometer {horas_comprometidas} horas porque en tu inscripción registraste una disponibilidad máxima de {disp_maxima} horas por semana."
        }), 400

    if horas_comprometidas > horas_restantes:
        return jsonify({
            "error": "Cupo horario semanal agotado",
            "mensaje_humano": f"Tienes {disp_maxima} horas semanales registradas y ya comprometiste {horas_ya_comprometidas} horas en otras labores. Actualmente puedes comprometer máximo {horas_restantes} hora(s) adicional(es)."
        }), 400

    postulacion = PostulacionVoluntariado(
        voluntario_id=voluntario.id,
        necesidad_campana_id=necesidad.id,
        motivacion=motivacion,
        disponibilidad_propuesta=disponibilidad,
        estado_postulacion="ACEPTADO"
    )
    db.session.add(postulacion)
    db.session.flush()

    asignacion = AsignacionActividad(
        postulacion_id=postulacion.id,
        tarea_especifica=f"Apoyo en terreno: {necesidad.descripcion_item}",
        horas_comprometidas=horas_comprometidas,
        horas_cumplidas=0,
        estado_actividad="ASIGNADA"
    )
    db.session.add(asignacion)

    necesidad.cantidad_cubierta = Decimal(str(necesidad.cantidad_cubierta or 0)) + Decimal(str(horas_comprometidas))

    db.session.add(LogAuditoria(
        usuario_id=usuario_id,
        accion="POSTULACION_VOLUNTARIADO",
        entidad_afectada="postulaciones_voluntariado",
        registro_id=postulacion.id,
        detalle=f"Voluntario #{voluntario.id} postulado a '{necesidad.descripcion_item}' por {horas_comprometidas} horas.",
        direccion_ip=request.remote_addr
    ))

    db.session.commit()

    return jsonify({
        "mensaje_humano": f"¡Postulación confirmada! Quedaste inscrito(a) con {horas_comprometidas} horas para apoyar la actividad «{necesidad.descripcion_item}». La fundación cuenta contigo.",
        "postulacion_id": postulacion.id
    }), 201


@voluntariado_bp.route("/perfil-habilidades", methods=["GET"])
def obtener_perfil_habilidades():
    """
    CU10: Obtiene la información del voluntario autenticado (o solicitado) y su matriz de competencias.
    """
    voluntario_id = request.args.get("voluntario_id")
    if not voluntario_id:
        try:
            verify_jwt_in_request(optional=True)
            claims = get_jwt() or {}
            voluntario_id = claims.get("voluntario_id")
        except Exception:
            pass

    voluntario = db.session.get(Voluntario, int(voluntario_id)) if voluntario_id else Voluntario.query.first()

    if not voluntario:
        return jsonify({"error": "Voluntario no encontrado"}), 404

    nombre_vol = "Voluntario Sabana Norte"
    if voluntario.persona:
        nombre_vol = f"{voluntario.persona.nombres} {voluntario.persona.apellidos}"

    competencias = []
    for ph in voluntario.habilidades_perfil:
        if ph.habilidad:
            competencias.append({
                "id": ph.id,
                "habilidad_id": ph.habilidad.id,
                "habilidad_nombre": ph.habilidad.nombre,
                "categoria_nombre": ph.habilidad.categoria.nombre if ph.habilidad.categoria else "General",
                "nivel_dominio": ph.nivel_dominio,
                "anos_experiencia": ph.anos_experiencia
            })

    return jsonify({
        "voluntario": {
            "id": voluntario.id,
            "nombre_completo": nombre_vol,
            "disponibilidad_horas_semana": voluntario.disponibilidad_horas_semana,
            "biografia_corta": voluntario.biografia_corta,
            "dispuesto_desplazamiento_rural": voluntario.dispuesto_desplazamiento_rural,
            "competencias": competencias
        }
    }), 200


@voluntariado_bp.route("/perfil-habilidades", methods=["POST", "PUT"])
@requiere_roles("VOLUNTARIO", "ADMIN")
def actualizar_perfil_habilidades():
    """
    Exclusivo para VOLUNTARIO o ADMIN (Mínimo Privilegio):
    Permite al voluntario actualizar su disponibilidad rural y competencias en 5FN.
    """
    data = request.get_json(silent=True) or {}
    identidad = get_jwt_identity()
    claims = get_jwt()
    usuario_id = int(identidad) if identidad else None

    voluntario_id = claims.get("voluntario_id") or data.get("voluntario_id")
    voluntario = db.session.get(Voluntario, int(voluntario_id)) if voluntario_id else Voluntario.query.first()

    if not voluntario:
        return jsonify({
            "error": "Voluntario no encontrado",
            "mensaje_humano": "No se encontró el perfil de voluntario activo."
        }), 404

    if "disponibilidad_horas_semana" in data:
        voluntario.disponibilidad_horas_semana = max(1, int(data.get("disponibilidad_horas_semana") or 4))
    if "biografia_corta" in data:
        voluntario.biografia_corta = (data.get("biografia_corta") or "").strip()
    if "dispuesto_desplazamiento_rural" in data:
        voluntario.dispuesto_desplazamiento_rural = bool(data.get("dispuesto_desplazamiento_rural"))

    habilidad_id = data.get("habilidad_id")
    if habilidad_id:
        hab = db.session.get(Habilidad, int(habilidad_id))
        if hab:
            nivel = (data.get("nivel_dominio") or "INTERMEDIO").upper()
            anos = int(data.get("anos_experiencia") or 1)

            relacion = PerfilHabilidadVoluntario.query.filter_by(
                voluntario_id=voluntario.id,
                habilidad_id=hab.id
            ).first()

            if relacion:
                relacion.nivel_dominio = nivel
                relacion.anos_experiencia = anos
            else:
                db.session.add(PerfilHabilidadVoluntario(
                    voluntario_id=voluntario.id,
                    habilidad_id=hab.id,
                    nivel_dominio=nivel,
                    anos_experiencia=anos
                ))

    db.session.add(LogAuditoria(
        usuario_id=usuario_id,
        accion="ACTUALIZAR_PERFIL_HABILIDADES",
        entidad_afectada="perfil_habilidades_voluntario",
        registro_id=voluntario.id,
        detalle=f"Actualizadas competencias y disponibilidad ({voluntario.disponibilidad_horas_semana}h/sem) del voluntario #{voluntario.id}.",
        direccion_ip=request.remote_addr
    ))

    db.session.commit()

    return jsonify({
        "mensaje_humano": "¡Tus habilidades y disponibilidad semanal han quedado actualizadas en tu perfil de voluntario!"
    }), 200


@voluntariado_bp.route("/perfil-habilidades/<int:registro_id>", methods=["DELETE"])
@requiere_roles("VOLUNTARIO", "ADMIN")
def eliminar_habilidad_voluntario(registro_id: int):
    rel = db.session.get(PerfilHabilidadVoluntario, registro_id)
    if not rel:
        return jsonify({"error": "No encontrado"}), 404
    db.session.delete(rel)
    db.session.commit()
    return jsonify({"mensaje_humano": "Habilidad retirada de tu perfil."}), 200
