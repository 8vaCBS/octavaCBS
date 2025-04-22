from requests_html import HTMLSession

# Crear sesión que renderiza JavaScript
session = HTMLSession()
url = "https://icbs.cl/c/v/985"

# Obtener página y renderizar JS
r = session.get(url)
r.html.render(timeout=20)  # Renderiza el contenido dinámico

# Buscar la tabla (solo la primera encontrada)
table = r.html.find("table", first=True)

# Generar HTML completo con la tabla o un mensaje de error
html_output = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Estado Máquinas Octava</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        h2 {{ color: darkred; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #999; padding: 8px; text-align: left; }}
        th {{ background-color: #eee; }}
    </style>
</head>
<body>
    <h2>🚒 Estado Máquinas Octava</h2>
    {table_content}
</body>
</html>
""".format(table_content=table.html if table else "<p>No se encontró la tabla de estado.</p>")

# Guardar archivo como HTML en el repositorio
with open("estado_carros_actualizado.html", "w", encoding="utf-8") as f:
    f.write(html_output)
