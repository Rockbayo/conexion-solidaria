"""
Blueprint CU03 - Publicar Necesidad y Catálogo de Causas (5FN).
Cruza fundaciones_osal, categorias_causas, ods_objetivos, campanas, tipos_necesidad y necesidades_campana.
"""
from datetime import datetime, date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import (
    Campana, NecesidadCampana, TipoNecesidad, FundacionOsal,
    CategoriaCausa, OdsObjetivo, LogAuditoria
)

campanas_bp = Blueprint("campanas", __name__, url_prefix="/api/campanas")


@campanas_bp.route("", methods=["GET"])
def listar_campanas():
    """
    Retorna todas las campañas solidarias activas en la Sabana Norte junto con su fundación,
    municipio, ODS, categoría de causa y desglose de necesidades (económica, especie o tiempo).
    """
    campanas = Campana.query.order_by(Campana.id.desc()).all()
    resultado = []

    for c in campanas:
        municipio_nombre = "Sabana Norte"
        vereda = ""
        if c.fundacion and c.fundacion.direccion:
            vereda = c.fundacion.direccion.vereda_o_barrio
            if c.fundacion.direccion.municipio:
                municipio_nombre = c.fundacion.direccion.municipio.nombre

        resultado.append({
            "id": c.id,
            "titulo": c.titulo,
            "descripcion": c.descripcion,
            "meta_economica": float(c.meta_economica or 0),
            "monto_recaudado": float(c.monto_recaudado or 0),
            "fecha_inicio": c.fecha_inicio.isoformat() if c.fecha_inicio else None,
            "fecha_fin": c.fecha_fin.isoformat() if c.fecha_fin else None,
            "estado": c.estado,
            "fundacion": {
                "id": c.fundacion.id if c.fundacion else None,
                "razon_social": c.fundacion.razon_social if c.fundacion else "Fundación Rural",
                "municipio": municipio_nombre,
                "vereda": vereda,
            },
            "categoria_causa": c.categoria_causa.nombre if c.categoria_causa else "General",
            "ods": {
                "numero": c.ods.numero_ods if c.ods else 2,
                "titulo": c.ods.titulo if c.ods else "Hambre Cero"
            },
            "necesidades": [
                {
                    "id": n.id,
                    "tipo_codigo": n.tipo_necesidad.codigo if n.tipo_necesidad else "ESPECIE",
                    "tipo_nombre": n.tipo_necesidad.nombre if n.tipo_necesidad else "Donación en Especie",
                    "descripcion_item": n.descripcion_item,
                    "cantidad_requerida": float(n.cantidad_requerida or 0),
                    "cantidad_cubierta": float(n.cantidad_cubierta or 0),
                    "prioridad": n.prioridad,
                }
                for n in c.necesidades
            ]
        })

    return jsonify({"campanas": resultado}), 200


@campanas_bp.route("", methods=["POST"])
@jwt_required(optional=True)
def crear_campana():
    """
    CU03: Permite a una OSAL crear una campaña solidaria y publicar sus necesidades
    específicas (apoyo económico, donación en especie o tiempo de voluntariado).
    """
    data = request.get_json(silent=True) or {}
    identidad = get_jwt_identity()
    usuario_id = int(identidad) if identidad else None

    fundacion_id = data.get("fundacion_id")
    if not fundacion_id:
        primera_fundacion = FundacionOsal.query.first()
        fundacion_id = primera_fundacion.id if primera_fundacion else None

    categoria_causa_id = data.get("categoria_causa_id") or 1
    ods_id = data.get("ods_id") or 1
    titulo = (data.get("titulo") or "").strip()
    descripcion = (data.get("descripcion") or "").strip()
    meta_economica = float(data.get("meta_economica") or 0)
    fecha_inicio_str = data.get("fecha_inicio")
    fecha_fin_str = data.get("fecha_fin")
    necesidades_input = data.get("necesidades") or []

    if not titulo or not descripcion or not fundacion_id:
        return jsonify({
            "error": "Datos incompletos",
            "mensaje_humano": "Por favor escribe el título y la descripción de la necesidad comunitaria que deseas publicar."
        }), 400

    try:
        f_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date() if fecha_inicio_str else date.today()
        f_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date() if fecha_fin_str else date(date.today().year, 12, 31)
    except ValueError:
        f_inicio = date.today()
        f_fin = date(date.today().year, 12, 31)

    cat = db.session.get(CategoriaCausa, int(categoria_causa_id)) or CategoriaCausa.query.first()
    ods = db.session.get(OdsObjetivo, int(ods_id)) or OdsObjetivo.query.first()

    nueva_campana = Campana(
        fundacion_id=int(fundacion_id),
        categoria_causa_id=cat.id,
        ods_id=ods.id,
        titulo=titulo,
        descripcion=descripcion,
        meta_economica=meta_economica,
        monto_recaudado=0,
        fecha_inicio=f_inicio,
        fecha_fin=f_fin,
        estado="ACTIVA"
    )
    db.session.add(nueva_campana)
    db.session.flush()

    necesidades_creadas = []
    for item in necesidades_input:
        tipo_id = item.get("tipo_necesidad_id")
        tipo_cod = item.get("tipo_codigo")
        tn = None
        if tipo_id:
            tn = db.session.get(TipoNecesidad, int(tipo_id))
        elif tipo_cod:
            tn = TipoNecesidad.query.filter_by(codigo=tipo_cod).first()
        if not tn:
            tn = TipoNecesidad.query.first()

        desc_item = (item.get("descripcion_item") or "").strip()
        if desc_item and tn:
            nec = NecesidadCampana(
                campana_id=nueva_campana.id,
                tipo_necesidad_id=tn.id,
                descripcion_item=desc_item,
                cantidad_requerida=float(item.get("cantidad_requerida") or 1),
                cantidad_cubierta=0,
                prioridad=(item.get("prioridad") or "ALTA").upper()
            )
            db.session.add(nec)
            necesidades_creadas.append(desc_item)

    db.session.add(LogAuditoria(
        usuario_id=usuario_id,
        accion="PUBLICAR_CAMPAÑA_Y_NECESIDADES",
        entidad_afectada="campanas",
        registro_id=nueva_campana.id,
        detalle=f"Publicada campaña '{titulo}' con {len(necesidades_creadas)} necesidades asociadas.",
        direccion_ip=request.remote_addr
    ))

    db.session.commit()

    return jsonify({
        "mensaje_humano": f"¡Excelente! La campaña '{titulo}' ya está visible para los donantes y voluntarios de la Sabana Norte.",
        "campana_id": nueva_campana.id
    }), 201
