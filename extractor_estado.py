import requests
from bs4 import BeautifulSoup

# URL desde donde se extraerán los datos
url = "https://icbs.cl/c/v/985"

try:
    # Hacer la solicitud HTTP
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    # Guardar el HTML descargado para depurar
    with open("debug_icbs.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    # Procesar el HTML con BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    tabla = soup.find("table")

    if not tabla:
        raise ValueError("No se encontró ninguna tabla en el HTML.")

    # Construir el archivo HTML de salida
    html_salida = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Estado Máquinas Octava</title>
        <style>
            body { font-family: Arial, sans-serif; }
            h1 { color: #b00; }
            table { width: 100%%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #999; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>🚒 Estado Máquinas Octava</h1>
        %s
    </body>
    </html>
    """ % str(tabla)

    # Guardar el HTML generado
    with open("estado_carros_actualizado.html", "w", encoding="utf-8") as f:
        f.write(html_salida)

except Exception as e:
    with open("estado_carros_actualizado.html", "w", encoding="utf-8") as f:
        f.write(f"<h1>Error al obtener datos:</h1><pre>{e}</pre>")
