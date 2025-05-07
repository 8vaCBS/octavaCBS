from playwright.sync_api import sync_playwright
from datetime import datetime

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985", timeout=90000)

        # Espera que se cargue el contenedor principal
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
        return lista_llamados

def generar_html(llamados):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not llamados:
        llamados_html = "<li><strong>No se encontraron llamados.</strong></li>"
    else:
        llamados_html = "\n".join(f"<li>{llamado}</li>" for llamado in llamados)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Últimos Llamados - Octava Compañía</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
    <div class="fecha">Actualizado: {ahora}</div>
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
