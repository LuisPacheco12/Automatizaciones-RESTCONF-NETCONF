import requests
from requests.auth import HTTPBasicAuth
import urllib3

# Desactiva advertencias de HTTPS no verificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración
router = {
    "host": "10.10.20.48",
    "port": "443",
    "user": "developer",
    "pass": "C1sco12345"
}

# URL base RESTCONF
url = f"https://{router['host']}:{router['port']}/restconf/data/ietf-interfaces:interfaces"
headers = {
    "Accept": "application/yang-data+json"
}

# Solicitud GET
response = requests.get(
    url,
    auth=HTTPBasicAuth(router["user"], router["pass"]),
    headers=headers,
    verify=False
)

# Procesar respuesta
if response.status_code == 200:
    data = response.json()
    interfaces = data["ietf-interfaces:interfaces"]["interface"]
    for intf in interfaces:
        name = intf["name"]
        desc = intf.get("description", "Sin descripción")
        enabled = "Sí" if intf.get("enabled") else "No"
        ipv4_data = intf.get("ietf-ip:ipv4", {}).get("address", [])
        ip = ipv4_data[0]["ip"] if ipv4_data else "Sin IP"
        mask = ipv4_data[0]["netmask"] if ipv4_data else "Sin máscara"
        print(f"- {name}: {desc} | Activada: {enabled} | IP: {ip} / {mask}")
else:
    print(f"Error {response.status_code}: {response.text}")
