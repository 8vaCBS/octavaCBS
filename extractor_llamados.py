from playwright.sync_api import sync_playwright
from datetime import datetime

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985", timeout=60000)
        pagina.wait_for_selector(".tabla14", timeout=60000)

        filas = pagina.query_selector_all(".tabla14 tr")
        llamados = []

        for fila in filas[1:]:  # Saltar encabezado
            celdas = fila.query_selector_all("td")
            if len(celdas) >= 2:
                fecha = celdas[0].inner_text().strip()
                descripcion = celdas[1].inner_text().strip()
                llamados.append((fecha, descripcion))

        navegador.close()
        return llamados

def generar_html(llamados):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Últimos Llamados</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      padding: 20px;
      background-color: #f5f5f5;
      color: #333;
    }}
    .contenedor {{
      background: #fff;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      max-width: 600px;
      margin: auto;
    }}
    h1 {{
      background-color: #003366;
      color: white;
      padding: 15px;
      margin: 0;
      border-top-left-radius: 10px;
      border-top-right-radius: 10px;
      font-size: 18px;
    }}
    .cuerpo {{
      padding: 20px;
    }}
    .llamado {{
      margin-bottom: 10px;
      padding: 10px;
      border-bottom: 1px solid #ccc;
    }}
    .fecha {{
      font-weight: bold;
      color: #555;
    }}
    .actualizado {{
      text-align: right;
      margin-top: 20px;
      font-size: 0.8em;
      color: #666;
    }}
  </style>
</head>
<body>
  <div class="contenedor">
    <h1>8va Compañía de Bomberos de Santiago<br>Últimos Llamados</h1>
    <div class="cuerpo">
    {''.join(f'<div class="llamado"><div class="fecha">{fecha}</div><div>{descripcion}</div></div>' for fecha, descripcion in llamados) if llamados else "<p>No se encontró información de los llamados.</p>"}
    </div>
    <div class="actualizado">Actualizado: {ahora}</div>
  </div>
</body>
</html>
"""
    with open("llamados_actualizado.html", "w", encoding="utf-8") as f:
        f.write(html)

def main():
    llamados = extraer_llamados()
    generar_html(llamados)

if __name__ == "__main__":
    main()
