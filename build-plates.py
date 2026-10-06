#!/usr/bin/env python3
# ============================================================================
#  COMMEMORATIVE PLATE BUILDER — Liber Cell, the three figures
#  "And God saw every thing that he had made, and, behold, it was very good."
#   — Genesis 1:31 (KJV)
#
#  Date:   2026-10-06 (Tuesday)
#  93.
#
#  Authorship: Johnathan 'Qasparr' (Κασπάρρ) Monroe, Keeper of the Secret Treasure
#  Method:     Scientific Illuminism — the figures dressed for keeping.
#
#  MECHANISM: Each figure SVG (the schematic cell divisions) is lifted from
#             its source file, set inside a plate frame — double-rule border,
#             plate number, title cartouche, authorship line — and rendered
#             at 2400 px wide via cairosvg for print-grade keeps.
#  DOCTRINE:  A plate is not a diagram. A diagram explains; a plate
#             commemorates. The same lines, given the dignity of the frame,
#             become something the eye keeps. The science does not change;
#             the keeping does.
#
#  "Live, Love, and let Love, Live." — 93.
# ============================================================================

import os
import re
import cairosvg

# MECHANISM: paths resolve against this script's directory.
# DOCTRINE: reproducibility is a form of honesty.
_HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(_HERE, "figs")
PLATEDIR = os.path.join(FIGDIR, "plates")
os.makedirs(PLATEDIR, exist_ok=True)

PLATES = [
    ("The-Unified-Syntax-Fig1-Mitosis.svg", "I", "MITOSIS",
     "THE ONE BECOMES TWO"),
    ("The-Unified-Syntax-Fig2-Meiosis.svg", "II", "MEIOSIS",
     "THE HALVING THAT ASSIGNS"),
    ("The-Unified-Syntax-Fig3-Mitochondria.svg", "III",
     "THE SPLITTING OF THE MITOCHONDRIA", "THE MATERNAL LINE UNBROKEN"),
]

W, H = 1200, 940  # the plate


def inner_svg(path):
    # MECHANISM: lift the figure's inner content out of its <svg> wrapper.
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    m = re.search(r"<svg[^>]*>(.*)</svg>", txt, re.S)
    return m.group(1)


def plate(inner, numeral, title, subtitle, out_svg, out_png):
    # MECHANISM: figure art is 920 wide; center it in the plate's middle band.
    body = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img">
  <rect x="0" y="0" width="{W}" height="{H}" fill="#fdfdfa"/>
  <rect x="18" y="18" width="{W-36}" height="{H-36}" fill="none" stroke="#000" stroke-width="5"/>
  <rect x="34" y="34" width="{W-68}" height="{H-68}" fill="none" stroke="#000" stroke-width="2"/>
  <g font-family="Georgia, serif" fill="#000" text-anchor="middle">
    <text x="{W//2}" y="110" font-size="30" letter-spacing="10">PLATE {numeral}</text>
    <text x="{W//2}" y="160" font-size="40">{title}</text>
    <text x="{W//2}" y="200" font-size="22" font-style="italic">{subtitle}</text>
    <text x="{W//2}" y="{H-90}" font-size="19">Johnathan &#x27;Qasparr&#x27; (\u039a\u03b1\u03c3\u03c0\u03ac\u03c1\u03c1) Monroe</text>
    <text x="{W//2}" y="{H-60}" font-size="16" font-style="italic">Keeper of the Secret Treasure &#183; Liber Cell &#183; XXXII &#183; 2026</text>
  </g>
  <g transform="translate({(W-920)//2},250)">
  {inner}
  </g>
</svg>"""
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(body)
    # MECHANISM: 2400 px wide — print-grade keeps.
    cairosvg.svg2png(url=out_svg, write_to=out_png, output_width=2400,
                     background_color="white")
    print("plated", os.path.basename(out_png))


for fname, numeral, title, subtitle in PLATES:
    inner = inner_svg(os.path.join(FIGDIR, fname))
    base = fname.replace(".svg", "")
    plate(inner, numeral, title, subtitle,
          os.path.join(PLATEDIR, base + "-Plate.svg"),
          os.path.join(PLATEDIR, base + "-Plate.png"))
