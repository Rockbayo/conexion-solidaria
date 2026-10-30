"""
Blueprint CU08 - Dashboard OSAL (Métricas Operativas en Quinta Forma Normal).
Consolida recaudo económico, donaciones en especie, voluntarios postulados/asignados y campañas.
Aplica alcance por rol: REPRESENTANTE_OSAL visualiza los indicadores y voluntarios de su fundación;
ADMIN y SUPER_ADMIN visualizan el consolidado regional.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.models import (
    FundacionOsal, Campana, DonacionEconomica, DonacionEspecie,
    Voluntario, PostulacionVoluntariado
)

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard_bp.route("/osal", methods=["GET"])
def obtener_metricas_osal():
    """
    CU08: Retorna los indicadores clave de desempeño (KPIs) para las fundaciones OSAL
    junto con el listado de voluntarios postulados a sus campañas.
    """
    fundacion_id = request.args.get("fundacion_id")
    roles_usuario = set()
    try:
        verify_jwt_in_request(optional=True)
        claims = get_jwt() or {}
        roles_usuario = set(claims.get("roles") or [])
        if not fundacion_id and "REPRESENTANTE_OSAL" in roles_usuario and "ADMIN" not in roles_usuario and "SUPER_ADMIN" not in roles_usuario:
            fundacion_id = claims.get("fundacion_id")
    except Exception:
        pass

    campanas_query = Campana.query
    if fundacion_id:
        campanas_query = campanas_query.filter_by(fundacion_id=int(fundacion_id))
    campanas = campanas_query.order_by(Campana.id.desc()).all()
    ids_campanas = {c.id for c in campanas}

    meta_global = sum(float(c.meta_economica or 0) for c in campanas)
    recaudo_campanas = sum(float(c.monto_recaudado or 0) for c in campanas)

    todas_eco = DonacionEconomica.query.all()
    recaudo_eco = sum(
        float(de.monto or 0)
        for de in todas_eco
        if de.aporte and de.aporte.campana_id in ids_campanas
    )
    recaudo_consolidado = max(recaudo_eco, recaudo_campanas)

    total_campanas_activas = sum(1 for c in campanas if c.estado == "ACTIVA")
    total_fundaciones = 1 if fundacion_id else FundacionOsal.query.count()

    todas_post = PostulacionVoluntariado.query.order_by(PostulacionVoluntariado.fecha_postulacion.desc()).all()
    post_filtradas = [
        p for p in todas_post
        if p.necesidad_campana and p.necesidad_campana.campana_id in ids_campanas
    ]
    horas_comprometidas = sum(
        (p.asignacion.horas_comprometidas if p.asignacion else 0)
        for p in post_filtradas
    )
    voluntarios_unicos = {p.voluntario_id for p in post_filtradas if p.voluntario_id}
    total_voluntarios = len(voluntarios_unicos) if fundacion_id else Voluntario.query.filter_by(activo=True).count()

    todas_esp = DonacionEspecie.query.all()
    esp_filtradas = [
        de for de in todas_esp
        if de.aporte and de.aporte.campana_id in ids_campanas
    ]

    recibidos = sum(1 for de in esp_filtradas if de.estado_logistico_actual == "RECIBIDO")
    en_bodega = sum(1 for de in esp_filtradas if de.estado_logistico_actual == "EN_BODEGA")
    entregados = sum(1 for de in esp_filtradas if de.estado_logistico_actual == "ENTREGADO")

    resumen_campanas = []
    ods_agrupado = {}
    total_necesidades_req = 0.0
    total_necesidades_cub = 0.0

    for c in campanas:
        meta = float(c.meta_economica or 0)
        rec = float(c.monto_recaudado or 0)
        porcentaje = round((rec / meta) * 100, 1) if meta > 0 else 0.0
        for nec in c.necesidades:
            req_n = float(nec.cantidad_requerida or 0)
            cub_n = float(nec.cantidad_cubierta or 0)
            if req_n > 0:
                total_necesidades_req += 1.0
                total_necesidades_cub += min(1.0, cub_n / req_n)

        if c.ods:
            clave_ods = c.ods.numero_ods
            if clave_ods not in ods_agrupado:
                ods_agrupado[clave_ods] = {
                    "numero_ods": c.ods.numero_ods,
                    "titulo_ods": c.ods.titulo,
                    "campanas_asociadas": 0,
                    "recaudo_cop": 0.0,
                    "meta_cop": 0.0
                }
            ods_agrupado[clave_ods]["campanas_asociadas"] += 1
            ods_agrupado[clave_ods]["recaudo_cop"] += rec
            ods_agrupado[clave_ods]["meta_cop"] += meta

        resumen_campanas.append({
            "id": c.id,
            "titulo": c.titulo,
            "fundacion": c.fundacion.razon_social if c.fundacion else "OSAL Sabana Norte",
            "municipio": (
                c.fundacion.direccion.municipio.nombre
                if (c.fundacion and c.fundacion.direccion and c.fundacion.direccion.municipio)
                else "Sabana Norte"
            ),
            "ods": f"ODS {c.ods.numero_ods}: {c.ods.titulo}" if c.ods else "ODS Territorial",
            "meta_economica": meta,
            "monto_recaudado": rec,
            "porcentaje_avance": min(100.0, porcentaje),
            "total_necesidades": len(c.necesidades),
            "estado": c.estado
        })

    impacto_por_ods = []
    for k in sorted(ods_agrupado.keys()):
        item_ods = ods_agrupado[k]
        m_ods = item_ods["meta_cop"]
        r_ods = item_ods["recaudo_cop"]
        item_ods["porcentaje_avance"] = round((r_ods / m_ods) * 100, 1) if m_ods > 0 else 0.0
        impacto_por_ods.append(item_ods)

    tasa_cobertura_nec = round((total_necesidades_cub / total_necesidades_req) * 100, 1) if total_necesidades_req > 0 else 0.0

    voluntarios_postulados = []
    for p in post_filtradas:
        vol_nombre = "Voluntario Comunitario"
        vol_tel = "Sin registro"
        vol_correo = ""
        habilidades_txt = []
        if p.voluntario:
            if p.voluntario.persona:
                vol_nombre = f"{p.voluntario.persona.nombres} {p.voluntario.persona.apellidos}"
                vol_tel = p.voluntario.persona.telefono_contacto or "Sin registro"
                if p.voluntario.persona.usuario:
                    vol_correo = p.voluntario.persona.usuario.correo_electronico
            for ph in p.voluntario.habilidades_perfil:
                if ph.habilidad:
                    habilidades_txt.append(f"{ph.habilidad.nombre} ({ph.nivel_dominio})")

        voluntarios_postulados.append({
            "postulacion_id": p.id,
            "voluntario_nombre": vol_nombre,
            "telefono": vol_tel,
            "correo": vol_correo,
            "habilidades": habilidades_txt,
            "labor_descripcion": p.necesidad_campana.descripcion_item if p.necesidad_campana else "Labor comunitaria",
            "campana_titulo": (
                p.necesidad_campana.campana.titulo
                if (p.necesidad_campana and p.necesidad_campana.campana)
                else "Campaña Sabana Norte"
            ),
            "disponibilidad_propuesta": p.disponibilidad_propuesta,
            "horas_comprometidas": p.asignacion.horas_comprometidas if p.asignacion else 0,
            "estado_postulacion": p.estado_postulacion,
        })

    return jsonify({
        "kpis": {
            "recaudo_total_cop": recaudo_consolidado,
            "meta_global_cop": float(meta_global),
            "porcentaje_global": round((recaudo_consolidado / float(meta_global)) * 100, 1) if float(meta_global) > 0 else 0.0,
            "campanas_activas": total_campanas_activas,
            "fundaciones_registradas": total_fundaciones,
            "voluntarios_activos": total_voluntarios,
            "postulaciones_voluntariado": len(post_filtradas),
            "horas_voluntariado_comprometidas": int(horas_comprometidas),
            "donaciones_especie_totales": len(esp_filtradas),
            "tasa_cobertura_necesidades_pct": tasa_cobertura_nec
        },
        "logistica_especie": {
            "recibido": recibidos,
            "en_bodega": en_bodega,
            "entregado": entregados
        },
        "impacto_por_ods": impacto_por_ods,
        "campanas_desempeno": resumen_campanas,
        "voluntarios_postulados": voluntarios_postulados
    }), 200
