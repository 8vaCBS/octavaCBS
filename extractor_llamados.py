from playwright.sync_api import sync_playwright
from datetime import datetime
from bs4 import BeautifulSoup

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985", timeout=60000)

        try:
            pagina.wait_for_selector("#set_llamados .tabla14, #set_llamados .tabla15", timeout=60000, state="attached")
            llamados_html = pagina.query_selector_all("#set_llamados .tabla14, #set_llamados .tabla15")
            datos = [llamado.inner_html().strip() for llamado in llamados_html]
        except Exception as e:
            datos = []
            print(f"[ERROR] No se pudo obtener llamados: {e}")

        navegador.close()
        return datos

def generar_html(llamados_html):
    fecha_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    lista_llamados = "\n".join(f"<li>{BeautifulSoup(llamado, 'html.parser').get_text(strip=True)}</li>" for llamado in llamados_html)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Últimos Llamados</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 1rem;
        }}
        .contenedor {{
            max-width: 800px;
            margin: auto;
            background-color: #fff;
            border: 2px solid #d32f2f;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 0 8px rgba(0,0,0,0.1);
        }}
        h2 {{
            color: #d32f2f;
            margin-top: 0;
        }}
        ul {{
            padding-left: 1.2rem;
        }}
        li {{
            margin-bottom: 0.75rem;
            line-height: 1.4;
        }}
        .fecha {{
            text-align: right;
            font-size: 0.9rem;
            color: #666;
            margin-top: 1rem;
        }}
        @media (max-width: 600px) {{
            .contenedor {{
                padding: 0.75rem;
            }}
            li {{
                font-size: 0.95rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <h2>Últimos llamados</h2>
        <ul>
            {lista_llamados if lista_llamados else "<li>No se encontraron llamados.</li>"}
        </ul>
        <div class="fecha">Actualizado: {fecha_hora}</div>
    </div>
</body>
</html>"""
    
    return html

def guardar_html(html, nombre_archivo="llamados_actualizado.html"):
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(html)

def main():
    llamados = extraer_llamados()
    html = generar_html(llamados)
    guardar_html(html)

if __name__ == "__main__":
    main()
