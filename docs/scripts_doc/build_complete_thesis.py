# -*- coding: utf-8 -*-
"""
Compilador Maestro del Documento Final de Grado:
CONEXIÓN SOLIDARIA. TECNOLOGÍA PARA EL CAMBIO SOCIAL
Genera:
1. docs/20-documento-completo-consolidado.md
2. docs/CONEXION_SOLIDARIA_PROYECTO_GRADO_FINAL.docx
"""

import os
import re
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_COLOR_INDEX
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

sys.stdout.reconfigure(encoding='utf-8')

from part1_cap1_cap2 import CAPITULO_1_Y_2
from part2_cap3_cap4 import CAPITULO_3_Y_4
from part3_cap5_cierre import CAPITULO_5_Y_CIERRE
from part4_anexos_A_a_L import ANEXOS_COMPLETOS

ALL_BLOCKS = CAPITULO_1_Y_2 + CAPITULO_3_Y_4 + CAPITULO_5_Y_CIERRE + ANEXOS_COMPLETOS


def strip_edit_tags(text):
    return text.replace("[[EDITAR]]", "").replace("[[/EDITAR]]", "")


def add_runs_with_optional_highlight(paragraph, text, font_size=12, bold=False, italic=False, highlight_manual=False):
    """Agrega runs al párrafo, resaltando en amarillo los bloques [[EDITAR]]...[[/EDITAR]] si highlight_manual=True."""
    if not highlight_manual or "[[EDITAR]]" not in text:
        clean_text = strip_edit_tags(text)
        r = paragraph.add_run(clean_text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(font_size)
        r.bold = bold
        r.italic = italic
        return

    pattern = re.compile(r'(\[\[EDITAR\]\].*?\[\[/EDITAR\]\])', re.DOTALL)
    parts = pattern.split(text)
    for part in parts:
        if not part:
            continue
        if part.startswith("[[EDITAR]]") and part.endswith("[[/EDITAR]]"):
            inner = part[len("[[EDITAR]]"):-len("[[/EDITAR]]")]
            r = paragraph.add_run(inner)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(font_size)
            r.bold = bold
            r.italic = italic
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
        else:
            r = paragraph.add_run(part)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(font_size)
            r.bold = bold
            r.italic = italic


def set_cell_border(cell, **kwargs):
    """Configura bordes sobrios estilo APA 7 para celdas de tabla."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('start', 'top', 'end', 'bottom', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key in ["sz", "val", "color", "space", "shadow"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))


def set_cell_shading(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)


def set_cell_margins(cell, top=80, bottom=80, left=110, right=110):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def add_page_number_header(section):
    header = section.header
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = hp.add_run("CONEXIÓN SOLIDARIA: TECNOLOGÍA PARA EL CAMBIO SOCIAL   ")
    run.font.name = "Times New Roman"
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(90, 90, 90)
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    hp._p.append(fldSimple)


def build_markdown(md_path):
    lines = [
        "# CONEXIÓN SOLIDARIA. TECNOLOGÍA PARA EL CAMBIO SOCIAL",
        "",
        "**OPCIÓN DE GRADO - RUTA DE EMPRENDIMIENTO E INNOVACIÓN**  ",
        "**PARA OPTAR AL TÍTULO DE INGENIERO EN SISTEMAS Y COMPUTACIÓN**",
        "",
        "**Autores:**  ",
        "ANGÉLICA ROSA OLIER QUIROGA  ",
        "OSCAR GIOVANNI ROBAYO OLAYA",
        "",
        "**UNIVERSIDAD DE CUNDINAMARCA - EXTENSIÓN CHÍA**  ",
        "**FACULTAD DE INGENIERÍA - PROGRAMA DE INGENIERÍA DE SISTEMAS Y COMPUTACIÓN**  ",
        "**2026**",
        "",
        "---",
        ""
    ]
    for btype, content in ALL_BLOCKS:
        if btype == "H1":
            lines.append(f"\n# {content}\n")
        elif btype == "H2":
            lines.append(f"\n## {content}\n")
        elif btype == "H3":
            lines.append(f"\n### {content}\n")
        elif btype == "P":
            lines.append(f"{strip_edit_tags(content)}\n")
        elif btype == "P_BOLD":
            lines.append(f"\n**{strip_edit_tags(content)}**\n")
        elif btype == "UL":
            for item in content:
                lines.append(f"- {strip_edit_tags(item)}")
            lines.append("")
        elif btype == "REF":
            for ref in content:
                lines.append(f"- {ref}")
            lines.append("")
        elif btype == "CODE":
            lines.append("```python")
            lines.append(content)
            lines.append("```\n")
        elif btype == "TABLE":
            lines.append(f"\n**{content['title']}**\n")
            headers = content["headers"]
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for row in content["rows"]:
                clean_row = [c.replace("\n", " ") for c in row]
                lines.append("| " + " | ".join(clean_row) + " |")
            lines.append(f"\n*{content['note']}*\n")
        elif btype == "IMAGE":
            lines.append(f"\n**{content['caption']}**  ")
            lines.append(f"![{content['caption']}]({content['path']})  ")
            lines.append(f"*{content['note']}*\n")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Markdown maestro generado en: {md_path}")


def build_docx(docx_path, highlight_manual=False):
    doc = Document()

    # Configuración de márgenes APA 7 (2.54 cm en los 4 lados)
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)
        add_page_number_header(section)

    # Estilo Normal base: Times New Roman 12pt, interlineado 1.5
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    normal_style.paragraph_format.space_after = Pt(6)

    # =========================================================================
    # PORTADA INSTITUCIONAL UDEC
    # =========================================================================
    cover_lines = [
        ("", 24),
        ("CONEXIÓN SOLIDARIA. TECNOLOGÍA PARA EL CAMBIO SOCIAL", 14, True),
        ("", 48),
        ("OPCIÓN DE GRADO - RUTA DE EMPRENDIMIENTO E INNOVACIÓN", 12, True),
        ("PARA OPTAR AL TÍTULO DE INGENIERO EN SISTEMAS Y COMPUTACIÓN", 12, True),
        ("", 60),
        ("ANGÉLICA ROSA OLIER QUIROGA", 12, True),
        ("OSCAR GIOVANNI ROBAYO OLAYA", 12, True),
        ("", 72),
        ("UNIVERSIDAD DE CUNDINAMARCA - EXTENSIÓN CHÍA", 12, True),
        ("PROGRAMA DE INGENIERÍA DE SISTEMAS Y COMPUTACIÓN", 12, True),
        ("FACULTAD DE INGENIERÍA", 12, True),
        ("CHÍA, CUNDINAMARCA", 12, True),
        ("2026", 12, True),
    ]
    for item in cover_lines:
        if len(item) == 2:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(item[1])
        else:
            text, size, bold = item
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.first_line_indent = Cm(0)
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(size)
            r.bold = bold

    doc.add_page_break()

    # =========================================================================
    # TABLA DE CONTENIDO COMPLETA Y ESTRUCTURADA
    # =========================================================================
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc.paragraph_format.space_after = Pt(12)
    r_toc = p_toc.add_run("TABLA DE CONTENIDO")
    r_toc.font.name = 'Times New Roman'
    r_toc.font.size = Pt(13)
    r_toc.bold = True

    for btype, content in ALL_BLOCKS:
        if btype in ("H1", "H2", "H3"):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            if btype == "H1":
                p.paragraph_format.left_indent = Cm(0)
                p.paragraph_format.space_before = Pt(6)
                r = p.add_run(content)
                r.bold = True
                r.font.size = Pt(11)
            elif btype == "H2":
                p.paragraph_format.left_indent = Cm(0.6)
                r = p.add_run(content)
                r.bold = False
                r.font.size = Pt(10.5)
            elif btype == "H3":
                p.paragraph_format.left_indent = Cm(1.2)
                r = p.add_run(content)
                r.bold = False
                r.font.size = Pt(10)
            r.font.name = 'Times New Roman'

    doc.add_page_break()

    # =========================================================================
    # LISTA DE TABLAS Y LISTA DE FIGURAS
    # =========================================================================
    p_lt = doc.add_paragraph()
    p_lt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lt.paragraph_format.space_after = Pt(10)
    r_lt = p_lt.add_run("LISTA DE TABLAS")
    r_lt.font.name = 'Times New Roman'
    r_lt.font.size = Pt(13)
    r_lt.bold = True

    for btype, content in ALL_BLOCKS:
        if btype == "TABLE":
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(content["title"])
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10.5)

    p_lf = doc.add_paragraph()
    p_lf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lf.paragraph_format.space_before = Pt(16)
    p_lf.paragraph_format.space_after = Pt(10)
    r_lf = p_lf.add_run("LISTA DE FIGURAS")
    r_lf.font.name = 'Times New Roman'
    r_lf.font.size = Pt(13)
    r_lf.bold = True

    for btype, content in ALL_BLOCKS:
        if btype == "IMAGE":
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(content["caption"])
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10.5)

    doc.add_page_break()

    # =========================================================================
    # CUERPO DEL DOCUMENTO (CAPÍTULOS 1 A 5, CIERRE, REFERENCIAS Y ANEXOS A-L)
    # =========================================================================
    first_h1 = True
    for btype, content in ALL_BLOCKS:
        if btype == "H1":
            if not first_h1:
                doc.add_page_break()
            first_h1 = False
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(content)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(13)
            r.bold = True

        elif btype == "H2":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(content)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.bold = True

        elif btype == "H3":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            r = p.add_run(content)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
            r.bold = True
            r.italic = True

        elif btype == "P":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Cm(1.27)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
            p.paragraph_format.space_after = Pt(6)
            add_runs_with_optional_highlight(p, content, font_size=12, bold=False, italic=False, highlight_manual=highlight_manual)

        elif btype == "P_BOLD":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            add_runs_with_optional_highlight(p, content, font_size=12, bold=True, italic=False, highlight_manual=highlight_manual)

        elif btype == "UL":
            for item in content:
                p = doc.add_paragraph(style='List Bullet')
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.left_indent = Cm(1.27)
                p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
                p.paragraph_format.space_after = Pt(4)
                add_runs_with_optional_highlight(p, item, font_size=12, bold=False, italic=False, highlight_manual=highlight_manual)

        elif btype == "REF":
            # Sangría francesa APA 7 (1.27 cm)
            for ref in content:
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.left_indent = Cm(1.27)
                p.paragraph_format.first_line_indent = Cm(-1.27)
                p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
                p.paragraph_format.space_after = Pt(6)
                r = p.add_run(ref)
                r.font.name = 'Times New Roman'
                r.font.size = Pt(11.5)

        elif btype == "CODE":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.left_indent = Cm(0.8)
            p.paragraph_format.right_indent = Cm(0.8)
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(8)
            r = p.add_run(content)
            r.font.name = 'Consolas'
            r.font.size = Pt(9)

        elif btype == "TABLE":
            # Título de tabla en APA 7
            parts = content["title"].split(".", 1)
            p_num = doc.add_paragraph()
            p_num.paragraph_format.space_before = Pt(10)
            p_num.paragraph_format.space_after = Pt(2)
            p_num.paragraph_format.keep_with_next = True
            r_num = p_num.add_run(parts[0].strip())
            r_num.font.name = 'Times New Roman'
            r_num.font.size = Pt(11)
            r_num.bold = True

            if len(parts) > 1:
                p_tit = doc.add_paragraph()
                p_tit.paragraph_format.space_before = Pt(0)
                p_tit.paragraph_format.space_after = Pt(4)
                p_tit.paragraph_format.keep_with_next = True
                r_tit = p_tit.add_run(parts[1].strip())
                r_tit.font.name = 'Times New Roman'
                r_tit.font.size = Pt(11)
                r_tit.italic = True

            headers = content["headers"]
            rows = content["rows"]
            table = doc.add_table(rows=1 + len(rows), cols=len(headers))
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = True

            # Encabezados de tabla con borde superior e inferior APA 7
            hdr_cells = table.rows[0].cells
            for j, h_text in enumerate(headers):
                hdr_cells[j].text = ""
                p_cell = hdr_cells[j].paragraphs[0]
                p_cell.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p_cell.paragraph_format.line_spacing = 1.05
                p_cell.paragraph_format.space_after = Pt(2)
                r_cell = p_cell.add_run(h_text)
                r_cell.font.name = 'Times New Roman'
                r_cell.font.size = Pt(9.5)
                r_cell.bold = True
                set_cell_shading(hdr_cells[j], "F2F2F2")
                set_cell_margins(hdr_cells[j], top=70, bottom=70, left=90, right=90)
                set_cell_border(
                    hdr_cells[j],
                    top={"sz": 10, "val": "single", "color": "000000"},
                    bottom={"sz": 8, "val": "single", "color": "000000"}
                )

            # Filas de datos
            for i, row_data in enumerate(rows):
                row_cells = table.rows[i + 1].cells
                is_last = (i == len(rows) - 1)
                for j, val in enumerate(row_data):
                    row_cells[j].text = ""
                    p_cell = row_cells[j].paragraphs[0]
                    p_cell.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p_cell.paragraph_format.line_spacing = 1.05
                    p_cell.paragraph_format.space_after = Pt(2)
                    r_cell = p_cell.add_run(val)
                    r_cell.font.name = 'Times New Roman'
                    r_cell.font.size = Pt(9.5)
                    set_cell_margins(row_cells[j], top=60, bottom=60, left=90, right=90)
                    if is_last:
                        set_cell_border(
                            row_cells[j],
                            bottom={"sz": 10, "val": "single", "color": "000000"}
                        )
                    else:
                        set_cell_border(
                            row_cells[j],
                            bottom={"sz": 4, "val": "single", "color": "D9D9D9"}
                        )

            # Nota al pie de la tabla
            p_note = doc.add_paragraph()
            p_note.paragraph_format.space_before = Pt(3)
            p_note.paragraph_format.space_after = Pt(10)
            p_note.paragraph_format.line_spacing = 1.1
            r_note = p_note.add_run(content["note"])
            r_note.font.name = 'Times New Roman'
            r_note.font.size = Pt(9.5)
            r_note.italic = True

        elif btype == "IMAGE":
            img_path = content["path"]
            parts = content["caption"].split(".", 1)
            p_fnum = doc.add_paragraph()
            p_fnum.paragraph_format.space_before = Pt(10)
            p_fnum.paragraph_format.space_after = Pt(2)
            p_fnum.paragraph_format.keep_with_next = True
            r_fnum = p_fnum.add_run(parts[0].strip())
            r_fnum.font.name = 'Times New Roman'
            r_fnum.font.size = Pt(11)
            r_fnum.bold = True

            if len(parts) > 1:
                p_ftit = doc.add_paragraph()
                p_ftit.paragraph_format.space_before = Pt(0)
                p_ftit.paragraph_format.space_after = Pt(4)
                p_ftit.paragraph_format.keep_with_next = True
                r_ftit = p_ftit.add_run(parts[1].strip())
                r_ftit.font.name = 'Times New Roman'
                r_ftit.font.size = Pt(11)
                r_ftit.italic = True

            if os.path.exists(img_path):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_after = Pt(4)
                p_img.paragraph_format.keep_with_next = True
                r_img = p_img.add_run()
                r_img.add_picture(img_path, width=Inches(5.7))
            else:
                print(f"ADVERTENCIA: Imagen no encontrada: {img_path}")

            p_fnote = doc.add_paragraph()
            p_fnote.paragraph_format.space_before = Pt(2)
            p_fnote.paragraph_format.space_after = Pt(10)
            p_fnote.paragraph_format.line_spacing = 1.1
            r_fnote = p_fnote.add_run(content["note"])
            r_fnote.font.name = 'Times New Roman'
            r_fnote.font.size = Pt(9.5)
            r_fnote.italic = True

    try:
        doc.save(docx_path)
        print(f"Documento Word final generado exitosamente en: {docx_path} ({os.path.getsize(docx_path):,} bytes)")
    except PermissionError:
        alt_path = docx_path.replace(".docx", "_ACUERDO_012.docx")
        doc.save(alt_path)
        print(f"AVISO: El archivo original estaba abierto en Word. Se guardó versión actualizada en: {alt_path} ({os.path.getsize(alt_path):,} bytes)")


if __name__ == "__main__":
    base_docs = r"c:\Users\ingor\conexion-solidaria\docs"
    md_out = os.path.join(base_docs, "20-documento-completo-consolidado.md")
    docx_clean_out = os.path.join(base_docs, "CONEXION_SOLIDARIA_PROYECTO_GRADO_FINAL.docx")
    docx_highlight_out = os.path.join(base_docs, "CONEXION_SOLIDARIA_PARA_EDITAR_MANUAL.docx")
    build_markdown(md_out)
    build_docx(docx_clean_out, highlight_manual=False)
    build_docx(docx_highlight_out, highlight_manual=True)

