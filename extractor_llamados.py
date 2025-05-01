#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from playwright.sync_api import sync_playwright

SISPAR_URL = "https://icbs.cl/c/v/985"

def extraer_llamados():
    llamados = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(SISPAR_URL, timeout=60_000)
        page.wait_for_selector(".tabla14, .tabla15", timeout=30_000)
        filas = page.query_selector_all(".tabla14, .tabla15")
        for fila in filas[:6]:
            texto = fila.inner_text().strip().replace("\n", " / ")
            llamados.append(texto)
        browser.close()
    return llamados

def generar_html(llamados):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if llamados:
        filas_html = "\n".join(
            f'<div class="llamado">{item}</div>' for item in llamados
        )
    else:
        filas_html = '<p class="empty">No se encontró información de los llamados.</p>'

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>8va Compañía de Bomberos de Santiago - Últimos Llamados</title>
  <style>
    body {{ margin:0; padding:20px; font-family: Arial,sans-serif; }}
    .container {{ background:#fff; border-radius:8px; padding:20px; box-shadow:0 2px 8px rgba(0,0,0,0.1); }}
    h1 {{ margin:0; font-size:1.5rem; color:#003366; }}
    h2 {{ margin:4px 0 12px; font-size:1.25rem; color:#003366; }}
    .updated {{ font-size:0.9em; color:#666; margin-bottom:12px; }}
    .llamado {{ border-bottom:1px solid #ddd; padding:8px 0; font-size:1em; color:#333; }}
    .empty {{ color:#333; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>8va Compañía de Bomberos de Santiago</h1>
    <h2>Últimos Llamados</h2>
    <div class="updated">Última actualización: {ahora}</div>
    {filas_html}
  </div>
</body>
</html>"""

def main():
    llamados = extraer_llamados()
    html = generar_html(llamados)
    with open("llamados_actualizado.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
