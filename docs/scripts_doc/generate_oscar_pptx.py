# -*- coding: utf-8 -*-
"""
Generador de la Presentación PowerPoint (.pptx) Limpia, Visual y sin formato de plantilla (fondo blanco neutro)
para proyectar detrás de Oscar y Angélica durante la sustentación.
Reglas solicitadas por Oscar:
1. SIN guion en las diapositivas y SIN tiempos ("Minutos X a Y") en los títulos ni en el cuerpo de la diapositiva.
2. SIN exceso de texto: diapositivas limpias, con las capturas de pantalla actualizadas (que incluyen el nuevo logo y fotografías reales de las fundaciones) y viñetas muy cortas como apoyo visual.
3. Numerada Diapositiva 1 a Diapositiva 15 en exacta correspondencia 1 a 1 ("como un guante") con la Guía Maestra Visual de Estudio (GUIA_VISUAL_INTEGRAL_OSCAR_COMPLETA.docx), que es la que lleva a Oscar de la mano con el guion y los tiempos.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from generate_oscar_technical_guide import (
    SECCIONES_OSCAR,
)

DOCS_DIR = r"c:\Users\ingor\conexion-solidaria\docs"
OUT_PPTX = os.path.join(DOCS_DIR, "PRESENTACION_TECNICA_OSCAR_PARA_ANEXAR.pptx")


# Tablas resumidas y limpias para las Diapositivas 2 a 5 (sin párrafos largos en la proyección)
TABLA_PPT_OBJETIVOS = [
    ("OE1 · Diagnóstico Territorial", "4 OSAL rurales (100 % adopción) y 170 ciudadanos", "5 roles, 12 Requisitos Funcionales y 6 No Funcionales"),
    ("OE2 · Modelo Canvas Social", "Plataforma 100 % gratuita (0 % comisión a OSAL)", "Sostenibilidad vía RSE empresarial, convocatorias y reportes"),
    ("OE3 · Diseño e Ingeniería RUP", "Arquitectura ligera 3 capas + Modelo de Datos", "10 Casos de Uso y Base de Datos de 34 tablas en 5FN"),
    ("OE4 · Construcción del MVP", "Aplicación Web PWA desplegada en la nube (Render)", "Angular 17 + Leaflet (Front) y Python/Flask en 6 Blueprints"),
    ("OE5 · Validación y Calidad QA", "Piloto con 5 fundaciones referentes de la Sabana", "15/15 Casos de Prueba aprobados · Respuesta media: 19,8 ms"),
    ("OE6 · Sostenibilidad a 5 Años", "Fundación en Régimen Tributario Especial (RTE)", "Efectivo Año 0: $3,21 M · Semilla: $8,38 M · Superávit desde Año 2"),
]

TABLA_PPT_NORMATIVIDAD = [
    ("Acuerdo 012 de 2024 (UdeC / MEDIT)", "Ruta de Emprendimiento e Innovación", "MVP en producción + Plan de Negocio + Impacto en 18 municipios"),
    ("Ley 1581 de 2012 (Habeas Data)", "Autorización expresa de datos personales", "Casilla obligatoria en Paso 3 del registro con sello de fecha y hora"),
    ("Estatuto Tributario (Arts. 125-1 y 257)", "Descuento del 25 % en renta por donaciones", "Emisión automática del Certificado Tributario PDF tras confirmación"),
    ("Ley 527 de 1999 (Comercio Electrónico)", "Validez jurídica y autenticidad digital", "Sello criptográfico único (código hash) impreso en cada certificado"),
    ("Ley 720 de 2001 (Voluntariado)", "Formalización de la acción voluntaria", "Agendamiento por franjas horarias, habilidades y control de cupos"),
    ("Directiva 04 de 2012 (Cero Papel)", "Eficiencia administrativa digital", "Eliminación de planillas físicas, cuadernos y recibos en papel"),
]

TABLA_PPT_ODS = [
    ("Impacto Directo (5 ODS)", "ODS 1 · ODS 9 · ODS 10 · ODS 11 · ODS 17", "Infraestructura web gratuita para zonas rurales, cierre de brecha digital y alianzas regionales"),
    ("Impacto Misional (4 ODS)", "ODS 2 · ODS 3 · ODS 4 · ODS 15", "Campañas verificadas de nutrición/abuelos, salud, educación infantil rural y bienestar animal/ambiental"),
]

TABLA_PPT_FINANCIERA = [
    ("1. Base y Parámetros 2026", "Memoria de Cálculo (15 hojas en Excel)", "SMLMV $1.750.905 (Ley 2101) · Inflación 6,30 % · TRM $3.309,55 · UVB $12.110"),
    ("2. Inversión Inicial (Año 0)", "$28,51 M Totales ($25,30 M especie / $3,21 M efectivo)", "88,7 % ya aportado (640 h software + equipos) · Efectivo incluye reserva riesgos ($2,17 M)"),
    ("3. Operación Anual (Año 1)", "$16,23 M al año ($1,35 M / mes · 25 fundaciones)", "Servidor Render Cloud: $3,23 M/año (US$62/mes) + Contador RTE + Verificación y Mercadeo"),
    ("4. Ingresos Año 1 y Semilla", "Ingresos Año 1: $11,80 M (72,7 %) · Semilla: $8,38 M", "3 empresas RSE + convocatorias · El capital semilla cubre efectivo Año 0 y valle del mes 6"),
    ("5. Autosostenibilidad (Años 2-5)", "De 25 a 200 OSAL · Superávit desde el Año 2 (117,2 %)", "Con 7 a 13 empresas RSE (< 2 % del corredor industrial) · Retorno del efectivo en 2,88 años"),
]


def add_clean_title(slide, title_text, subtitle_text=""):
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.22), Inches(12.3), Inches(0.95))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = title_text
    r.font.size = Pt(22)
    r.font.bold = True

    if subtitle_text:
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = subtitle_text
        r2.font.size = Pt(12)
        r2.font.italic = True


def add_table_slide(prs, title_text, subtitle_text, headers, rows_data):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_clean_title(slide, title_text, subtitle_text)

    table_shape = slide.shapes.add_table(
        1 + len(rows_data), len(headers),
        Inches(0.5), Inches(1.3), Inches(12.3), Inches(5.6)
    )
    table = table_shape.table

    if len(headers) == 3:
        table.columns[0].width = Inches(3.1)
        table.columns[1].width = Inches(4.1)
        table.columns[2].width = Inches(5.1)

    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = ""
        p = cell.text_frame.paragraphs[0]
        r = p.add_run()
        r.text = h
        r.font.size = Pt(13)
        r.font.bold = True

    for i, row in enumerate(rows_data):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.text = ""
            p = cell.text_frame.paragraphs[0]
            r = p.add_run()
            r.text = val
            r.font.size = Pt(12)
            if j == 0:
                r.font.bold = True


def build_clean_visual_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # DIAPOSITIVA 1: Portadilla Limpia de la Sustentación Técnica
    s0 = prs.slides.add_slide(blank)
    logo_path = r"c:\Users\ingor\conexion-solidaria\frontend\public\assets\social\logo.jpeg"
    if os.path.exists(logo_path):
        s0.shapes.add_picture(logo_path, Inches(0.8), Inches(0.8), height=Inches(1.5))

    tb0 = s0.shapes.add_textbox(Inches(0.8), Inches(2.5), Inches(11.7), Inches(4.2))
    tf0 = tb0.text_frame
    tf0.word_wrap = True
    p0 = tf0.paragraphs[0]
    r0 = p0.add_run()
    r0.text = "CONEXIÓN SOLIDARIA: TECNOLOGÍA PARA EL CAMBIO SOCIAL\nSustentación Técnica y Funcionamiento de la Plataforma"
    r0.font.size = Pt(28)
    r0.font.bold = True

    info_lines = [
        "Oscar Giovanni Robayo Olaya · Angélica Rosa Olier Quiroga",
        "Ingeniería de Sistemas y Computación · Universidad de Cundinamarca",
        "Arquitectura · Requisitos · Casos de Uso · Pruebas de Calidad · Normatividad · ODS · Viabilidad",
        "Plataforma en Producción: https://conexion-solidaria.onrender.com/login"
    ]
    for line in info_lines:
        p = tf0.add_paragraph()
        p.space_before = Pt(10)
        r = p.add_run()
        r.text = line
        r.font.size = Pt(15)

    # DIAPOSITIVAS 2 A 5: Esquemas Ejecutivos Limpios (Sin guion ni tiempos)
    add_table_slide(
        prs,
        "Cumplimiento de los 6 Objetivos Específicos",
        "Articulación entre Diagnóstico, Modelo Canvas, Ingeniería RUP y Sostenibilidad",
        ["Objetivo Específico", "Alcance y Evidencia", "Resultado en el Proyecto"],
        TABLA_PPT_OBJETIVOS,
    )

    add_table_slide(
        prs,
        "Normatividad Aplicada en la Plataforma",
        "Cumplimiento legal integrado directamente en los flujos del software",
        ["Norma / Ley", "Exigencia Legal", "Implementación en Conexión Solidaria"],
        TABLA_PPT_NORMATIVIDAD,
    )

    add_table_slide(
        prs,
        "Impacto en 9 Objetivos de Desarrollo Sostenible (ODS)",
        "Aporte directo por infraestructura digital y aporte misional por causas rurales",
        ["Nivel de Impacto", "ODS Vinculados", "Materialización en el Territorio"],
        TABLA_PPT_ODS,
    )

    add_table_slide(
        prs,
        "Síntesis de Viabilidad Financiera y Operativa",
        "Indicadores clave de la Memoria de Cálculo a 5 años",
        ["Eje Financiero", "Cifra Clave", "Soporte Técnico y Operativo"],
        TABLA_PPT_FINANCIERA,
    )

    # DIAPOSITIVAS 6 A 15: Las 10 Pantallas Visuales Limpias (Protagonismo de las Imágenes, Cero Tiempos, Cero Guion)
    for sec in SECCIONES_OSCAR:
        slide = prs.slides.add_slide(blank)
        # Limpiar cualquier prefijo numérico largo para dejar un título limpio de proyección
        clean_title = sec["titulo"]
        add_clean_title(
            slide,
            clean_title,
            sec["req_cu"]
        )

        imgs = []
        if os.path.exists(sec.get("img_path", "")):
            imgs.append(sec["img_path"])
        if "img_path_2" in sec and os.path.exists(sec["img_path_2"]):
            imgs.append(sec["img_path_2"])

        short_bullets = sec.get("viñetas_ppt", [])

        if len(imgs) == 1:
            # Columna izquierda angosta (3.8") con 3-4 viñetas cortas; Columna derecha amplia (8.3") para la captura grande
            tb = slide.shapes.add_textbox(Inches(0.5), Inches(1.4), Inches(3.8), Inches(5.4))
            tf = tb.text_frame
            tf.word_wrap = True

            for b_idx, bullet in enumerate(short_bullets):
                p = tf.paragraphs[0] if b_idx == 0 else tf.add_paragraph()
                p.space_before = Pt(10) if b_idx > 0 else Pt(0)
                r = p.add_run()
                r.text = f"• {bullet}"
                r.font.size = Pt(14)
                if b_idx == len(short_bullets) - 1:
                    r.font.bold = True

            pic = slide.shapes.add_picture(imgs[0], Inches(4.5), Inches(1.3), width=Inches(8.3))
            if pic.height > Inches(5.6):
                ratio = Inches(5.6) / pic.height
                pic.height = int(Inches(5.6))
                pic.width = int(pic.width * ratio)

            tb_cap = slide.shapes.add_textbox(Inches(4.5), Inches(7.0), Inches(8.3), Inches(0.4))
            tf_c = tb_cap.text_frame
            tf_c.word_wrap = True
            rc = tf_c.paragraphs[0].add_run()
            rc.text = sec["img_caption"]
            rc.font.size = Pt(10)
            rc.font.italic = True

        elif len(imgs) == 2:
            # Franja superior compacta (0.85") con 3 puntos cortos en horizontal y las 2 capturas grandes abajo
            tb = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.3), Inches(0.85))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            r = p.add_run()
            r.text = "   |   ".join([f"• {b}" for b in short_bullets])
            r.font.size = Pt(12.5)
            r.font.bold = True

            for k, ipath in enumerate(imgs):
                left_pos = Inches(0.5) if k == 0 else Inches(6.75)
                pic = slide.shapes.add_picture(ipath, left_pos, Inches(2.05), width=Inches(6.05))
                if pic.height > Inches(4.85):
                    ratio = Inches(4.85) / pic.height
                    pic.height = int(Inches(4.85))
                    pic.width = int(pic.width * ratio)

            tb_cap = slide.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(12.3), Inches(0.4))
            tf_c = tb_cap.text_frame
            tf_c.word_wrap = True
            rc = tf_c.paragraphs[0].add_run()
            rc.text = sec["img_caption"]
            rc.font.size = Pt(10)
            rc.font.italic = True

    prs.save(OUT_PPTX)
    print(f"==> Presentación PowerPoint limpia (sin guion ni tiempos) generada en: {OUT_PPTX} ({os.path.getsize(OUT_PPTX):,} bytes)")


if __name__ == "__main__":
    build_clean_visual_pptx()
