"""
Blueprint CU08 - Dashboard OSAL (Métricas Operativas en Quinta Forma Normal).
Consolida recaudo económico, donaciones en especie, voluntarios postulados/asignados y campañas.
"""
from sqlalchemy import func
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import (
    FundacionOsal, Campana, NecesidadCampana, AporteTransaccional,
    DonacionEconomica, DonacionEspecie, Voluntario, PostulacionVoluntariado, AsignacionActividad
)

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard_bp.route("/osal", methods=["GET"])
def obtener_metricas_osal():
    """
    CU08: Retorna los indicadores clave de desempeño (KPIs) para las fundaciones OSAL
    de la Sabana Norte: recaudo total, avance frente a la meta, voluntarios comprometidos,
    horas de voluntariado, estado logístico de especie y resumen por campaña.
    """
    fundacion_id = request.args.get("fundacion_id")

    total_recaudo = db.session.query(func.coalesce(func.sum(DonacionEconomica.monto), 0)).scalar() or 0
    meta_global = db.session.query(func.coalesce(func.sum(Campana.meta_economica), 0)).scalar() or 0
    recaudo_campanas = db.session.query(func.coalesce(func.sum(Campana.monto_recaudado), 0)).scalar() or 0
    recaudo_consolidado = max(float(total_recaudo), float(recaudo_campanas))

    total_campanas_activas = Campana.query.filter_by(estado="ACTIVA").count()
    total_fundaciones = FundacionOsal.query.count()
    total_voluntarios = Voluntario.query.filter_by(activo=True).count()
    total_postulaciones = PostulacionVoluntariado.query.count()
    horas_comprometidas = db.session.query(func.coalesce(func.sum(AsignacionActividad.horas_comprometidas), 0)).scalar() or 0
    total_aportes_especie = DonacionEspecie.query.count()

    # Desglose de campañas
    campanas_query = Campana.query
    if fundacion_id:
        campanas_query = campanas_query.filter_by(fundacion_id=int(fundacion_id))
    campanas = campanas_query.order_by(Campana.id.desc()).all()

    resumen_campanas = []
    for c in campanas:
        meta = float(c.meta_economica or 0)
        rec = float(c.monto_recaudado or 0)
        porcentaje = round((rec / meta) * 100, 1) if meta > 0 else 0.0
        resumen_campanas.append({
            "id": c.id,
            "titulo": c.titulo,
            "fundacion": c.fundacion.razon_social if c.fundacion else "OSAL Sabana Norte",
            "municipio": (
                c.fundacion.direccion.municipio.nombre
                if (c.fundacion and c.fundacion.direccion and c.fundacion.direccion.municipio)
                else "Sabana Norte"
            ),
            "meta_economica": meta,
            "monto_recaudado": rec,
            "porcentaje_avance": min(100.0, porcentaje),
            "total_necesidades": len(c.necesidades),
            "estado": c.estado
        })

    # Distribución logística de especie
    recibidos = DonacionEspecie.query.filter_by(estado_logistico_actual="RECIBIDO").count()
    en_bodega = DonacionEspecie.query.filter_by(estado_logistico_actual="EN_BODEGA").count()
    entregados = DonacionEspecie.query.filter_by(estado_logistico_actual="ENTREGADO").count()

    return jsonify({
        "kpis": {
            "recaudo_total_cop": recaudo_consolidado,
            "meta_global_cop": float(meta_global),
            "porcentaje_global": round((recaudo_consolidado / float(meta_global)) * 100, 1) if float(meta_global) > 0 else 0.0,
            "campanas_activas": total_campanas_activas,
            "fundaciones_registradas": total_fundaciones,
            "voluntarios_activos": total_voluntarios,
            "postulaciones_voluntariado": total_postulaciones,
            "horas_voluntariado_comprometidas": int(horas_comprometidas),
            "donaciones_especie_totales": total_aportes_especie
        },
        "logistica_especie": {
            "recibido": recibidos,
            "en_bodega": en_bodega,
            "entregado": entregados
        },
        "campanas_desempeno": resumen_campanas
    }), 200

