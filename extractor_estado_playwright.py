from playwright.sync_api import sync_playwright

def extraer_estado_carros():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://icbs.cl/c/v/985", wait_until="networkidle")
        
        # Esperar a que aparezcan los carros (3 segundos de espera por seguridad)
        page.wait_for_timeout(3000)

        # Extraer la sección que contiene el estado de los carros
        try:
            carros_html = page.locator("text=Carros en Servicio").locator("..").locator("..").inner_html()
        except:
            carros_html = "<p>No se encontró información de los carros.</p>"

        browser.close()

    # Construcción de HTML final
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Estado Máquinas Octava</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            h1 {{ color: darkred; }}
        </style>
    </head>
    <body>
        <h1>🚒 Estado Máquinas Octava</h1>
        {carros_html}
    </body>
    </html>
    """

    with open("estado_carros_actualizado.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    extraer_estado_carros()
