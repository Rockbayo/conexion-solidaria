# -*- coding: utf-8 -*-
"""
Genera las 4 gráficas estadísticas académicas (sobrias, estilo APA 7, sin iconos de IA)
a partir de los datos reales de:
- docs/150_Respuestas_Conexion_Solidaria.xlsx (n = 170 ciudadanos encuestados)
- docs/Respuestas_Encuesta_Fundaciones_Conexion_Solidaria.xlsx (n = 4 fundaciones encuestadas)
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"c:\Users\ingor\conexion-solidaria\docs\figuras_originales"
os.makedirs(OUT_DIR, exist_ok=True)


def get_font(size, bold=False):
    candidates = (
        [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\timesbd.ttf", r"C:\Windows\Fonts\calibrib.ttf"]
        if bold else
        [r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\times.ttf", r"C:\Windows\Fonts\calibri.ttf"]
    )
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_horizontal_bar_panel(draw, x0, y0, w, h, title, subtitle, items, max_pct, bar_color=(43, 87, 151)):
    """Dibuja un panel sobrio de barras horizontales con etiquetas, conteos y porcentajes."""
    f_title = get_font(20, bold=True)
    f_sub = get_font(15, bold=False)
    f_lbl = get_font(15, bold=False)
    f_val = get_font(15, bold=True)
    f_axis = get_font(13, bold=False)

    # Marco del panel
    draw.rectangle([x0, y0, x0 + w, y0 + h], outline=(190, 190, 190), width=2, fill=(255, 255, 255))
    draw.text((x0 + 22, y0 + 16), title, fill=(20, 20, 20), font=f_title)
    draw.text((x0 + 22, y0 + 44), subtitle, fill=(90, 90, 90), font=f_sub)

    chart_left = x0 + 310
    chart_right = x0 + w - 115
    chart_top = y0 + 82
    chart_bottom = y0 + h - 42
    chart_w = chart_right - chart_left

    # Líneas de grilla verticales
    steps = 5
    for i in range(steps + 1):
        pct_val = (max_pct / steps) * i
        gx = int(chart_left + (chart_w * (pct_val / max_pct)))
        draw.line([(gx, chart_top - 6), (gx, chart_bottom)], fill=(228, 228, 228), width=1)
        lbl_txt = f"{int(round(pct_val))}%"
        tw = draw.textlength(lbl_txt, font=f_axis)
        draw.text((gx - tw / 2, chart_bottom + 8), lbl_txt, fill=(100, 100, 100), font=f_axis)

    draw.line([(chart_left, chart_top - 6), (chart_left, chart_bottom)], fill=(80, 80, 80), width=2)
    draw.line([(chart_left, chart_bottom), (chart_right, chart_bottom)], fill=(80, 80, 80), width=2)

    n_items = len(items)
    row_h = (chart_bottom - chart_top) / max(n_items, 1)
    bar_h = min(32, int(row_h * 0.58))

    for idx, (label, count, pct) in enumerate(items):
        cy = chart_top + idx * row_h + row_h / 2
        by0 = int(cy - bar_h / 2)
        by1 = int(cy + bar_h / 2)

        # Etiqueta izquierda (soporta salto de línea si es larga)
        if len(label) > 36 and "\n" not in label:
            words = label.split(" ")
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
            t1w = draw.textlength(line1, font=f_lbl)
            t2w = draw.textlength(line2, font=f_lbl)
            draw.text((chart_left - 12 - t1w, cy - 17), line1, fill=(30, 30, 30), font=f_lbl)
            draw.text((chart_left - 12 - t2w, cy + 1), line2, fill=(30, 30, 30), font=f_lbl)
        else:
            tw = draw.textlength(label, font=f_lbl)
            draw.text((chart_left - 12 - tw, cy - 9), label, fill=(30, 30, 30), font=f_lbl)

        bw = max(4, int(chart_w * (pct / max_pct)))
        draw.rectangle([chart_left + 1, by0, chart_left + bw, by1], fill=bar_color, outline=(30, 60, 110), width=1)

        val_txt = f"{count} ({pct:.1f}%)"
        draw.text((chart_left + bw + 8, cy - 9), val_txt, fill=(25, 25, 25), font=f_val)


def make_chart_1():
    """Gráfica 1: Conocimiento de fundaciones locales y distribución por zona/edad (n = 170)."""
    img = Image.new("RGB", (1280, 720), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    items_top = [
        ("Sí, conozco varias y sus actividades", 60, 35.3),
        ("Casi no tengo conocimiento local", 49, 28.8),
        ("Conozco de nombre, no en detalle", 42, 24.7),
        ("No conozco ninguna fundación", 19, 11.2),
    ]
    draw_horizontal_bar_panel(
        draw, 25, 20, 1230, 325,
        "A. Nivel de conocimiento sobre fundaciones activas en su municipio (Pregunta 5, n = 170)",
        "El 64,7 % de los ciudadanos encuestados desconoce total o parcialmente las actividades de las fundaciones locales",
        items_top, 50.0, bar_color=(47, 85, 151)
    )

    items_bottom = [
        ("Zona Urbana (Casco urbano)", 93, 54.7),
        ("Zona Rural / Periurbana (Vereda)", 77, 45.3),
        ("Edad: 26 a 35 años", 61, 35.9),
        ("Edad: 36 a 50 años", 59, 34.7),
        ("Edad: 18 a 25 años", 25, 14.7),
        ("Edad: Más de 50 años", 25, 14.7),
    ]
    draw_horizontal_bar_panel(
        draw, 25, 365, 1230, 335,
        "B. Distribución por zona de residencia y rango de edad de la muestra (Preguntas 1 y 4, n = 170)",
        "Participación equilibrada entre habitantes urbanos (54,7 %) y de veredas o sectores rurales (45,3 %) de la Sabana",
        items_bottom, 70.0, bar_color=(70, 114, 124)
    )

    out_path = os.path.join(OUT_DIR, "encuesta_comunidad_1_perfil_y_conocimiento.png")
    img.save(out_path, "PNG")
    print("Generada:", out_path)


def make_chart_2():
    """Gráfica 2: Causas sociales de mayor interés y formas de participación en el último año (n = 170)."""
    img = Image.new("RGB", (1280, 780), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    items_top = [
        ("Infancia y juventud", 96, 56.5),
        ("Adulto mayor", 65, 38.2),
        ("Desarrollo comunitario y rural", 60, 35.3),
        ("Medio ambiente y sostenibilidad", 56, 32.9),
        ("Educación y formación técnica", 56, 32.9),
        ("Salud y bienestar general", 43, 25.3),
        ("Cuidado y protección animal", 41, 24.1),
        ("Artes y emprendimiento local", 15, 8.8),
    ]
    draw_horizontal_bar_panel(
        draw, 25, 20, 1230, 400,
        "A. Causas sociales que despiertan mayor interés en la comunidad (Pregunta 6, opción múltiple, n = 170)",
        "Porcentaje calculado sobre los 170 encuestados (cada participante seleccionó una o varias líneas de acción)",
        items_top, 70.0, bar_color=(47, 85, 151)
    )

    items_bottom = [
        ("Voluntariado presencial en campo", 60, 35.3),
        ("Donación de bienes o insumos", 55, 32.4),
        ("Donaciones de dinero", 42, 24.7),
        ("No ha participado activamente", 35, 20.6),
        ("Voluntariado profesional / remoto", 33, 19.4),
        ("Difusión en redes sociales", 32, 18.8),
    ]
    draw_horizontal_bar_panel(
        draw, 25, 435, 1230, 325,
        "B. Modalidades de participación o apoyo a causas sociales en el último año (Pregunta 7, n = 170)",
        "Predominan el voluntariado presencial (35,3 %) y la donación de insumos en especie (32,4 %)",
        items_bottom, 50.0, bar_color=(84, 130, 53)
    )

    out_path = os.path.join(OUT_DIR, "encuesta_comunidad_2_causas_y_participacion.png")
    img.save(out_path, "PNG")
    print("Generada:", out_path)


def make_chart_3():
    """Gráfica 3: Condición indispensable para apoyar y disposición de uso de Conexión Solidaria (n = 170)."""
    img = Image.new("RGB", (1280, 660), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    items_top = [
        ("Transparencia total en uso de recursos", 99, 58.2),
        ("Claridad en actividades a realizar", 37, 21.8),
        ("Facilidad para aportar de forma digital", 18, 10.6),
        ("Cercanía comunitaria o geográfica", 16, 9.4),
    ]
    draw_horizontal_bar_panel(
        draw, 25, 20, 1230, 305,
        "A. Condición indispensable para donar o hacer voluntariado en una fundación (Pregunta 8, n = 170)",
        "El 80,0 % exige transparencia verificable en el uso de fondos (58,2 %) o claridad en las tareas de voluntariado (21,8 %)",
        items_top, 70.0, bar_color=(47, 85, 151)
    )

    items_bottom = [
        ("Totalmente dispuesto(a) a usarla", 90, 52.9),
        ("Probablemente sí la usaría", 73, 42.9),
        ("No me interesaría", 7, 4.1),
    ]
    draw_horizontal_bar_panel(
        draw, 25, 345, 1230, 295,
        "B. Disposición a utilizar la plataforma Conexión Solidaria para donar o postularse (Pregunta 9, n = 170)",
        "Aceptación positiva consolidada del 95,9 % (163 de 170 encuestados: 52,9 % totalmente dispuestos + 42,9 % probablemente sí)",
        items_bottom, 65.0, bar_color=(56, 118, 29)
    )

    out_path = os.path.join(OUT_DIR, "encuesta_comunidad_3_condicion_y_adopcion.png")
    img.save(out_path, "PNG")
    print("Generada:", out_path)


def make_chart_4():
    """Gráfica 4: Resultados de la Encuesta Diagnóstica de las 4 Fundaciones (Desafíos y Funcionalidades)."""
    img = Image.new("RGB", (1280, 680), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Severidad invertida sobre 100% o ranking directo y porcentaje de elección de módulos
    items_top = [
        ("Falta de recursos económicos (Prom. 1,25/5)", 3, 75.0),
        ("Baja visibilidad pública (Prom. 2,25/5)", 1, 25.0),
        ("Reclutar y retener voluntarios (Prom. 2,50/5)", 4, 100.0),
        ("Carga administrativa (Prom. 4,25/5)", 0, 0.0),
        ("Medir e informar impacto (Prom. 4,75/5)", 0, 0.0),
    ]
    # Mejor representamos Índice de Criticidad (de 0 a 100%, donde Puesto 1 = 100%, Puesto 2 = 75%, Puesto 3 = 50%, Puesto 4 = 25%, Puesto 5 = 0%)
    items_crit = [
        ("1. Falta de recursos económicos (Ranking 1,25)", 4, 93.8),
        ("2. Baja visibilidad pública (Ranking 2,25)", 4, 68.8),
        ("3. Reclutar y retener voluntarios (Ranking 2,50)", 4, 62.5),
        ("4. Carga administrativa (Ranking 4,25)", 4, 18.8),
        ("5. Medir e informar impacto (Ranking 4,75)", 4, 6.3),
    ]
    draw_horizontal_bar_panel(
        draw, 25, 20, 1230, 315,
        "A. Índice de criticidad de los desafíos operativos en las 4 fundaciones encuestadas (Pregunta 11, n = 4)",
        "Conversión ponderada del ranking 1 (Mayor obstáculo = 100 %) a 5 (Menor = 0 %) en Cajicá, Machetá, Simijaca y La Calera",
        items_crit, 100.0, bar_color=(140, 55, 45)
    )

    items_bottom = [
        ("Interés inmediato en plataforma gratuita", 4, 100.0),
        ("Módulo necesidades donación (dinero/insumos)", 3, 75.0),
        ("Módulo reclutamiento y agenda voluntarios", 3, 75.0),
        ("Perfil institucional verificado (confianza)", 2, 50.0),
    ]
    draw_horizontal_bar_panel(
        draw, 25, 355, 1230, 305,
        "B. Disposición de adopción y funcionalidades más valiosas seleccionadas por las OSAL (Preguntas 12 y 13, n = 4)",
        "El 100 % adoptaría la plataforma de inmediato, priorizando necesidades de donación (75 %) y agenda de voluntariado (75 %)",
        items_bottom, 100.0, bar_color=(47, 85, 151)
    )

    out_path = os.path.join(OUT_DIR, "encuesta_fundaciones_desafios_y_modulos.png")
    img.save(out_path, "PNG")
    print("Generada:", out_path)


if __name__ == "__main__":
    make_chart_1()
    make_chart_2()
    make_chart_3()
    make_chart_4()

