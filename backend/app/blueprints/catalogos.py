"""
Blueprint de Catálogos Maestros 5FN (Offline-First Cacheable).
Provee municipios de Sabana Norte, tipos de documento, ODS, categorías de causas,
tipos de necesidad, unidades de medida, métodos de pago y habilidades.
"""
from flask import Blueprint, jsonify
from app.models import (
    Municipio, TipoDocumento, OdsObjetivo, CategoriaCausa,
    TipoNecesidad, UnidadMedida, MetodoPago, CategoriaHabilidad, Habilidad
)

catalogos_bp = Blueprint("catalogos", __name__, url_prefix="/api/catalogos")


@catalogos_bp.route("/general", methods=["GET"])
def obtener_catalogos_generales():
    municipios = Municipio.query.filter_by(es_sabana_norte=True).order_by(Municipio.nombre.asc()).all()
    tipos_doc = TipoDocumento.query.order_by(TipoDocumento.id.asc()).all()
    ods = OdsObjetivo.query.order_by(OdsObjetivo.numero_ods.asc()).all()
    categorias_causas = CategoriaCausa.query.order_by(CategoriaCausa.nombre.asc()).all()
    tipos_necesidad = TipoNecesidad.query.order_by(TipoNecesidad.id.asc()).all()
    unidades_medida = UnidadMedida.query.order_by(UnidadMedida.id.asc()).all()
    metodos_pago = MetodoPago.query.order_by(MetodoPago.id.asc()).all()
    categorias_hab = CategoriaHabilidad.query.order_by(CategoriaHabilidad.nombre.asc()).all()
    habilidades = Habilidad.query.order_by(Habilidad.nombre.asc()).all()

    return jsonify({
        "municipios_sabana_norte": [
            {
                "id": m.id,
                "codigo_dane": m.codigo_dane,
                "nombre": m.nombre,
                "latitud_centro": float(m.latitud_centro) if m.latitud_centro is not None else 4.95,
                "longitud_centro": float(m.longitud_centro) if m.longitud_centro is not None else -74.01,
            }
            for m in municipios
        ],
        "tipos_documento": [
            {"id": td.id, "sigla": td.sigla, "nombre": td.nombre}
            for td in tipos_doc
        ],
        "ods_objetivos": [
            {"id": o.id, "numero_ods": o.numero_ods, "titulo": o.titulo, "descripcion": o.descripcion}
            for o in ods
        ],
        "categorias_causas": [
            {"id": c.id, "nombre": c.nombre, "descripcion": c.descripcion}
            for c in categorias_causas
        ],
        "tipos_necesidad": [
            {"id": tn.id, "codigo": tn.codigo, "nombre": tn.nombre}
            for tn in tipos_necesidad
        ],
        "unidades_medida": [
            {"id": um.id, "simbolo": um.simbolo, "nombre": um.nombre}
            for um in unidades_medida
        ],
        "metodos_pago": [
            {"id": mp.id, "codigo": mp.codigo, "nombre": mp.nombre}
            for mp in metodos_pago
        ],
        "categorias_habilidades": [
            {"id": ch.id, "nombre": ch.nombre, "descripcion": ch.descripcion}
            for ch in categorias_hab
        ],
        "habilidades": [
            {"id": h.id, "categoria_id": h.categoria_id, "nombre": h.nombre, "descripcion": h.descripcion}
            for h in habilidades
        ],
    }), 200
