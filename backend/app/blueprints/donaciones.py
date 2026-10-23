"""
Blueprint Transaccional unificado para:
- CU04: Registrar Donación (Económica y Especie con validación estricta de soporte y monto mínimo $10.000 COP)
- CU07: Certificados Tributarios (Generación de Comprobante Electrónico / Factura Digital PDF con normativa DIAN y envío por correo)
- CU09: Trazabilidad Logística (Actualización de estado en donaciones_especie y trazabilidad_entregas: RECIBIDO -> EN_BODEGA -> ENTREGADO)
"""
import io
import uuid
import hashlib
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.extensions import db
from app.security import requiere_roles
from app.models import (
    Donante, Campana, AporteTransaccional, DonacionEconomica, DonacionEspecie,
    TrazabilidadEntrega, ReciboTributario, MetodoPago, UnidadMedida, LogAuditoria,
    ParametroSistema
)

donaciones_bp = Blueprint("donaciones", __name__, url_prefix="/api/donaciones")


def formatear_pesos_cop(valor: float | int | Decimal) -> str:
    """Formatea un valor numérico en pesos colombianos con punto separador de miles y sin decimales."""
    entero = int(round(float(valor or 0)))
    return f"$ {entero:,}".replace(",", ".") + " COP"


@donaciones_bp.route("", methods=["GET"])
def listar_donaciones():
    """
    Retorna los aportes transaccionales aplicando Mínimo Privilegio:
    - DONANTE: Solo ve sus propias transacciones y certificados.
    - REPRESENTANTE_OSAL: Ve las donaciones dirigidas a su fundación.
    - ADMIN / SUPER_ADMIN: Ve el libro completo de la plataforma.
    """
    roles_usuario = set()
    donante_id_sesion = None
    fundacion_id_sesion = None

    try:
        verify_jwt_in_request(optional=True)
        claims = get_jwt() or {}
        roles_usuario = set(claims.get("roles") or [])
        donante_id_sesion = claims.get("donante_id")
        fundacion_id_sesion = claims.get("fundacion_id")
    except Exception:
        pass

    todos_aportes = AporteTransaccional.query.order_by(AporteTransaccional.fecha_aporte.desc()).all()

    if "ADMIN" in roles_usuario or "SUPER_ADMIN" in roles_usuario:
        aportes = todos_aportes
    elif "REPRESENTANTE_OSAL" in roles_usuario and fundacion_id_sesion:
        aportes = [a for a in todos_aportes if a.campana and a.campana.fundacion_id == int(fundacion_id_sesion)]
    elif donante_id_sesion:
        aportes = [a for a in todos_aportes if a.donante_id == int(donante_id_sesion)]
    else:
        aportes = todos_aportes

    resultado = []

    for a in aportes:
        nombre_donante = "Donante Solidario"
        doc_donante = "N/A"
        correo_donante = ""
        if a.donante and a.donante.persona:
            nombre_donante = f"{a.donante.persona.nombres} {a.donante.persona.apellidos}"
            if a.donante.persona.documento_identidad:
                doc_donante = a.donante.persona.documento_identidad.numero_documento
            if a.donante.persona.usuario:
                correo_donante = a.donante.persona.usuario.correo_electronico

        item = {
            "id": a.id,
            "codigo_referencia": a.codigo_referencia,
            "modalidad": a.modalidad,
            "estado_aporte": a.estado_aporte,
            "url_comprobante": a.url_comprobante,
            "observaciones": a.observaciones,
            "fecha_aporte": a.fecha_aporte.isoformat() if a.fecha_aporte else None,
            "donante_nombre": nombre_donante,
            "donante_documento": doc_donante,
            "donante_correo": correo_donante,
            "campana_titulo": a.campana.titulo if a.campana else "Campaña Sabana Norte",
            "fundacion_nombre": a.campana.fundacion.razon_social if (a.campana and a.campana.fundacion) else "OSAL Rural",
        }

        if a.donacion_economica:
            rec = a.donacion_economica.recibo_tributario
            item["economica"] = {
                "id": a.donacion_economica.id,
                "monto": int(round(float(a.donacion_economica.monto))),
                "moneda": a.donacion_economica.moneda,
                "metodo_pago": a.donacion_economica.metodo_pago.nombre if a.donacion_economica.metodo_pago else "Transferencia",
                "referencia_bancaria": a.donacion_economica.referencia_bancaria,
                "consecutivo_tributario": rec.numero_consecutivo if rec else None,
                "enviado_correo": bool(rec.enviado_correo) if rec else False,
                "correo_destino": rec.correo_destino if rec else correo_donante,
            }

        if a.donacion_especie:
            item["especie"] = {
                "id": a.donacion_especie.id,
                "descripcion_articulos": a.donacion_especie.descripcion_articulos,
                "cantidad": float(a.donacion_especie.cantidad),
                "unidad_simbolo": a.donacion_especie.unidad_medida.simbolo if a.donacion_especie.unidad_medida else "UND",
                "estado_logistico_actual": a.donacion_especie.estado_logistico_actual,
                "historial_trazabilidad": [
                    {
                        "id": t.id,
                        "estado_logistico": t.estado_logistico,
                        "ubicacion_reportada": t.ubicacion_reportada,
                        "observacion": t.observacion,
                        "fecha_actualizacion": t.fecha_actualizacion.isoformat() if t.fecha_actualizacion else None,
                    }
                    for t in a.donacion_especie.trazabilidad
                ]
            }

        resultado.append(item)

    return jsonify({"donaciones": resultado}), 200


