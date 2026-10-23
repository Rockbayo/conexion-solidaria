"""
Blueprint de Catálogos Maestros y Parametrización del Sistema (5FN).
Provee municipios de Sabana Norte, tipos de documento, ODS, categorías de causas,
tipos de necesidad, unidades de medida, métodos de pago, habilidades, franjas horarias
y parámetros globales. Incluye endpoints exclusivos para SUPER_ADMIN.
"""
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.extensions import db
from app.security import requiere_roles
from app.models import (
    Municipio, TipoDocumento, OdsObjetivo, CategoriaCausa,
    TipoNecesidad, UnidadMedida, MetodoPago, CategoriaHabilidad, Habilidad,
    FranjaHoraria, ParametroSistema, LogAuditoria
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
    franjas = FranjaHoraria.query.filter_by(activa=True).order_by(FranjaHoraria.id.asc()).all()
    parametros = ParametroSistema.query.order_by(ParametroSistema.id.asc()).all()

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
        "franjas_horarias": [
            {"id": fh.id, "codigo": fh.codigo, "nombre": fh.nombre, "horas_sugeridas": fh.horas_sugeridas}
            for fh in franjas
        ],
        "parametros_sistema": [
            {
                "id": p.id,
                "clave": p.clave,
                "valor": p.valor,
                "descripcion": p.descripcion,
                "tipo_dato": p.tipo_dato
            }
            for p in parametros
        ],
    }), 200


@catalogos_bp.route("/unidades-medida", methods=["POST"])
@requiere_roles("SUPER_ADMIN")
def agregar_unidad_medida():
    """Exclusivo para SUPER_ADMIN: Agrega o actualiza una unidad de recolección en la plataforma."""
    data = request.get_json(silent=True) or {}
    simbolo = (data.get("simbolo") or "").strip().upper()
    nombre = (data.get("nombre") or "").strip()

    if not simbolo or not nombre:
        return jsonify({
            "error": "Datos incompletos",
            "mensaje_humano": "Por favor escribe el símbolo (ej. LT, KG, CAJA) y el nombre de la unidad de medida."
        }), 400

    existente = UnidadMedida.query.filter_by(simbolo=simbolo).first()
    if existente:
        existente.nombre = nombre
        msg = f"Se actualizó la unidad de medida '{nombre} ({simbolo})'."
    else:
        nueva = UnidadMedida(simbolo=simbolo, nombre=nombre)
        db.session.add(nueva)
        msg = f"Se agregó la unidad de medida '{nombre} ({simbolo})' al catálogo de la plataforma."

    usuario_id = int(get_jwt_identity())
    db.session.add(LogAuditoria(
        usuario_id=usuario_id,
        accion="PARAMETRIZAR_UNIDAD_MEDIDA",
        entidad_afectada="unidades_medida",
        detalle=f"Unidad de medida configurada: {simbolo} - {nombre}",
        direccion_ip=request.remote_addr
    ))
    db.session.commit()
    return jsonify({"mensaje_humano": msg}), 201


@catalogos_bp.route("/categorias-causas", methods=["POST"])
@requiere_roles("SUPER_ADMIN")
def agregar_categoria_causa():
    """Exclusivo para SUPER_ADMIN: Agrega una nueva línea de intervención o categoría de causa."""
    data = request.get_json(silent=True) or {}
    nombre = (data.get("nombre") or "").strip()
    descripcion = (data.get("descripcion") or "Línea de intervención comunitaria en Sabana Norte").strip()

    if not nombre:
        return jsonify({
            "error": "Datos incompletos",
            "mensaje_humano": "Por favor escribe el nombre de la nueva línea de intervención."
        }), 400

    existente = CategoriaCausa.query.filter_by(nombre=nombre).first()
    if existente:
        existente.descripcion = descripcion
        msg = f"Se actualizó la categoría '{nombre}'."
    else:
        db.session.add(CategoriaCausa(nombre=nombre, descripcion=descripcion))
        msg = f"Se agregó la categoría '{nombre}' al catálogo de causas."

    usuario_id = int(get_jwt_identity())
    db.session.add(LogAuditoria(
        usuario_id=usuario_id,
        accion="PARAMETRIZAR_CATEGORIA_CAUSA",
        entidad_afectada="categorias_causas",
        detalle=f"Categoría de causa configurada: {nombre}",
        direccion_ip=request.remote_addr
    ))
    db.session.commit()
    return jsonify({"mensaje_humano": msg}), 201


