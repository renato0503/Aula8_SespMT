# -*- coding: utf-8 -*-
"""Exporta caderno-dia8.html para "Caderno Dia 8 - SESP.pdf" (A4).

Duas passadas: (1) gera o HTML e o PDF, descobre em que página cada seção
começou; (2) regera o HTML com esses números no sumário e exporta de novo.
Força tema claro, abre as respostas do quiz e cria marcadores (outline) no PDF.

Requisitos: pip install playwright pymupdf && playwright install chromium
"""
import json
import pathlib
import re
import subprocess
import sys

import pymupdf
from playwright.sync_api import sync_playwright

AQUI = pathlib.Path(__file__).resolve().parent
HTML = AQUI / "caderno-dia8.html"
PDF = AQUI / "Caderno Dia 8 - SESP.pdf"
MAPA = AQUI / "_paginas.json"

RODAPE = ('<div style="width:100%;font-family:Arial,sans-serif;font-size:8px;color:#7a8084;padding:0 13mm;'
          'display:flex;justify-content:space-between"><span>Caderno do Dia 8 · Curso de Capacitação SESP/MT</span>'
          '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>')


def gerar_html(com_paginas=False):
    args = [sys.executable, str(AQUI / "gerar_caderno_aula8.py")]
    if com_paginas:
        args.append(str(MAPA))
    subprocess.run(args, check=True)


def exportar():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(color_scheme="light")
        pg.goto(HTML.as_uri(), wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        pg.wait_for_timeout(800)
        pg.emulate_media(media="print")
        pg.pdf(path=str(PDF), prefer_css_page_size=True, print_background=True,
               display_header_footer=True, header_template="<span></span>", footer_template=RODAPE,
               outline=True, tagged=True)
        ids = pg.eval_on_selector_all("main section", "els => els.map(e => e.id)")
        b.close()
    return ids


def mapear_paginas(ids):
    doc = pymupdf.open(str(PDF))
    paginas = {}
    for n, anchor in enumerate(ids, start=1):
        alvo = f"§ {n}"
        for i, page in enumerate(doc):
            linhas = [l.strip() for l in page.get_text().splitlines()]
            if alvo in linhas:
                paginas[anchor] = i + 1
                break
    return paginas, len(doc)


gerar_html()
ids = exportar()
mapa, _ = mapear_paginas(ids)
MAPA.write_text(json.dumps(mapa), encoding="utf-8")

gerar_html(com_paginas=True)
ids = exportar()
mapa2, total = mapear_paginas(ids)
MAPA.unlink()

faltando = [a for a in ids if a not in mapa2]
if mapa != mapa2 or faltando:
    print("ATENÇÃO: sumário pode estar desalinhado", faltando, {k: (mapa.get(k), v) for k, v in mapa2.items() if mapa.get(k) != v})
print(f"PDF: {PDF.name} — {total} páginas, {len(ids)} seções no sumário")
