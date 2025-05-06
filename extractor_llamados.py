
from playwright.sync_api import sync_playwright
from datetime import datetime

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985")

        # Espera primero que cargue el contenedor principal
        pagina.wait_for_selector("#set_llamados", timeout=90000)

        # Espera por los elementos específicos dentro del contenedor
        pagina.wait_for_selector("#set_llamados .tabla14, #set_llamados .tabla15", timeout=90000)
        llamados_html = pagina.query_selector_all("#set_llamados .tabla14, #set_llamados .tabla15")

        # Procesar llamados (fecha y contenido de cada fila)
        llamados = []
        for i in range(0, len(llamados_html), 2):
            if i + 1 < len(llamados_html):
                fecha = llamados_html[i].inner_text().strip()
                texto = llamados_html[i + 1].inner_text().strip()
                llamados.append(f"<li><strong>{fecha}</strong> – {texto}</li>")

        navegador.close()
        return llamados

def generate_html(llamados):
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not llamados:
        llamados_html = "<li><strong>No se encontraron llamados.</strong></li>"
    else:
        llamados_html = "\n".join(llamados)

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
    <div class="fecha">Actualizado: {fecha_actual}</div>
  </div>
</body>
</html>"""
    return html

def main():
    llamados = extraer_llamados()
    html = generate_html(llamados)
    with open("llamados_actualizado.html", "w", encoding="utf-8") as archivo:
        archivo.write(html)

if __name__ == "__main__":
    main()
