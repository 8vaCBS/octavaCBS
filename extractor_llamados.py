from playwright.sync_api import sync_playwright

def extraer_llamados():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://icbs.cl/c/v/985", wait_until="networkidle")
        page.wait_for_timeout(3000)

        try:
            tabla_llamados = page.locator("text=Actualizado").locator("..").locator("..").inner_html()
        except:
            tabla_llamados = "<p>No se encontró información de los llamados.</p>"

        browser.close()

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>8va Compañía Bomberos de Santiago</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                padding: 20px;
                background-color: #f5f5f5;
                color: #333;
            }}
            h1 {{
                color: #b30000;
            }}
            .contenedor {{
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <div class="contenedor">
            <h1>📟 Actualización</h1>
            {tabla_llamados}
        </div>
    </body>
    </html>
    """

    with open("llamados_actualizado.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    extraer_llamados()
