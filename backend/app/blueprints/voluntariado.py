"""
Blueprint de Voluntariado y Asignaciones (5FN):
- CU05: Postulación Voluntariado (postulaciones_voluntariado, asignaciones_actividades, necesidades_campana)
- CU10: Perfil de Habilidades (voluntarios, categorias_habilidades, habilidades, perfil_habilidades_voluntario)
"""
from decimal import Decimal
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import (
    Voluntario, Habilidad, PerfilHabilidadVoluntario,
    NecesidadCampana, PostulacionVoluntariado, AsignacionActividad, LogAuditoria
)

voluntariado_bp = Blueprint("voluntariado", __name__, url_prefix="/api/voluntariado")


@voluntariado_bp.route("/labores", methods=["GET"])
def listar_labores_voluntariado():
    """
    Lista las necesidades de campañas de tipo TIEMPO_VOLUNTARIADO (o generales) y las
    postulaciones/asignaciones registradas en la Sabana Norte.
    """
    necesidades = NecesidadCampana.query.order_by(NecesidadCampana.id.desc()).all()
    postulaciones = PostulacionVoluntariado.query.order_by(PostulacionVoluntariado.fecha_postulacion.desc()).all()

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

    lista_postulaciones = []
    for p in postulaciones:
        vol_nombre = "Voluntario Solidario"
        if p.voluntario and p.voluntario.persona:
            vol_nombre = f"{p.voluntario.persona.nombres} {p.voluntario.persona.apellidos}"

        lista_postulaciones.append({
            "id": p.id,
            "voluntario_nombre": vol_nombre,
            "labor_descripcion": p.necesidad_campana.descripcion_item if p.necesidad_campana else "Labor rural",
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

    return jsonify({
        "labores": labores,
        "postulaciones": lista_postulaciones
    }), 200


@voluntariado_bp.route("/postular", methods=["POST"])
@jwt_required(optional=True)
def postular_a_labor():
    """
    CU05: Registra la postulación de un voluntario a una labor específica (necesidad_campana_id),
    genera la asignación inicial en asignaciones_actividades y actualiza las horas comprometidas.
    """
    data = request.get_json(silent=True) or {}
    identidad = get_jwt_identity()
    usuario_id = int(identidad) if identidad else None

    voluntario_id = data.get("voluntario_id")
    necesidad_id = data.get("necesidad_campana_id")
    motivacion = (data.get("motivacion") or "").strip()
    disponibilidad = (data.get("disponibilidad_propuesta") or "Fines de semana en la mañana").strip()
    horas_comprometidas = int(data.get("horas_comprometidas") or 6)

    voluntario = db.session.get(Voluntario, int(voluntario_id)) if voluntario_id else Voluntario.query.first()
    necesidad = db.session.get(NecesidadCampana, int(necesidad_id)) if necesidad_id else NecesidadCampana.query.first()

    if not voluntario or not necesidad or not motivacion:
        return jsonify({
            "error": "Datos incompletos",
            "mensaje_humano": "Por favor selecciona la labor comunitaria y cuéntanos brevemente tu motivación para participar."
        }), 400

    existente = PostulacionVoluntariado.query.filter_by(
        voluntario_id=voluntario.id,
        necesidad_campana_id=necesidad.id
    ).first()

    if existente:
        return jsonify({
            "error": "Postulación ya existente",
            "mensaje_humano": "Ya te habías postulado anteriormente a esta labor comunitaria. ¡Gracias por tu compromiso!"
        }), 409

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
        detalle=f"Voluntario #{voluntario.id} postulado a necesidad #{necesidad.id} por {horas_comprometidas} horas.",
        direccion_ip=request.remote_addr
    ))

    db.session.commit()

    return jsonify({
        "mensaje_humano": f"¡Postulación exitosa! Te hemos asignado {horas_comprometidas} horas en la labor '{necesidad.descripcion_item}'.",
        "postulacion_id": postulacion.id
    }), 201


@voluntariado_bp.route("/perfil-habilidades", methods=["GET"])
def obtener_perfil_habilidades():
    """
    CU10: Obtiene la información del voluntario y su matriz de competencias normalizada
    en perfil_habilidades_voluntario -> habilidades -> categorias_habilidades.
    """
    voluntario_id = request.args.get("voluntario_id")
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
@jwt_required(optional=True)
def actualizar_perfil_habilidades():
    """
    CU10: Permite al voluntario actualizar su disponibilidad rural, agregar una nueva
    competencia (o actualizar su nivel de dominio y años de experiencia en 5FN).
    """
    data = request.get_json(silent=True) or {}
    identidad = get_jwt_identity()
    usuario_id = int(identidad) if identidad else None

    voluntario_id = data.get("voluntario_id")
    voluntario = db.session.get(Voluntario, int(voluntario_id)) if voluntario_id else Voluntario.query.first()

    if not voluntario:
        return jsonify({
            "error": "Voluntario no encontrado",
            "mensaje_humano": "No se encontró el perfil de voluntario activo."
        }), 404

    if "disponibilidad_horas_semana" in data:
        voluntario.disponibilidad_horas_semana = int(data.get("disponibilidad_horas_semana") or 4)
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
        detalle=f"Actualizadas competencias y disponibilidad del voluntario #{voluntario.id}.",
        direccion_ip=request.remote_addr
    ))

    db.session.commit()

    return jsonify({
        "mensaje_humano": "¡Tus habilidades y disponibilidad rural han quedado actualizadas en tu perfil solidario!"
    }), 200


@voluntariado_bp.route("/perfil-habilidades/<int:registro_id>", methods=["DELETE"])
def eliminar_habilidad_voluntario(registro_id: int):
    rel = db.session.get(PerfilHabilidadVoluntario, registro_id)
    if not rel:
        return jsonify({"error": "No encontrado"}), 404
    db.session.delete(rel)
    db.session.commit()
    return jsonify({"mensaje_humano": "Habilidad retirada de tu perfil."}), 200
