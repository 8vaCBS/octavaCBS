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

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Últimos Llamados - Octava Compañía</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #ffffff;
            margin: 0;
            padding: 2rem;
            display: flex;
            justify-content: center;
        }}
        .contenedor {{
            background-color: #fff;
            border: 3px solid red;
            border-radius: 12px;
            padding: 1.5rem;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: red;
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }}
        .fecha {{
            font-size: 0.9rem;
            color: #555;
            margin-bottom: 1rem;
        }}
        ul {{
            padding-left: 1.2rem;
        }}
        li {{
            margin-bottom: 0.75rem;
            line-height: 1.4;
        }}
        @media (max-width: 600px) {{
            body {{
                padding: 1rem;
            }}
            .contenedor {{
                padding: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <h1>Últimos Llamados - Octava Comp
