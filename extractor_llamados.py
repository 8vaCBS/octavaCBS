from playwright.sync_api import sync_playwright
from datetime import datetime
from bs4 import BeautifulSoup

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985", timeout=120000)

        pagina.wait_for_selector("#set_llamados", timeout=90000)
        html_set_llamados = pagina.query_selector("#set_llamados").inner_html()

        navegador.close()

    # Procesar con BeautifulSoup
    soup = BeautifulSoup(html_set_llamados, "html.parser")
    bloques = soup.find_all(class_=["tabla14", "tabla15"])

    llamados = []
    for i in range(0, len(bloques), 2):
        if i + 1 < len(bloques):
            fecha = bloques[i].get_text(strip=True)
            texto = bloques[i + 1].get_text(strip=True)
            llamados.append(f"<li><strong>{fecha}</strong> – {texto}</li>")
    return llamados

def generar_html(llamados):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not llamados:
        llamados_html = "<li><strong>No se encontraron llamados.</strong></li>"
    else:
        llamados_html = "\n".join(llamados)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Últimos Llamados - Octava Compañía</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 20px; font-family: Arial, sans-serif; background-color: #f5f5f5;">
    <div style="max-width: 700px; margin: auto; padding: 30px; background: #fff; border: 2px solid red; border-radius: 10px;">
        <h2 style="color: red; margin-bottom: 10px;">Últimos llamados</h2>
        <ul style="padding-left: 20px; font-size: 16px;">
            {llamados_html}
        </ul>
        <p style="text-align: right; font-size: 0.9em; color: #555;">Actualizado: {fecha_hora}</p>
    </div>
</body>
</html>"""
    return html

def main():
    llamados = extraer_llamados()
    html = generar_html(llamados)
    with open("llamados_actualizado.html", "w", encoding="utf-8") as archivo:
        archivo.write(html)

if __name__ == "__main__":
    main()
