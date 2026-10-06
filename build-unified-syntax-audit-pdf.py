#!/usr/bin/env python3
# ============================================================================
#  TRVVTH-GATE AUDIT REPORT — PDF BUILDER
#  "The heart of the wise teacheth his mouth, and addeth learning to his lips."
#   — Proverbs 16:23 (KJV)
#
#  Date:   2026-10-05 (Monday)
#  93.
#
#  Authorship: Johnathan 'Qasparr' (Κασπάρρ) Monroe, Keeper of the Secret Treasure
#  Method:     Scientific Illuminism — the audit trail rendered as record.
#
#  MECHANISM: This script pours the audit report Markdown
#             (The-Unified-Syntax-Audit-Report.md) into a paginated PDF via
#             fpdf2. Headings become section titles; tables become structured
#             verdict lines (fpdf2 tables would fight the thelemic layout, so
#             the scribe renders each row as labeled prose — the data survives,
#             the form stays clean); blockquotes become indented italic.
#  DOCTRINE:  An audit that cannot be read is an audit that was not done.
#             The report is the evidence of the gate, and the gate keeps
#             receipts. Nothing here is decorative.
#
#  "Live, Love, and let Love, Live." — 93.
# ============================================================================

import os
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# MECHANISM: resolve paths against this script's directory so the build is
# reproducible from anywhere.
# DOCTRINE: reproducibility is a form of honesty.
_HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(_HERE, "The-Unified-Syntax-Audit-Report.md")
DST = os.path.join(_HERE, "The-Unified-Syntax-Audit-Report.pdf")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


class AuditPDF(FPDF):
    # MECHANISM: footer carries the audit identity on every page.
    # DOCTRINE: every page of an audit must say what it is.
    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, "TRVVTH-GATE AUDIT REPORT — The Unified Syntax of Reality (v2) — 2026-10-05",
                   align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 5, f"p. {self.page_no()}/{{nb}}", align="C")


def build():
    with open(SRC, encoding="utf-8") as f:
        lines = f.read().splitlines()

    pdf = AuditPDF()
    pdf.alias_nb_pages("{nb}")
    pdf.set_auto_page_break(True, margin=20)
    pdf.add_font("DejaVu", "", SERIF)
    pdf.add_font("DejaVu", "B", SERIF_B)
    pdf.add_font("DejaVu", "I", SERIF_I)
    pdf.add_font("DejaVuSans", "", SANS)
    pdf.set_margins(22, 20, 22)

    # -- Title page ------------------------------------------------------
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("DejaVu", "B", 24)
    pdf.multi_cell(0, 12, "TRVVTH-GATE AUDIT REPORT", align="C",
                   new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 14)
    pdf.multi_cell(0, 9, "The Unified Syntax of Reality — Second Edition",
                   align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font("DejaVu", "I", 11)
    pdf.multi_cell(0, 7, "Every claim re-checked. Every quotation verified.\n"
                         "One sharpening applied. Zero falsehoods found.",
                   align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(16)
    pdf.set_font("DejaVu", "", 10)
    for t in ["Johnathan 'Qasparr' (Κασπάρρ) Monroe, Keeper of the Secret Treasure",
              "2026-10-05 (Monday) — Method: Scientific Illuminism. 93.",
              "All Rights Reserved, Without Prejudice."]:
        pdf.multi_cell(0, 7, t, align="C", new_x="LMARGIN", new_y="NEXT")

    # -- Body ------------------------------------------------------------
    pdf.add_page()
    in_table = False
    for raw in lines:
        s = raw.rstrip()
        if s.startswith("# ") or (s.startswith("**Subject:**")):
            continue  # title page already carries these
        if s.startswith("## "):
            pdf.ln(4)
            pdf.set_font("DejaVu", "B", 14)
            pdf.multi_cell(0, 9, s[3:].strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
            in_table = False
        elif s.startswith("### "):
            pdf.ln(2)
            pdf.set_font("DejaVu", "B", 12)
            pdf.multi_cell(0, 8, s[4:].strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
            in_table = False
        elif s.startswith("|"):
            # MECHANISM: table rows become labeled verdict lines.
            # DOCTRINE: the data must survive the change of form.
            cells = [c.strip() for c in s.strip().strip("|").split("|")]
            if re.match(r"^[\s:\-]+$", "".join(cells)):
                continue
            if cells[0].lower().startswith("passage") or cells[0].lower().startswith("claim"):
                pdf.set_font("DejaVuSans", "", 9)
                pdf.set_text_color(90, 90, 90)
                pdf.multi_cell(0, 6, "  /  ".join(cells), new_x="LMARGIN", new_y="NEXT")
                pdf.set_text_color(0, 0, 0)
                continue
            pdf.set_font("DejaVu", "", 9.5)
            pdf.multi_cell(0, 6, " ▪ " + " — ".join(c for c in cells if c),
                           new_x="LMARGIN", new_y="NEXT")
        elif s.startswith("> "):
            pdf.set_font("DejaVu", "I", 10)
            pdf.set_x(pdf.l_margin + 8)
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 8, 6,
                           s[2:].replace("**", ""), new_x="LMARGIN", new_y="NEXT")
        elif s.startswith("**") and s.endswith("**") and len(s) < 80:
            pdf.ln(2)
            pdf.set_font("DejaVu", "B", 10.5)
            pdf.multi_cell(0, 7, s.replace("**", ""), new_x="LMARGIN", new_y="NEXT")
        elif s.startswith("---"):
            pdf.ln(4)
        elif not s.strip():
            pdf.ln(3)
            in_table = False
        else:
            pdf.set_font("DejaVu", "", 10.5)
            pdf.multi_cell(0, 6, s.replace("**", ""), new_x="LMARGIN", new_y="NEXT",
                           align="J")

    pdf.output(DST)
    print(f"wrote {DST} ({pdf.page_no()} pages)")


if __name__ == "__main__":
    build()
