import requests
from prometheus_client import Gauge, start_http_server
import time
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

router_ip = '10.10.20.48'
username = 'developer'
password = 'C1sco12345'

# Métricas Prometheus
cpu_gauge = Gauge('router_cpu_usage_percent', 'Uso de CPU del router en porcentaje.')
ram_used_gauge = Gauge('router_ram_used_percent', 'Porcentaje de RAM usada en el router.')

def print_available_keys(data, prefix=""):
    """Imprime las claves disponibles en el JSON con rutas completas."""
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f"{prefix}/{key}" if prefix else key
            print(full_key)
            print_available_keys(value, full_key)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print_available_keys(item, f"{prefix}[{i}]")

def fetch_json(url):
    """Realiza una petición RESTCONF y retorna el JSON."""
    headers = {'Accept': 'application/yang-data+json'}
    try:
        response = requests.get(url, auth=(username, password), headers=headers, verify=False, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error al obtener datos desde {url}: {e}")
        return None

def get_cpu_usage():
    url = f"https://{router_ip}/restconf/data/Cisco-IOS-XE-process-cpu-oper:cpu-usage"
    data = fetch_json(url)
    if data:
        print("\n🔍 Claves disponibles en CPU JSON:")
        print_available_keys(data)
    return None

def get_ram_usage():
    url = f"https://{router_ip}/restconf/data/Cisco-IOS-XE-process-memory-oper:memory-usage-processes"
    data = fetch_json(url)
    if data:
        print("\n🔍 Claves disponibles en RAM JSON:")
        print_available_keys(data)
    return None

if __name__ == '__main__':
    print("Iniciando detección de claves...\n")
    get_cpu_usage()
    get_ram_usage()
