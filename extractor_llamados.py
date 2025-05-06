from playwright.sync_api import sync_playwright
from datetime import datetime

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=True)
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985", timeout=120000)

        try:
            pagina.wait_for_selector("#set_llamados .tabla14, #set_llamados .tabla15", timeout=90000)
            contenido = pagina.locator("#set_llamados").inner_html()
        except Exception as e:
            contenido = f"<div style='color:red;'>ERROR: No se pudo extraer el contenido de #set_llamados. Detalles: {str(e)}</div>"
        
        navegador.close()
        return contenido

def main():
    llamados = extraer_llamados()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html = f"""<!DOCTYPE html>
<html lang='es'>
<head>
    <meta charset='UTF-8'>
    <title>Últimos Llamados</title>
    <link href='https://fonts.googleapis.com/css?family=Oswald:400,700' rel='stylesheet'>
    <style>
        body {{
            font-family: 'Oswald', sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 20px;
        }}
        .contenedor {{
            background-color: #ffffff;
            border: 3px solid #dc3545;
            border-radius: 10px;
            padding: 20px;
            max-width: 900px;
            margin: auto;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #dc3545;
            text-align: center;
        }}
        .actualizado {{
            text-align: right;
            color: #6c757d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <h1>Últimos Llamados</h1>
        <div class="actualizado">Actualizado: {ahora}</div>
        {llamados}
    </div>
</body>
</html>"""
    with open("llamados_actualizado.html", "w", encoding="utf-8") as archivo:
        archivo.write(html)

if __name__ == "__main__":
    main()
