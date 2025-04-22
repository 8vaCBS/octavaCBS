import requests
from bs4 import BeautifulSoup

# 1. Descargar la página fuente
URL = "https://icbs.cl/c/v/985"
response = requests.get(URL)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# 2. Extraer la tabla de estado de los carros (tabla completa)
tabla = soup.find('table')

# 3. Crear HTML de salida
html_final = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Estado Máquinas Octava</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 30px;
        }}
        h1 {{
            color: #c40000;
            font-size: 28px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #ccc;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #e91e63;
            color: white;
        }}
    </style>
</head>
<body>
    <h1>🚒 Estado Máquinas Octava</h1>
    {str(tabla) if tabla else "<p>No se pudo cargar la tabla de datos.</p>"}
</body>
</html>
"""

# 4. Guardar como archivo HTML para publicar en GitHub Pages
with open("estado_carros_actualizado.html", "w", encoding="utf-8") as f:
    f.write(html_final)