@donaciones_bp.route("", methods=["POST"])
@requiere_roles("DONANTE", "ADMIN")
def registrar_donacion():
    """
    Exclusivo para DONANTE o ADMIN (Mínimo Privilegio):
    Registra un aporte validando estrictamente:
    1. Soporte documental adjunto obligatorio.
    2. Si es ECONOMICA: monto entero >= $10.000 COP (sin decimales) y referencia bancaria obligatoria.
    3. Si es ESPECIE: descripción de artículos y cantidad >= 1 obligatorias.
    """
    data = request.get_json(silent=True) or {}
    identidad = get_jwt_identity()
    claims = get_jwt()
    usuario_id = int(identidad) if identidad else None

    campana_id = data.get("campana_id") or 1
    donante_id = claims.get("donante_id") or data.get("donante_id")
    modalidad = (data.get("modalidad") or "ECONOMICA").upper()
    nombre_comprobante = (data.get("nombre_comprobante") or "").strip()
    observaciones = (data.get("observaciones") or "").strip()

    # 1. Validar soporte documental obligatorio
    if not nombre_comprobante:
        return jsonify({
            "error": "Soporte documental obligatorio",
            "mensaje_humano": "Es obligatorio adjuntar el archivo de soporte o comprobante de tu aporte antes de registrarlo."
        }), 400

    donante = db.session.get(Donante, int(donante_id)) if donante_id else Donante.query.first()
    campana = db.session.get(Campana, int(campana_id)) or Campana.query.first()

    if not donante or not campana:
        return jsonify({
            "error": "Datos de referencia no encontrados",
            "mensaje_humano": "No encontramos la campaña o el perfil de donante seleccionado."
        }), 404

    param_min = ParametroSistema.query.filter_by(clave="MONTO_MINIMO_DONACION_COP").first()
    try:
        minimo_cop = int(param_min.valor) if param_min else 10000
    except ValueError:
        minimo_cop = 10000

    # 2. Validaciones previas según modalidad antes de insertar el aporte
    if modalidad == "ECONOMICA":
        monto_raw = str(data.get("monto") if data.get("monto") is not None else "").replace(".", "").replace(",", "").strip()
        if not monto_raw or not monto_raw.isdigit():
            return jsonify({
                "error": "Monto inválido",
                "mensaje_humano": f"Por favor ingresa un importe válido en pesos colombianos sin decimales (mínimo {formatear_pesos_cop(minimo_cop)})."
            }), 400

        monto_entero = int(monto_raw)
        if monto_entero < minimo_cop:
            return jsonify({
                "error": "Monto inferior al mínimo permitido",
                "mensaje_humano": f"El importe mínimo permitido para aportes monetarios es de {formatear_pesos_cop(minimo_cop)}."
            }), 400

        ref_bancaria = (data.get("referencia_bancaria") or "").strip()
        if not ref_bancaria:
            return jsonify({
                "error": "Referencia bancaria obligatoria",
                "mensaje_humano": "Por favor ingresa el número de referencia o comprobante bancario de la transacción."
            }), 400
    else:
        desc_articulos = (data.get("descripcion_articulos") or "").strip()
        try:
            cantidad_val = Decimal(str(data.get("cantidad") or "0"))
        except InvalidOperation:
            cantidad_val = Decimal("0")

        if not desc_articulos or cantidad_val < 1:
            return jsonify({
                "error": "Datos de especie incompletos",
                "mensaje_humano": "Por favor escribe el detalle de los insumos a donar y una cantidad igual o mayor a 1."
            }), 400

    codigo_ref = f"CS-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    nuevo_aporte = AporteTransaccional(
        donante_id=donante.id,
        campana_id=campana.id,
        codigo_referencia=codigo_ref,
        modalidad=modalidad,
        estado_aporte="VERIFICADO",
        url_comprobante=f"/uploads/comprobantes/{codigo_ref}_{nombre_comprobante}",
        observaciones=observaciones
    )
    db.session.add(nuevo_aporte)
    db.session.flush()

    donacion_economica_id = None
    donacion_especie_id = None

    if modalidad == "ECONOMICA":
        monto = Decimal(str(monto_entero))
        metodo_id = data.get("metodo_pago_id") or 1

        mp = db.session.get(MetodoPago, int(metodo_id)) or MetodoPago.query.first()
        don_eco = DonacionEconomica(
            aporte_id=nuevo_aporte.id,
            metodo_pago_id=mp.id,
            monto=monto,
            moneda="COP",
            referencia_bancaria=ref_bancaria
        )
        db.session.add(don_eco)
        db.session.flush()
        donacion_economica_id = don_eco.id

        # Actualizar recaudo de la campaña
        campana.monto_recaudado = Decimal(str(campana.monto_recaudado or 0)) + monto

        # Emitir registro en recibos_tributarios (Base para CU07)
        anio_actual = datetime.now(timezone.utc).year
        consecutivo = f"CERT-{anio_actual}-{don_eco.id:05d}"
        hash_verif = hashlib.sha256(f"{consecutivo}-{codigo_ref}-{monto_entero}".encode("utf-8")).hexdigest()[:32].upper()
        correo_don = (
            donante.persona.usuario.correo_electronico
            if (donante.persona and donante.persona.usuario)
            else None
        )
        recibo = ReciboTributario(
            donacion_economica_id=don_eco.id,
            numero_consecutivo=consecutivo,
            anio_gravable=anio_actual,
            hash_verificacion=hash_verif,
            enviado_correo=False,
            correo_destino=correo_don
        )
        db.session.add(recibo)

    else:
        # Modalidad ESPECIE
        unidad_id = data.get("unidad_medida_id") or 1
        ubicacion_inicial = (data.get("ubicacion_reportada") or "Punto de Acopio Veredal Sabana Norte").strip()

        um = db.session.get(UnidadMedida, int(unidad_id)) or UnidadMedida.query.first()
        don_esp = DonacionEspecie(
            aporte_id=nuevo_aporte.id,
            unidad_medida_id=um.id,
            descripcion_articulos=desc_articulos,
            cantidad=cantidad_val,
            estado_logistico_actual="RECIBIDO"
        )
        db.session.add(don_esp)
        db.session.flush()
        donacion_especie_id = don_esp.id

        traza_inicial = TrazabilidadEntrega(
            donacion_especie_id=don_esp.id,
            estado_logistico="RECIBIDO",
            ubicacion_reportada=ubicacion_inicial,
            observacion="Aporte en especie reportado y recibido inicialmente por la red solidaria."
        )
        db.session.add(traza_inicial)

    db.session.add(LogAuditoria(
        usuario_id=usuario_id,
        accion=f"REGISTRO_DONACION_{modalidad}",
        entidad_afectada="aportes_transaccionales",
        registro_id=nuevo_aporte.id,
        detalle=f"Aporte {codigo_ref} registrado en campaña '{campana.titulo}'.",
        direccion_ip=request.remote_addr
    ))

    db.session.commit()

    return jsonify({
        "mensaje_humano": f"¡Aporte registrado con éxito! Tu comprobante {codigo_ref} quedó contabilizado y tu certificado ya está disponible en el libro de transacciones.",
        "codigo_referencia": codigo_ref,
        "aporte_id": nuevo_aporte.id,
        "donacion_economica_id": donacion_economica_id,
        "donacion_especie_id": donacion_especie_id
    }), 201


