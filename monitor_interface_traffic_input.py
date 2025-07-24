
import requests
from requests.auth import HTTPBasicAuth
import urllib3

# Desactiva advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración
router = {
    "host": "10.10.20.48",
    "port": "443",
    "user": "developer",
    "pass": "C1sco12345"
}

# Pedir interfaz por consola
interface = input("Nombre de la interfaz a monitorear (ej. GigabitEthernet3): ")

# URL del endpoint de estado de interfaces
url = f"https://{router['host']}:{router['port']}/restconf/data/ietf-interfaces:interfaces-state/interface"

# Cabeceras
headers = {
    "Accept": "application/yang-data+json"
}

def get_traffic():
    response = requests.get(
        url,
        auth=HTTPBasicAuth(router["user"], router["pass"]),
        headers=headers,
        verify=False
    )

    if response.status_code == 200:
        data = response.json()
        interfaces = data["ietf-interfaces:interface"]

        for iface in interfaces:
            if iface["name"] == interface:
                stats = iface.get("statistics", {})
                in_octets = stats.get("in-octets", 0)
                out_octets = stats.get("out-octets", 0)
                in_errors = stats.get("in-errors", 0)
                out_errors = stats.get("out-errors", 0)

                print(f"📡 Interfaz: {interface}")
                print(f"↓ Tráfico recibido (in-octets): {in_octets} bytes")
                print(f"↑ Tráfico enviado (out-octets): {out_octets} bytes")
                print(f"✖ Errores de entrada: {in_errors}")
                print(f"✖ Errores de salida: {out_errors}")
                return

        print(f"[✖] La interfaz {interface} no fue encontrada.")
    else:
        print(f"[✖] Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    print(f"Monitoreando interfaz {interface}...\n")
    get_traffic()
