from playwright.sync_api import sync_playwright
from datetime import datetime

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985", timeout=60000)
        pagina.wait_for_selector("#set_llamados .tabla14, #set_llamados .tabla15", timeout=60000)
        llamados_html = pagina.query_selector_all("#set_llamados .tabla14, #set_llamados .tabla15")
        datos = [llamado.inner_text().strip() for llamado in llamados_html]
        navegador.close()
        return datos

def generar_html(llamados):
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lista_llamados = ""
    for i in range(0, len(llamados), 2):
        fecha = llamados[i] if i < len(llamados) else ""
        detalle = llamados[i+1] if i+1 < len(llamados) else ""
        lista_llamados += f"<li><strong>{fecha}</strong> – {detalle}</li>\n"

    html = (
        "<!DOCTYPE html>\n"
        "<html lang='es'>\n"
        "<head>\n"
        "    <meta charset='UTF-8'>\n"
        "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
        "    <title>Últimos Llamados - Octava Compañía</title>\n"
        "    <style>\n"
        "        body {\n"
        "            font-family: Arial, sans-serif;\n"
        "            background-color: #ffffff;\n"
        "            margin: 0;\n"
        "            padding: 2rem;\n"
        "            display: flex;\n"
        "            justify-content: center;\n"
        "        }\n"
        "        .contenedor {\n"
        "            background-color: #fff;\n"
        "
