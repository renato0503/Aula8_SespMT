from playwright.sync_api import sync_playwright
import subprocess

try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context()
        pg = ctx.new_page()
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

        pg.goto("file:///D:/Dev/Aula%20Sesp/Aula%208/caderno-dia8.html", wait_until="networkidle")
        print("TITLE:", pg.title())
        secs = pg.query_selector_all("section")
        print(f"Sections found: {len(secs)}")
        toc_links = pg.query_selector_all("nav.toc a")
        print(f"TOC links: {len(toc_links)}")
        if secs:
            h2 = secs[0].query_selector("h2")
            print(f"First section h2: {h2.inner_text() if h2 else 'none'}")
        print(f"Console errors: {errs}")
        theme_btn = pg.query_selector("#themebtn")
        pdf_btn = pg.query_selector("#pdfbtn")
        print(f"Theme btn: {bool(theme_btn)}, PDF btn: {bool(pdf_btn)}")

        if theme_btn:
            theme_btn.click()
            body = pg.query_selector("body")
            print(f"Theme after toggle - data-theme: {body.getAttribute('data-theme')}")

        b.close()
        print("VALIDATION OK")
except Exception as e:
    print(f"ERROR: {e}")
