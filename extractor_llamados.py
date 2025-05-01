
from playwright.sync_api import sync_playwright
from datetime import datetime
import os

def extraer_llamados():
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page()
        pagina.goto("https://icbs.cl/c/v/985", timeout=90000)

        # Esperar que se cargue la tabla de llamados
        try:
            pagina.wait_for_selector("div#resultado .tabla15 tr", timeout=60000)
        except Exception as e:
            print("⚠️ No se encontró la tabla de llamados:", e)
            navegador.close()
            return []

        filas = pagina.query_selector_all("div#resultado .tabla15 tr")[1:]  # omitir cabecera

        llamados = []
        for fila in filas[:5]:
            columnas = fila.query_selector_all("td")
            if len(columnas) >= 2:
                fecha = columnas[0].inner_text().strip()
                descripcion = columnas[1].inner_text().strip()
                llamados.append((fecha, descripcion))

        navegador.close()
        return llamados

def generar_bloques(llamados):
    if not llamados:
        return '<div class="llamado"><p>No se encontró información de los llamados.</p></div>'
    return "\n".join(
        f'<div class="llamado"><p><strong>{fecha}</strong><br>{descripcion}</p></div>'
        for fecha, descripcion in llamados
    )

def generar_html(llamados):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bloques = generar_bloques(llamados)
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Últimos Llamados</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 20px;
        }}
        .contenedor {{
            max-width: 600px;
            margin: auto;
            background: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .encabezado {{
            background: #002855;
            color: white;
            padding: 16px;
            font-size: 18px;
            font-weight: bold;
        }}
        .subtitulo {{
            font-size: 16px;
            margin-top: 4px;
        }}
        .llamado {{
            border-top: 1px solid #ccc;
            padding: 12px 16px;
        }}
        .llamado p {{
            margin: 4px 0;
        }}
        .actualizado {{
            font-size: 12px;
            color: #666;
            text-align: right;
            padding: 10px 16px;
            border-top: 1px solid #ccc;
            background: #f9f9f9;
        }}
    </style>
</head>
<body>
    <div class="contenedor">
        <div class="encabezado">
            8va Compañía de Bomberos de Santiago<br>
            <span class="subtitulo">Últimos Llamados</span>
        </div>
        {bloques}
        <div class="actualizado">Actualizado: {ahora}</div>
    </div>
</body>
</html>"""
    return html

def main():
    llamados = extraer_llamados()
    html = generar_html(llamados)
    with open("llamados_actualizado.html", "w", encoding="utf-8") as archivo:
        archivo.write(html)

if __name__ == "__main__":
    main()
