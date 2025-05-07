from playwright.sync_api import sync_playwright
from datetime import datetime

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985", timeout=90000)
        pagina.wait_for_selector("#set_llamados", timeout=60000)
        
        llamados_divs = pagina.locator("#set_llamados div")
        cantidad = llamados_divs.count()
        llamados_puros = []

        for i in range(cantidad):
            texto = llamados_divs.nth(i).inner_text().strip()
            if texto:
                llamados_puros.append(texto)

        navegador.close()

        # Agrupar en pares (fecha + contenido) y tomar solo los tres últimos
        llamados_agrupados = []
        for i in range(0, len(llamados_puros) - 1, 2):
            fecha = llamados_puros[i]
            contenido = llamados_puros[i + 1]
            llamados_agrupados.append((fecha, contenido))

        return llamados_agrupados[-3:]  # Solo los tres últimos llamados

def generar_html(llamados):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not llamados:
        llamados_html = "<li><strong>No se encontraron llamados.</strong></li>"
    else:
        llamados_html = "\n".join(
            f'<li><span style="font-size: 0.85em; color: #666;">{fecha}</span><br><strong>{contenido}</strong></li>'
            for fecha, contenido in llamados
        )

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
      margin-bottom: 16px;
      line-height: 1.6;
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
        print("✅ Archivo HTML actualizado correctamente.")
    except Exception as e:
        print("❌ Error al procesar los llamados:", e)

if __name__ == "__main__":
    main()
