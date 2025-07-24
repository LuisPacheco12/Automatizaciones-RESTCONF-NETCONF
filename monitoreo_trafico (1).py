import requests
import urllib3
import sqlite3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración del router
router = {
    "host": "10.10.20.48",
    "port": "443",
    "user": "developer",
    "pass": "C1sco12345"
}

# Conexión a la base de datos SQLite
db_conn = sqlite3.connect("metricas_red.db")
cursor = db_conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS trafico_interfaces (
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    interfaz TEXT,
    in_octets INTEGER,
    out_octets INTEGER
)
""")
db_conn.commit()

# Solicitar interfaz al usuario
interface = input("Nombre de la interfaz a monitorear (ej. GigabitEthernet2): ")

# Construir URL RESTCONF
url = f"https://{router['host']}:{router['port']}/restconf/data/ietf-interfaces:interfaces-state/interface={interface}"

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# Obtener estadísticas de tráfico
response = requests.get(url, auth=(router["user"], router["pass"]), headers=headers, verify=False)

if response.status_code == 200:
    data = response.json()
    stats = data["ietf-interfaces:interface"]["statistics"]
    in_octets = stats["in-octets"]
    out_octets = stats["out-octets"]

    print(f"[✔] Tráfico en {interface}")
    print(f"   - Entrante: {in_octets} octetos")
    print(f"   - Saliente: {out_octets} octetos")

    # Guardar en la base de datos
    cursor.execute("INSERT INTO trafico_interfaces (interfaz, in_octets, out_octets) VALUES (?, ?, ?)", (interface, in_octets, out_octets))
    db_conn.commit()
else:
    print(f"[✖] Error al obtener estadísticas (código {response.status_code}):")
    print(response.text)

db_conn.close()
