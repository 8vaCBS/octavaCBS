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

        # Tomar solo los bloques impares (contenido sin fecha)
        llamados_solos = []
        for i in range(1, len(llamados_puros), 2):
            llamados_solos.append(llamados_puros[i])

        return llamados_solos[-4:]  # Los últimos 4 llamados

def generar_html(llamados):
    llamados_html = "\n<hr>\n".join(f"<p>{llamado}</p>" for llamado in llamados)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Últimos Llamados</title>
</head>
<body>
  <div id="resultado">
    {llamados_html}
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
        print("✅ HTML generado correctamente.")
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
