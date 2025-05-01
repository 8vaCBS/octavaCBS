
from playwright.sync_api import sync_playwright
from datetime import datetime

def extraer_llamados():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        pagina = browser.new_page()
        pagina.goto("https://icbs.cl/c/v/985", wait_until="networkidle")
        pagina.wait_for_selector(".tabla14, .tabla15", timeout=60000)
        contenido = pagina.inner_html("#resultado")
        browser.close()
        return contenido

def main():
    llamados = extraer_llamados()
    ahora = datetime.now().strftime("%d-%m-%Y %H:%M")

    html = f'''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Últimos Llamados - Octava</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
            color: #333;
        }}
        .contenedor {{
            background: #fff;
            max-width: 1000px;
            margin: auto;
            padding: 24px;
            border-radius: 10px;
            border: 2px solid #003366;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #e3000f;
            font-size: 24px;
            margin-bottom: 10px;
        }}
        h2 {{
            color: #003366;
            font-size: 20px;
            margin-top: 0;
        }}
        .timestamp {{
            font-size: 14px;
            color: #666;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 8px;
            border: 1px solid #ccc;
            font-size: 14px;
        }}
        th {{
            background-color: #f0f0f0;
            color: #000;
        }}
        @media screen and (max-width: 600px) {{
            table, thead, tbody, th, td, tr {{
                display: block;
            }}
            td {{
                border: none;
                border-bottom: 1px solid #eee;
            }}
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <h1>8va Compañía de Bomberos de Santiago</h1>
        <h2>Últimos Llamados</h2>
        <p class="timestamp">Actualizado el {ahora}</p>
        {llamados}
    </div>
</body>
</html>
'''
    with open("llamados_actualizado.html", "w", encoding="utf-8") as archivo:
        archivo.write(html)

if __name__ == "__main__":
    main()
