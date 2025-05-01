from playwright.sync_api import sync_playwright
from datetime import datetime

URL = "https://icbs.cl/c/v/985"
ARCHIVO_SALIDA = "llamados_actualizado.html"

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto(URL, timeout=60000)
        pagina.wait_for_selector(".tabla14, .tabla15", timeout=60000)
        filas = pagina.query_selector_all(".tabla14, .tabla15")
        llamados = []

        for fila in filas:
            fecha = fila.query_selector("td:nth-child(2) div") or fila.query_selector("td:nth-child(2)")
            clave_direccion = fila.query_selector("td:nth-child(2)") or ""
            maquinas = fila.query_selector("td:nth-child(5)")

            llamados.append({
                "fecha": fecha.inner_text().strip() if fecha else "",
                "descripcion": clave_direccion.inner_text().strip() if clave_direccion else "",
                "maquinas": maquinas.inner_text().strip() if maquinas else "",
            })

        navegador.close()
        return llamados

def generar_html(llamados):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    bloques = ""
    for llamado in llamados:
        bloques += f"""
        <div class="llamado">
            <div class="fecha">{llamado['fecha']}</div>
            <div class="descripcion">{llamado['descripcion']}</div>
            <div class="maquinas">{llamado['maquinas']}</div>
        </div>
        """

    if not llamados:
        bloques = "<p>No se encontró información de los llamados.</p>"

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Últimos Llamados</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 2em;
        }}
        .contenedor {{
            background: white;
            max-width: 800px;
            margin: auto;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .titulo {{
            background-color: #002f6c;
            color: white;
            padding: 10px 15px;
            font-size: 1.2em;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }}
        .subtitulo {{
            font-size: 1.5em;
            font-weight: bold;
        }}
        .llamado {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        .llamado .fecha {{
            font-weight: bold;
        }}
        .actualizado {{
            font-size: 0.8em;
            color: #666;
            text-align: right;
            margin-top: 1em;
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <div class="titulo">
            8va Compañía de Bomberos de Santiago<br>
            <span class="subtitulo">Últimos Llamados</span>
        </div>
        {bloques}
        <div class="actualizado">Actualizado: {ahora}</div>
    </div>
</body>
</html>
"""

def main():
    llamados = extraer_llamados()
    html = generar_html(llamados)
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    main()
