import requests
from bs4 import BeautifulSoup

url = 'https://icbs.cl/c/v/985'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# Buscar filas de estado
tabla = soup.find('table')
filas = tabla.find_all('tr')[1:]  # omite encabezado
carros = ['Q-8', 'RX-8', 'M-8']
datos = []

for fila in filas:
    celdas = fila.find_all('td')
    if not celdas or len(celdas) < 3:
        continue
    nombre = celdas[0].text.strip()
    estado = celdas[1].text.strip()
    lugar = celdas[2].text.strip()
    if nombre in carros:
        datos.append((nombre, estado, lugar))

# Crear HTML
with open('estado_carros_actualizado.html', 'w', encoding='utf-8') as f:
    f.write('<html><head><meta charset="utf-8"><title>Estado Máquinas</title></head><body>')
    f.write('<h2>🚒 Estado Máquinas Octava</h2>')
    for nombre, estado, lugar in datos:
        color = '#eb3b5a'
        if 'Servicio' in estado:
            color = '#26c281'
        elif 'Disponible' in estado:
            color = '#f7b731'
        f.write(f'<div style="margin:10px;padding:10px;border:1px solid #ccc;border-radius:6px;">')
        f.write(f'<strong>{nombre}</strong><br>')
        f.write(f'<span style="background:{color};padding:4px 8px;color:white;border-radius:12px;">{estado}</span><br>')
        f.write(f'<small>Ubicación: {lugar}</small>')
        f.write('</div>')
    f.write('</body></html>')
