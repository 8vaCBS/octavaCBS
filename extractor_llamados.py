from playwright.sync_api import sync_playwright
import datetime

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985", timeout=120000)

        pagina.wait_for_selector("#set_llamados > div", timeout=60000)
        llamados_html = pagina.locator("#set_llamados > div").all()
        llamados = []

        total = len(llamados_html)
        pares = total if total % 2 == 0 else total - 1  # Asegura que haya pares

        for i in range(0, pares, 2):
            fecha = llamados_html[i].inner_text().strip()
            texto = llamados_html[i+1].inner_text().strip()
            llamados.append(f"{fecha} - {texto}")

        navegador.close()
        return llamados

def main():
    llamados = extraer_llamados()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("llamados_actualizado.html", "w", encoding="utf-8") as f:
        f.write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Últimos Llamados</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    padding: 20px;
                }}
                .llamado {{
                    margin-bottom: 10px;
                    padding: 10px;
                    border-left: 4px solid #c00;
                    background-color: #fff;
                }}
                .timestamp {{
                    font-size: 12px;
                    color: #888;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <h2>Últimos Llamados - Octava Compañía</h2>
        """)

        for llamado in llamados:
            f.write(f'<div class="llamado">{llamado}</div>\n')

        f.write(f"""
            <div class="timestamp">Última actualización: {now}</div>
        </body>
        </html>
        """)

if __name__ == "__main__":
    main()