@catalogos_bp.route("/habilidades", methods=["POST"])
@requiere_roles("SUPER_ADMIN")
def agregar_habilidad_catalogo():
    """Exclusivo para SUPER_ADMIN: Agrega una nueva competencia al catálogo de voluntariado."""
    data = request.get_json(silent=True) or {}
    categoria_id = int(data.get("categoria_id") or 1)
    nombre = (data.get("nombre") or "").strip()
    descripcion = (data.get("descripcion") or "Competencia comunitaria certificada").strip()

    if not nombre:
        return jsonify({
            "error": "Datos incompletos",
            "mensaje_humano": "Por favor escribe el nombre de la habilidad o competencia."
        }), 400

    cat = db.session.get(CategoriaHabilidad, categoria_id) or CategoriaHabilidad.query.first()
    db.session.add(Habilidad(categoria_id=cat.id, nombre=nombre, descripcion=descripcion))

    usuario_id = int(get_jwt_identity())
    db.session.add(LogAuditoria(
        usuario_id=usuario_id,
        accion="PARAMETRIZAR_HABILIDAD",
        entidad_afectada="habilidades",
        detalle=f"Nueva habilidad agregada al catálogo: {nombre}",
        direccion_ip=request.remote_addr
    ))
    db.session.commit()
    return jsonify({"mensaje_humano": f"Se agregó la competencia '{nombre}' al catálogo de voluntariado."}), 201


@catalogos_bp.route("/franjas-horarias", methods=["POST"])
@requiere_roles("SUPER_ADMIN")
def agregar_franja_horaria():
    """Exclusivo para SUPER_ADMIN: Agrega una nueva franja horaria para voluntariado."""
    data = request.get_json(silent=True) or {}
    nombre = (data.get("nombre") or "").strip()
    horas_sugeridas = int(data.get("horas_sugeridas") or 4)

    if not nombre:
        return jsonify({
            "error": "Datos incompletos",
            "mensaje_humano": "Por favor escribe la descripción de la franja horaria."
        }), 400

    codigo = nombre.upper().replace(" ", "_")[:35]
    existente = FranjaHoraria.query.filter_by(codigo=codigo).first()
    if existente:
        existente.nombre = nombre
        existente.horas_sugeridas = horas_sugeridas
    else:
        db.session.add(FranjaHoraria(codigo=codigo, nombre=nombre, horas_sugeridas=horas_sugeridas, activa=True))

    usuario_id = int(get_jwt_identity())
    db.session.add(LogAuditoria(
        usuario_id=usuario_id,
        accion="PARAMETRIZAR_FRANJA_HORARIA",
        entidad_afectada="franjas_horarias",
        detalle=f"Franja horaria configurada: {nombre} ({horas_sugeridas}h)",
        direccion_ip=request.remote_addr
    ))
    db.session.commit()
    return jsonify({"mensaje_humano": f"Franja horaria '{nombre}' agregada exitosamente."}), 201


@catalogos_bp.route("/parametros", methods=["PUT"])
@requiere_roles("SUPER_ADMIN")
def actualizar_parametro_sistema():
    """Exclusivo para SUPER_ADMIN: Actualiza un parámetro global del sistema."""
    data = request.get_json(silent=True) or {}
    clave = (data.get("clave") or "").strip().upper()
    valor = str(data.get("valor") or "").strip()

    if not clave or not valor:
        return jsonify({
            "error": "Datos incompletos",
            "mensaje_humano": "Debes indicar el parámetro y su nuevo valor."
        }), 400

    param = ParametroSistema.query.filter_by(clave=clave).first()
    if not param:
        return jsonify({
            "error": "Parámetro no encontrado",
            "mensaje_humano": f"No se encontró el parámetro {clave}."
        }), 404

    param.valor = valor
    param.fecha_actualizacion = datetime.now(timezone.utc)

    usuario_id = int(get_jwt_identity())
    db.session.add(LogAuditoria(
        usuario_id=usuario_id,
        accion="ACTUALIZAR_PARAMETRO_SISTEMA",
        entidad_afectada="parametros_sistema",
        registro_id=param.id,
        detalle=f"Parámetro '{clave}' actualizado a '{valor}'.",
        direccion_ip=request.remote_addr
    ))
    db.session.commit()
    return jsonify({
        "mensaje_humano": f"El parámetro '{clave}' se actualizó correctamente a '{valor}'."
    }), 200
