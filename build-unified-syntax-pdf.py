#!/usr/bin/env python3
"""Build the Unified Syntax of Reality thesis PDF from its Markdown twin.

Epigraph: "The heavens declare the glory of God; and the firmament
sheweth his handywork." — Psalm 19:1 (KJV)
Date: 2026-10-05 (Monday). 93.
Authorship: Johnathan 'Qasparr' (Kasparr) Monroe, Keeper of the Secret Treasure.
Method: Scientific Illuminism.

MECHANISM: walk the Markdown line by line and pour it into a styled
letter-size PDF via fpdf2 — headings sized by depth, blockquotes
indented, tables drawn as ruled grids, body text justified.
DOCTRINE: the thesis carries a TRVVTH ledger table, so this pour
implements a real table renderer (unlike the bank-proposal script,
which honestly had no tables). One document, one script, no dead code.
"""
import os
import re
from fpdf import FPDF

_HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(_HERE, "The-Unified-Syntax-of-Reality.md")
OUT = os.path.join(_HERE, "The-Unified-Syntax-of-Reality.pdf")
TITLE = "The Unified Syntax of Reality"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


class ThesisPDF(FPDF):
    # MECHANISM: footer on every page after the title page.
    # DOCTRINE: the first page is the title; numbering it would be noise.
    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"{TITLE}  |  {self.page_no() - 1}", align="C")


def render_table(pdf, rows):
    """MECHANISM: draw a ruled table; row height grows with the longest cell.
    DOCTRINE: the ledger must be readable, not pretty — ruled lines, no
    decoration, because it is an audit instrument."""
    pdf.set_font("DejaVu", "", 8.5)
    col_w = [14, 108, (pdf.w - pdf.l_margin - pdf.r_margin) - 122]
    pdf.set_font("DejaVu", "B", 8.5)
    pdf.set_fill_color(240, 240, 240)
    x0 = pdf.get_x()
    for i, c in enumerate(rows[0]):
        pdf.cell(col_w[i], 7, c, border=1, fill=True)
    pdf.ln()
    pdf.set_font("DejaVu", "", 8.5)
    for r in rows[1:]:
        h = 7
        for i, c in enumerate(r):
            h = max(h, 7 + 4.2 * (len(c) // 45))
        y0, x0 = pdf.get_y(), pdf.get_x()
        if y0 + h > pdf.h - 30:
            pdf.add_page()
            y0, x0 = pdf.get_y(), pdf.get_x()
        for i, c in enumerate(r):
            pdf.set_xy(x0 + sum(col_w[:i]), y0)
            pdf.multi_cell(col_w[i], 6, c, border=1)
        pdf.set_xy(x0, y0 + h)
    pdf.ln(3)


def main():
    md = open(SRC, encoding="utf-8").read()
    pdf = ThesisPDF(format="Letter")
    pdf.set_margins(25.4, 25.4, 25.4)  # one-inch margins, the formal standard
    pdf.set_auto_page_break(True, margin=25.4)
    pdf.add_font("DejaVu", "", SERIF)
    pdf.add_font("DejaVu", "B", SERIF_B)
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)

    in_quote, in_table = False, []
    for line in md.split("\n"):
        s = line.rstrip()
        # MECHANISM: pipe-rows accumulate until a non-row line flushes them.
        if s.strip().startswith("|") and s.strip().endswith("|"):
            cells = [c.strip() for c in s.strip().strip("|").split("|")]
            if not re.match(r'^[\s\-|:]+$', s.strip()):
                in_table.append(cells)
            continue
        if in_table:
            render_table(pdf, in_table)
            in_table = []
        if s.startswith("# "):
            pdf.set_font("DejaVu", "B", 20)
            pdf.multi_cell(0, 9, s[2:].strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif s.startswith("## "):
            pdf.ln(3)
            pdf.set_font("DejaVu", "B", 14)
            pdf.multi_cell(0, 8, s[3:].strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        elif s.startswith(">"):
            pdf.set_x(pdf.l_margin + 10)
            pdf.set_font("DejaVu", "", 10)
            text = s.lstrip("> ").strip().replace("**", "")
            if text:
                pdf.multi_cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.ln(2)
        elif re.fullmatch(r"\*\*.+\*\*", s):
            pdf.ln(2)
            pdf.set_font("DejaVu", "B", 11)
            pdf.multi_cell(0, 7, s.strip("*").strip(),
                           new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        elif not s.strip():
            pdf.ln(3)
        elif s.strip() == "---":
            pdf.ln(4)
        else:
            # MECHANISM: Markdown image lines embed the PNG centered.
            # DOCTRINE: figures are evidence, not decoration — full width.
            m = re.match(r'!\[(.*)\]\((.+\.png)\)', s.strip())
            if m:
                alt, path = m.group(1), m.group(2)
                if not os.path.isabs(path):
                    path = os.path.join(_HERE, path)
                pdf.ln(2)
                pdf.image(path, x=pdf.l_margin, w=pdf.w - pdf.l_margin - pdf.r_margin)
                pdf.set_font("DejaVu", "", 9)
                pdf.set_text_color(90, 90, 90)
                pdf.multi_cell(0, 6, alt, new_x="LMARGIN", new_y="NEXT", align="C")
                pdf.set_text_color(0, 0, 0)
                pdf.ln(2)
                continue
            pdf.set_font("DejaVu", "", 10.5)
            pdf.multi_cell(0, 6, s.replace("**", ""),
                           new_x="LMARGIN", new_y="NEXT", align="J")
    if in_table:
        render_table(pdf, in_table)
    pdf.output(OUT)
    print(f"wrote {OUT} ({pdf.page_no()} pages)")


if __name__ == "__main__":
    main()

# "Live, Love, and let Love, Live." — 93.
