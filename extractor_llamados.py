from playwright.sync_api import sync_playwright
from datetime import datetime
from bs4 import BeautifulSoup

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985", timeout=60000)
        pagina.wait_for_selector("#set_llamados", timeout=60000)
        html = pagina.inner_html("#set_llamados")
        navegador.close()
        return html

def procesar_html(html):
    soup = BeautifulSoup(html, "html.parser")
    llamados = []

    filas = soup.select("tr")
    for fila in filas:
        columnas = fila.find_all("td")
        if len(columnas) >= 2:
            hora = columnas[0].get_text(strip=True)
            detalle = columnas[1].get_text(strip=True)
            if hora and detalle:
                llamados.append(f"{hora} - {detalle}")
    return llamados

def generar_html(llamados):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Últimos Llamados - Octava Compañía</title>
    </head>
    <body>
        <h2>Últimos Llamados - Octava Compañía</h2>
        <p>Última actualización: {ahora}</p>
        <ul>
    """
    for llamado in llamados:
        html += f"<li>{llamado}</li>\n"
    html += """
        </ul>
    </body>
    </html>
    """
    return html

def guardar_html(html):
    with open("llamados_actualizado.html", "w", encoding="utf-8") as archivo:
        archivo.write(html)

def main():
    html_crudo = extraer_llamados()
    llamados = procesar_html(html_crudo)
    html_final = generar_html(llamados)
    guardar_html(html_final)

if __name__ == "__main__":
    main()