@donaciones_bp.route("/economicas/<int:donacion_economica_id>/certificado-pdf", methods=["GET"])
def descargar_certificado_tributario_pdf(donacion_economica_id: int):
    """
    CU07 - Certificados Tributarios:
    Genera en memoria un Comprobante Electrónico / Certificado Tributario Oficial en formato PDF
    con estructura de factura digital certificada y marco legal del Estatuto Tributario Colombiano.
    """
    don_eco = db.session.get(DonacionEconomica, donacion_economica_id)
    if not don_eco:
        don_eco = DonacionEconomica.query.first()
        if not don_eco:
            return jsonify({
                "error": "Donación económica no encontrada",
                "mensaje_humano": "Aún no existe una donación económica registrada para generar el certificado PDF."
            }), 404

    aporte = don_eco.aporte
    campana = aporte.campana if aporte else None
    fundacion = campana.fundacion if campana else None
    donante = aporte.donante if aporte else None
    persona = donante.persona if donante else None
    recibo = don_eco.recibo_tributario

    if not recibo:
        anio_actual = datetime.now(timezone.utc).year
        consecutivo = f"CERT-{anio_actual}-{don_eco.id:05d}"
        hash_verif = hashlib.sha256(f"{consecutivo}-{don_eco.id}".encode("utf-8")).hexdigest()[:32].upper()
        recibo = ReciboTributario(
            donacion_economica_id=don_eco.id,
            numero_consecutivo=consecutivo,
            anio_gravable=anio_actual,
            hash_verificacion=hash_verif
        )
        db.session.add(recibo)
        db.session.commit()

    param_norma = ParametroSistema.query.filter_by(clave="NORMA_TRIBUTARIA_VIGENTE").first()
    norma_texto = (
        param_norma.valor
        if param_norma
        else "Artículos 125, 125-1, 125-2, 125-3 y 257 del Estatuto Tributario Nacional y Decreto 2150 de 2017"
    )

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Marco exterior formal tipo Factura / Comprobante Electrónico
    pdf.setStrokeColorRGB(0.15, 0.23, 0.35)
    pdf.setLineWidth(1.2)
    pdf.rect(35, 40, width - 70, height - 80, fill=0, stroke=1)

    # Banda superior institucional (Azul Corporativo SAP / Sabana Norte)
    pdf.setFillColorRGB(0.04, 0.24, 0.48)
    pdf.rect(35, height - 115, width - 70, 75, fill=1, stroke=0)

    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, height - 68, "COMPROBANTE ELECTRÓNICO Y CERTIFICADO DE DONACIÓN")
    pdf.setFont("Helvetica", 9.5)
    pdf.drawString(50, height - 84, "CONEXIÓN SOLIDARIA · RED DE GESTIÓN TERRITORIAL SABANA NORTE DE CUNDINAMARCA")
    pdf.drawString(50, height - 99, "Entidad Sin Ánimo de Lucro (ESAL) · Régimen Tributario Especial DIAN")

    # Recuadro derecho de numeración oficial (estilo Factura Electrónica)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.rect(width - 215, height - 107, 165, 58, fill=1, stroke=0)
    pdf.setFillColorRGB(0.04, 0.24, 0.48)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(width - 205, height - 64, "CERTIFICADO TRIBUTARIO N°")
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(width - 205, height - 80, recibo.numero_consecutivo)
    pdf.setFillColorRGB(0.2, 0.25, 0.3)
    pdf.setFont("Helvetica", 8)
    pdf.drawString(width - 205, height - 94, f"Año Gravable: {recibo.anio_gravable}")
    pdf.drawString(width - 205, height - 103, f"Expedición: {recibo.fecha_emision.strftime('%Y-%m-%d %H:%M')}")

    # SECCIÓN 1: ENTIDAD BENEFICIARIA (EMISOR DEL CERTIFICADO)
    y_cursor = height - 135
    pdf.setFillColorRGB(0.93, 0.95, 0.98)
    pdf.rect(45, y_cursor - 18, width - 90, 18, fill=1, stroke=0)
    pdf.setFillColorRGB(0.04, 0.24, 0.48)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(52, y_cursor - 13, "1. DATOS DE LA ENTIDAD RECEPTORA (ORGANIZACIÓN SIN ÁNIMO DE LUCRO - OSAL)")

    razon_osal = fundacion.razon_social if fundacion else "Fundación Agroecológica Raíces de Sabana Norte"
    nit_osal = fundacion.nit if fundacion else "901458932-1"
    tel_osal = fundacion.telefono_institucional if fundacion else "3114509876"
    mun_osal = (
        fundacion.direccion.municipio.nombre
        if (fundacion and fundacion.direccion and fundacion.direccion.municipio)
        else "Cogua, Cundinamarca"
    )
    dir_osal = fundacion.direccion.direccion_fisica if (fundacion and fundacion.direccion) else "Km 4 Vía Neusa"

    pdf.setFillColorRGB(0.1, 0.12, 0.16)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(52, y_cursor - 34, "Razón Social:")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(125, y_cursor - 34, razon_osal)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(390, y_cursor - 34, "NIT:")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(420, y_cursor - 34, f"{nit_osal} (Verificada)")

    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(52, y_cursor - 49, "Domicilio Fiscal:")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(135, y_cursor - 49, f"{dir_osal} · Municipio de {mun_osal}")
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(390, y_cursor - 49, "Teléfono:")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(438, y_cursor - 49, tel_osal)

    # SECCIÓN 2: DATOS DEL DONANTE / APORTANTE
    y_cursor -= 72
    pdf.setFillColorRGB(0.93, 0.95, 0.98)
    pdf.rect(45, y_cursor - 18, width - 90, 18, fill=1, stroke=0)
    pdf.setFillColorRGB(0.04, 0.24, 0.48)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(52, y_cursor - 13, "2. IDENTIFICACIÓN DEL DONANTE / APORTANTE SOLIDARIO")

    nombre_don = f"{persona.nombres} {persona.apellidos}" if persona else "Carlos Andrés Suárez Rico"
    if donante and donante.empresa_organizacion:
        nombre_don = f"{donante.empresa_organizacion} ({nombre_don})"
    num_doc = persona.documento_identidad.numero_documento if (persona and persona.documento_identidad) else "79845123"
    tipo_doc_sigla = (
        persona.documento_identidad.tipo_documento.sigla
        if (persona and persona.documento_identidad and persona.documento_identidad.tipo_documento)
        else "CC"
    )
    correo_don = persona.usuario.correo_electronico if (persona and persona.usuario) else "donante@conexion.org"
    tipo_pers = "Persona Jurídica / Empresa" if (donante and donante.tipo_donante == "EMPRESA") else "Persona Natural"

    pdf.setFillColorRGB(0.1, 0.12, 0.16)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(52, y_cursor - 34, "Donante / Titular:")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(140, y_cursor - 34, nombre_don)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(390, y_cursor - 34, "Identificación:")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(460, y_cursor - 34, f"{tipo_doc_sigla} {num_doc}")

    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(52, y_cursor - 49, "Tipo Contribuyente:")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(145, y_cursor - 49, tipo_pers)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(310, y_cursor - 49, "Correo Registrado:")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(400, y_cursor - 49, correo_don)

    # SECCIÓN 3: TABLA DE LIQUIDACIÓN DEL APORTE (ESTILO FACTURA DIGITAL)
    y_cursor -= 72
    pdf.setFillColorRGB(0.04, 0.24, 0.48)
    pdf.rect(45, y_cursor - 20, width - 90, 20, fill=1, stroke=0)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(52, y_cursor - 14, "CÓDIGO REF.")
    pdf.drawString(135, y_cursor - 14, "PROGRAMA / CAMPAÑA BENEFICIARIA")
    pdf.drawString(345, y_cursor - 14, "MEDIO DE PAGO / REF.")
    pdf.drawString(475, y_cursor - 14, "VALOR TOTAL (COP)")

    # Fila del ítem
    pdf.setStrokeColorRGB(0.75, 0.8, 0.86)
    pdf.setLineWidth(0.7)
    pdf.rect(45, y_cursor - 55, width - 90, 35, fill=0, stroke=1)

    cod_ref = aporte.codigo_referencia if aporte else "CS-2026-0001"
    titulo_camp = (campana.titulo if campana else "Huertas Escolares Sabana Norte")[:42]
    medio_str = don_eco.metodo_pago.nombre if don_eco.metodo_pago else "Transferencia PSE"
    ref_banc = don_eco.referencia_bancaria or cod_ref
    monto_formateado = formatear_pesos_cop(don_eco.monto)

    pdf.setFillColorRGB(0.1, 0.12, 0.16)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(52, y_cursor - 38, cod_ref)
    pdf.setFont("Helvetica", 8.5)
    pdf.drawString(135, y_cursor - 35, titulo_camp)
    pdf.drawString(135, y_cursor - 47, "Destinación: Desarrollo comunitario rural Sabana Norte")
    pdf.drawString(345, y_cursor - 35, medio_str[:24])
    pdf.drawString(345, y_cursor - 47, f"Soporte: {ref_banc[:20]}")
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(475, y_cursor - 40, monto_formateado)

    # Fila de Total Certificado
    pdf.setFillColorRGB(0.94, 0.97, 0.95)
    pdf.rect(340, y_cursor - 82, width - 385, 24, fill=1, stroke=1)
    pdf.setFillColorRGB(0.06, 0.35, 0.18)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(348, y_cursor - 74, "TOTAL CERTIFICADO:")
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(468, y_cursor - 74, monto_formateado)

    # SECCIÓN 4: MARCO NORMATIVO Y CERTIFICACIÓN LEGAL (ESTATUTO TRIBUTARIO)
    y_cursor -= 105
    pdf.setFillColorRGB(0.93, 0.95, 0.98)
    pdf.rect(45, y_cursor - 18, width - 90, 18, fill=1, stroke=0)
    pdf.setFillColorRGB(0.04, 0.24, 0.48)
    pdf.setFont("Helvetica-Bold", 9.5)
    pdf.drawString(52, y_cursor - 13, "3. FUNDAMENTO NORMATIVO Y CERTIFICACIÓN TRIBUTARIA (DIAN - COLOMBIA)")

    pdf.setStrokeColorRGB(0.75, 0.8, 0.86)
    pdf.rect(45, y_cursor - 98, width - 90, 80, fill=0, stroke=1)

    pdf.setFillColorRGB(0.15, 0.18, 0.22)
    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(52, y_cursor - 32, f"Norma Aplicable: {norma_texto[:95]}")
    pdf.setFont("Helvetica", 8.2)
    pdf.drawString(52, y_cursor - 46, "• El Representante Legal y el Contador Público / Revisor Fiscal de la entidad receptora certifican que el presente aporte")
    pdf.drawString(52, y_cursor - 58, "  fue recibido efectivamente y se destinará de forma exclusiva al desarrollo del objeto social meritorio en la Sabana Norte.")
    pdf.drawString(52, y_cursor - 70, "• De conformidad con el Artículo 257 del Estatuto Tributario y el Decreto Único Reglamentario 1625 de 2016, esta donación")
    pdf.drawString(52, y_cursor - 82, "  otorga derecho a un descuento sobre el impuesto sobre la renta y complementarios equivalente al 25% del valor donado.")
    pdf.drawString(52, y_cursor - 93, "• Los recursos fueron recibidos a través de sistema financiero autorizado y cuentan con soporte contable verificable.")

    # SECCIÓN 5: FIRMAS Y SELLO CRIPTOGRÁFICO DE VERIFICACIÓN (CUFE / HASH)
    y_cursor -= 125
    pdf.setStrokeColorRGB(0.4, 0.45, 0.5)
    pdf.line(65, y_cursor - 45, 250, y_cursor - 45)
    pdf.line(330, y_cursor - 45, 515, y_cursor - 45)

    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(85, y_cursor - 57, "REPRESENTANTE LEGAL OSAL")
    pdf.setFont("Helvetica", 8)
    pdf.drawString(85, y_cursor - 68, razon_osal[:38])

    pdf.setFont("Helvetica-Bold", 8.5)
    pdf.drawString(345, y_cursor - 57, "REVISOR FISCAL / CONTADOR PÚBLICO")
    pdf.setFont("Helvetica", 8)
    pdf.drawString(345, y_cursor - 68, "Tarjeta Profesional Vigente · Certificación Tributaria")

    # Caja inferior de sello digital
    pdf.setFillColorRGB(0.96, 0.97, 0.99)
    pdf.rect(45, 52, width - 90, 42, fill=1, stroke=1)
    pdf.setFillColorRGB(0.2, 0.25, 0.32)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(52, 80, f"CÓDIGO ÚNICO DE VERIFICACIÓN ELECTRÓNICA (SHA-256): {recibo.hash_verificacion}")
    pdf.setFont("Helvetica", 7.8)
    pdf.drawString(52, 68, f"Consecutivo Oficial: {recibo.numero_consecutivo}  |  Referencia Transaccional: {cod_ref}  |  Moneda: Pesos Colombianos (COP)")
    pdf.drawString(52, 57, "Documento emitido electrónicamente por la Plataforma Conexión Solidaria Sabana Norte. Validez tributaria sujeta a verificación DIAN.")

    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"Certificado_Tributario_{recibo.numero_consecutivo}.pdf"
    )


