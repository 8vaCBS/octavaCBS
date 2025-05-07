from playwright.sync_api import sync_playwright
from datetime import datetime

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985", timeout=90000)
        pagina.wait_for_selector("#set_llamados", timeout=60000)
        
        divs = pagina.locator("#set_llamados div")
        cantidad = divs.count()
        items = []

        for i in range(cantidad):
            texto = divs.nth(i).inner_text().strip()
            if texto:
                items.append(texto)

        navegador.close()

        # Agrupar en pares [fecha, llamado, fecha, llamado, ...] → tomar solo los llamados
        llamados = [items[i + 1] for i in range(0, len(items) - 1, 2)]
        return llamados[-4:]  # Últimos 4 llamados

def generar_html(llamados):
    filas = "\n".join(f"<tr><td>{llamado}</td></tr>" for llamado in llamados) if llamados else "<tr><td>No se encontraron llamados.</td></tr>"

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
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    td {{
      padding: 8px 0;
      border-bottom: 1px solid #ccc;
      font-size: 1em;
    }}
  </style>
</head>
<body>
  <div class="contenedor">
    <h1>Últimos llamados</h1>
    <table>
      {filas}
    </table>
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
        print("✅ Archivo HTML generado correctamente.")
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
