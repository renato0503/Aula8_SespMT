from playwright.sync_api import sync_playwright

html_path = "file:///D:/Dev/Aula%20Sesp/Aula%208/caderno-dia8.html"
pdf_path = "D:/Dev/Aula Sesp/Aula 8/Caderno Dia 8 - SESP.pdf"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(html_path, wait_until="networkidle")
    pg.wait_for_timeout(2000)
    pg.pdf(
        path=pdf_path,
        format="A4",
        print_background=True,
        margin={"top": "15mm", "bottom": "15mm", "left": "12mm", "right": "12mm"},
        display_header_footer=True,
        header_template="<div style='font-size:10px;margin-left:12mm;font-family:Archivo,sans-serif;color:#82888c'>Caderno do Dia 8 · SESP/MT</div>",
        footer_template="<div style='font-size:9px;text-align:center;width:100%;font-family:Archivo,sans-serif;color:#82888c'>Página <span class='pageNumber'></span> de <span class='totalPages'></span></div>"
    )
    b.close()
print(f"PDF gerado: {pdf_path}")