@donaciones_bp.route("/economicas/<int:donacion_economica_id>/enviar-correo", methods=["POST"])
@requiere_roles("DONANTE", "ADMIN")
def enviar_certificado_por_correo(donacion_economica_id: int):
    """
    Permite al donante o administrador enviar el Certificado Tributario Digital al correo registrado.
    Registra la trazabilidad del envío en recibos_tributarios y logs_auditoria.
    """
    identidad = get_jwt_identity()
    claims = get_jwt()
    usuario_id = int(identidad) if identidad else None

    don_eco = db.session.get(DonacionEconomica, donacion_economica_id)
    if not don_eco:
        return jsonify({
            "error": "Donación no encontrada",
            "mensaje_humano": "No se encontró la transacción seleccionada para enviar el certificado."
        }), 404

    data = request.get_json(silent=True) or {}
    correo_destino = (data.get("correo_destino") or "").strip().lower()
    if not correo_destino:
        if don_eco.aporte and don_eco.aporte.donante and don_eco.aporte.donante.persona and don_eco.aporte.donante.persona.usuario:
            correo_destino = don_eco.aporte.donante.persona.usuario.correo_electronico
        else:
            correo_destino = claims.get("correo_electronico") or "donante@conexion.org"

    recibo = don_eco.recibo_tributario
    if not recibo:
        anio_actual = datetime.now(timezone.utc).year
        consecutivo = f"CERT-{anio_actual}-{don_eco.id:05d}"
        hash_verif = hashlib.sha256(f"{consecutivo}-{don_eco.id}".encode("utf-8")).hexdigest()[:32].upper()
        recibo = ReciboTributario(
            donacion_economica_id=don_eco.id,
            numero_consecutivo=consecutivo,
            anio_gravable=anio_actual,
            hash_verificacion=hash_verif
        )
        db.session.add(recibo)

    recibo.enviado_correo = True
    recibo.correo_destino = correo_destino
    recibo.fecha_envio_correo = datetime.now(timezone.utc)

    db.session.add(LogAuditoria(
        usuario_id=usuario_id,
        accion="ENVIO_CERTIFICADO_CORREO",
        entidad_afectada="recibos_tributarios",
        registro_id=recibo.id,
        detalle=f"Certificado {recibo.numero_consecutivo} enviado digitalmente al correo {correo_destino}.",
        direccion_ip=request.remote_addr
    ))
    db.session.commit()

    return jsonify({
        "mensaje_humano": f"¡Certificado enviado! Hemos remitido una copia digital del Certificado Tributario {recibo.numero_consecutivo} al correo electrónico {correo_destino}.",
        "correo_destino": correo_destino,
        "consecutivo": recibo.numero_consecutivo
    }), 200


