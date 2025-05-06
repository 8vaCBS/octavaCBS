from playwright.sync_api import sync_playwright
from datetime import datetime
import time

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
        return lista_llamados

def generar_html(llamados):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Últimos Llamados - Octava Compañía</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px; }}
        h1 {{ color: #333; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 10px; }}
        .timestamp {{ font-size: 0.9em; color: #666; }}
    </style>
</head>
<body>
    <h1>Últimos Llamados - Octava Compañía</h1>
    <p class="timestamp">Última actualización: {ahora}</p>
    <ul>
        {''.join(f'<li>{llamado}</li>' for llamado in llamados)}
    </ul>
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
        print("Archivo HTML actualizado con éxito.")
    except Exception as e:
        print("Error al procesar los llamados:", e)

if __name__ == "__main__":
    main()
