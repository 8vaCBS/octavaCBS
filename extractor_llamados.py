from playwright.sync_api import sync_playwright
from datetime import datetime

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985", timeout=90000)
        pagina.wait_for_selector("#set_llamados", timeout=60000)

        llamados = pagina.locator("#set_llamados div")
        cantidad = llamados.count()
        lista_llamados = []

        for i in range(cantidad):
            div = llamados.nth(i)
            texto = div.inner_text().strip()
            if texto:
                lista_llamados.append(texto)

        navegador.close()
        return lista_llamados[-6:]  # Últimos 3 llamados = 6 divs (pares: fecha + texto)

def generar_html(llamados_raw):
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    llamados = []
    for i in range(0, len(llamados_raw), 2):
        if i + 1 < len(llamados_raw):
            fecha = llamados_raw[i]
            texto = llamados_raw[i + 1]
            llamados.append(f"""
                <li>
                    <div class="fecha">{fecha}</div>
                    <div class="texto"><strong>{texto}</strong></div>
                </li>""")

    llamados_html = "\n".join(llamados) if llamados else "<li><strong>No se encontraron llamados.</strong></li>"

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Últimos Llamados - Octava Compañía</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      background-color: #f4f4f4;
      margin: 0;
      padding: 20px;
    }}
    .contenedor {{
      background-color: white;
      border: 3px solid red;
      border-radius: 15px;
      padding: 20px;
      max-width: 700px;
      margin: 0 auto;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    h1 {{
      color: red;
      font-size: 1.8em;
      margin-bottom: 10px;
    }}
    ul {{
      padding-left: 20px;
      margin-top: 10px;
    }}
    li {{
      margin-bottom: 10px;
      line-height: 1.5;
    }}
    .fecha {{
      font-size: 0.85em;
      color: #555;
    }}
    .texto {{
      font-size: 1em;
      font-weight: bold;
    }}
    .actualizado {{
      text-align: right;
      font-size: 0.9em;
      color: #666;
      margin-top: 10px;
    }}
  </style>
</head>
<body>
  <div class="contenedor">
    <h1>Últimos llamados</h1>
    <ul>
      {llamados_html}
    </ul>
    <div class="actualizado">Actualizado: {fecha_actual}</div>
  </div>
</body>
</html>"""
    return html

def guardar_html(contenido):
    with open("llamados_actualizado.html", "w", encoding="utf-8") as archivo:
        archivo.write(contenido)

def main():
    try:
        llamados = extraer_llamados()
        html = generar_html(llamados)
        guardar_html(html)
        print("✅ Archivo HTML actualizado con éxito.")
    except Exception as e:
        print("❌ Error al procesar los llamados:", e)

if __name__ == "__main__":
    main()