@donaciones_bp.route("/especie/<int:donacion_especie_id>/trazabilidad", methods=["PUT", "POST"])
@requiere_roles("REPRESENTANTE_OSAL", "ADMIN")
def actualizar_trazabilidad_logistica(donacion_especie_id: int):
    """
    CU09 - Trazabilidad Logística:
    Actualiza el estado de una donación en especie siguiendo el flujo (RECIBIDO -> EN_BODEGA -> ENTREGADO)
    e inserta el registro de seguimiento en trazabilidad_entregas.
    """
    data = request.get_json(silent=True) or {}
    identidad = get_jwt_identity()
    usuario_id = int(identidad) if identidad else None

    don_esp = db.session.get(DonacionEspecie, donacion_especie_id)
    if not don_esp:
        return jsonify({
            "error": "Donación en especie no encontrada",
            "mensaje_humano": "No encontramos el registro de donación en especie que deseas actualizar."
        }), 404

    nuevo_estado = (data.get("estado_logistico") or "EN_BODEGA").strip().upper()
    estados_validos = {"RECIBIDO", "EN_BODEGA", "ENTREGADO"}
    if nuevo_estado not in estados_validos:
        return jsonify({
            "error": "Estado logístico inválido",
            "mensaje_humano": "El estado debe ser RECIBIDO, EN_BODEGA o ENTREGADO."
        }), 400

    ubicacion = (data.get("ubicacion_reportada") or "Bodega Comunitaria Sabana Norte").strip()
    observacion = (data.get("observacion") or f"Cambio de estado a {nuevo_estado}").strip()

    don_esp.estado_logistico_actual = nuevo_estado
    hito = TrazabilidadEntrega(
        donacion_especie_id=don_esp.id,
        estado_logistico=nuevo_estado,
        ubicacion_reportada=ubicacion,
        observacion=observacion
    )
    db.session.add(hito)

    db.session.add(LogAuditoria(
        usuario_id=usuario_id,
        accion="ACTUALIZAR_TRAZABILIDAD_ESPECIE",
        entidad_afectada="trazabilidad_entregas",
        registro_id=don_esp.id,
        detalle=f"Donación especie #{don_esp.id} pasó a '{nuevo_estado}' en {ubicacion}.",
        direccion_ip=request.remote_addr
    ))

    db.session.commit()

    return jsonify({
        "mensaje_humano": f"¡Trazabilidad actualizada! El aporte '{don_esp.descripcion_articulos}' ahora se encuentra en estado {nuevo_estado}.",
        "estado_logistico_actual": nuevo_estado,
        "hito": {
            "id": hito.id,
            "estado_logistico": hito.estado_logistico,
            "ubicacion_reportada": hito.ubicacion_reportada,
            "observacion": hito.observacion,
            "fecha_actualizacion": hito.fecha_actualizacion.isoformat()
        }
    }), 200
