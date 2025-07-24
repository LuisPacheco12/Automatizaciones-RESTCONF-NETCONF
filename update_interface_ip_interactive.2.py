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
new_ip = input("Dirección IP a asignar (ej. 192.168.50.1): ")
new_mask = input("Máscara de subred (ej. 255.255.255.0): ")

# URL del endpoint específico de la interfaz
url = f"https://{router['host']}:{router['port']}/restconf/data/ietf-interfaces:interfaces/interface={interface_name}"

# Cabeceras para RESTCONF con JSON
headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}

# Cuerpo JSON de configuración (reemplaza todo lo anterior en la interfaz)
payload = {
    "ietf-interfaces:interface": {
        "name": interface_name,
        "description": "Interfaz configurada vía RESTCONF",
        "type": "iana-if-type:ethernetCsmacd",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": new_ip,
                    "netmask": new_mask
                }
            ]
        },
        "ietf-ip:ipv6": {}
    }
}

# Enviar solicitud PUT
response = requests.put(
    url,
    auth=HTTPBasicAuth(router["user"], router["pass"]),
    headers=headers,
    json=payload,
    verify=False
)

# Verificar resultado
if response.status_code in [200, 201, 204]:
    print(f"[✔] La IP de la interfaz {interface_name} fue configurada correctamente.")
else:
    print(f"[✖] Error {response.status_code}: {response.text}")
