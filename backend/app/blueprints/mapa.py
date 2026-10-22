"""
Blueprint CU06 - Mapa Georreferenciado de la Sabana Norte de Cundinamarca.
Cruza fundaciones_osal, direcciones, municipios y campanas en 5FN para alimentar los pines interactivos de Leaflet.js.
"""
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import FundacionOsal, Direccion, Municipio

mapa_bp = Blueprint("mapa", __name__, url_prefix="/api/mapa")


@mapa_bp.route("/pines", methods=["GET"])
def obtener_pines_sabana_norte():
    """
    CU06: Realiza un JOIN explícito entre fundaciones_osal, direcciones y municipios
    para retornar los pines georreferenciados en la Sabana Norte de Cundinamarca.
    """
    municipio_id = request.args.get("municipio_id")

    query = (
        db.session.query(FundacionOsal, Direccion, Municipio)
        .join(Direccion, FundacionOsal.direccion_id == Direccion.id)
        .join(Municipio, Direccion.municipio_id == Municipio.id)
        .filter(Municipio.es_sabana_norte.is_(True))
    )

    if municipio_id:
        query = query.filter(Municipio.id == int(municipio_id))

    filas = query.all()
    pines = []

    for fundacion, direccion, municipio in filas:
        campanas_activas = [c.titulo for c in fundacion.campanas if c.estado == "ACTIVA"]
        pines.append({
            "fundacion_id": fundacion.id,
            "nit": fundacion.nit,
            "razon_social": fundacion.razon_social,
            "sigla": fundacion.sigla,
            "mision": fundacion.mision,
            "estado_validacion": fundacion.estado_validacion,
            "telefono": fundacion.telefono_institucional,
            "municipio_id": municipio.id,
            "municipio_nombre": municipio.nombre,
            "codigo_dane": municipio.codigo_dane,
            "vereda_o_barrio": direccion.vereda_o_barrio,
            "direccion_fisica": direccion.direccion_fisica,
            "indicaciones_rurales": direccion.indicaciones_rurales,
            "latitud": float(direccion.latitud),
            "longitud": float(direccion.longitud),
            "campanas_activas": campanas_activas,
            "total_campanas": len(campanas_activas),
        })

    return jsonify({
        "region": "Sabana Norte de Cundinamarca",
        "centro_mapa": {"latitud": 4.9650, "longitud": -74.0100, "zoom": 11},
        "total_pines": len(pines),
        "pines": pines
    }), 200
