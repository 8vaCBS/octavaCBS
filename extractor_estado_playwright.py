from playwright.sync_api import sync_playwright

def extraer_estado_carros():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://icbs.cl/c/v/985", wait_until="networkidle")
        page.wait_for_timeout(3000)  # esperar carga completa

        try:
            # Buscar contenedor que contiene "Carros en Servicio"
            elemento = page.locator("text=Carros en Servicio").first
            contenedor = elemento.locator("xpath=ancestor::div[contains(@class, 'col-md-6')]").first

            # Extraer HTML del contenedor
            carros_html = contenedor.inner_html()
        except Exception as e:
            print("Error al extraer carros:", e)
            carros_html = "<p>No se encontró información de los carros.</p>"

        browser.close()

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
