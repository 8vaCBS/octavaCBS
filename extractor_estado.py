import requests
from bs4 import BeautifulSoup

URL = "https://icbs.cl/c/v/985"
SALIDA = "estado_carros_actualizado.html"

# Solicitar contenido del sitio
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Obtener contadores principales
contadores = soup.select('.cuadro')
conteo_html = ""
for cont in contadores:
    conteo_html += str(cont)

# Obtener carros en servicio
carros = soup.select(".carro.en-servicio")
estados = soup.select(".estado")
carros_html = ""
if carros and estados:
    carros_html += "<h2>Carros en Servicio</h2><ul style='font-size: 18px;'>"
    for carro, estado in zip(carros, estados):
        carros_html += f"<li><strong>{carro.text.strip()}</strong>: {estado.text.strip()}</li>"
    carros_html += "</ul>"
else:
    carros_html += "<p>No se encontró información de los carros.</p>"

# Construir HTML final
html_final = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Estado Máquinas Octava</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        h1 {{ color: darkred; }}
        .cuadro {{ display: inline-block; margin: 10px; }}
    </style>
</head>
<body>
    <h1>🚒 Estado Máquinas Octava</h1>
    <div>{conteo_html}</div>
    <div>{carros_html}</div>
</body>
</html>
"""

# Guardar archivo
with open(SALIDA, "w", encoding="utf-8") as f:
    f.write(html_final)

print("Archivo generado correctamente.")
