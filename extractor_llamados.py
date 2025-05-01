#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from playwright.sync_api import sync_playwright
from datetime import datetime

def extraer_llamados() -> list[str]:
    """
    Abre la página de SISPAR, espera a que carguen las tablas de 'Últimas
    5 emergencias' y extrae fecha, clave y descripción de cada servicio.
    """
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985", timeout=60000)
        # Esperamos a que aparezca al menos una fila de emergencia
        pagina.wait_for_selector("#resultado table tr", timeout=60000)

        filas = pagina.query_selector_all("#resultado table tr")[1:]  # saltar header
        llamados = []
        for fila in filas[:5]:  # solo los 5 primeros
            celdas = fila.query_selector_all("td")
            if len(celdas) >= 2:
                # La celda 1 suele contener fecha y clave/dirección + vehículos
                texto = celdas[1].inner_text().strip().replace("\n", " | ")
                llamados.append(texto)
        navegador.close()
        return llamados

def main():
    llamados = extraer_llamados()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Construimos el HTML final
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>8va Compañía de Bomberos de Santiago – Últimos Llamados</title>
  <style>
    body {{ margin:0; padding:0; font-family: Arial, sans-serif; }}
    .container {{ max-width: 500px; margin: auto; background: #fff;
                 border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                 overflow: hidden; }}
    .header {{ background: #003366; color: #fff; padding: 12px 20px; }}
    .header h1 {{ margin: 0; font-size: 1.1rem; }}
    .header h2 {{ margin: 4px 0 0; font-size: 1.3rem; }}
    .body {{ padding: 20px; color: #333; }}
    .body p {{ margin: 0 0 12px; font-size: 0.95rem; line-height: 1.4; }}
    .footer {{ background: #f5f5f5; padding: 8px 20px; font-size: 0.8rem;
               color: #555; text-align: right; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>8va Compañía de Bomberos de Santiago</h1>
      <h2>Últimos Llamados</h2>
    </div>
    <div class="body">
{''.join(f'      <p>{ll}</p>\\n' for ll in llamados) if llamados else '      <p>No se encontró información de los llamados.</p>'}
    </div>
    <div class="footer">
      Actualizado: {ahora}
    </div>
  </div>
</body>
</html>
"""
    # Escribimos el archivo de salida
    with open("llamados_actualizado.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
