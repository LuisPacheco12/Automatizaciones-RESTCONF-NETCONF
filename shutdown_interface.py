import requests
from requests.auth import HTTPBasicAuth
import urllib3

# Desactiva advertencias SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración del router
router = {
    "host": "10.10.20.48",
    "port": "443",
    "user": "developer",
    "pass": "C1sco12345"
}

# Entradas del usuario
interface_name = input("Nombre de la interfaz (ej. GigabitEthernet2): ")
estado = input("¿Deseas habilitarla o deshabilitarla? (on/off): ").strip().lower()

# Determinar el valor booleano de 'enabled'
if estado == "on":
    enabled_state = True
elif estado == "off":
    enabled_state = False
else:
    print("[✖] Entrada no válida. Escribe 'on' para habilitar o 'off' para deshabilitar.")
    exit(1)

# URL RESTCONF para la interfaz
url = f"https://{router['host']}:{router['port']}/restconf/data/ietf-interfaces:interfaces/interface={interface_name}"

# Cabeceras
headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}

# Payload solo con cambio de estado
payload = {
    "ietf-interfaces:interface": {
        "name": interface_name,
        "enabled": enabled_state
    }
}

# Enviar solicitud PATCH
response = requests.patch(
    url,
    auth=HTTPBasicAuth(router["user"], router["pass"]),
    headers=headers,
    json=payload,
    verify=False
)

# Resultado
if response.status_code in [200, 204]:
    estado_str = "habilitada" if enabled_state else "deshabilitada"
    print(f"[✔] La interfaz {interface_name} fue {estado_str} correctamente.")
else:
    print(f"[✖] Error {response.status_code}: {response.text}")
