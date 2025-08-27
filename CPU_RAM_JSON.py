import requests
import json
from prometheus_client import Gauge, start_http_server
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Métricas
cpu_gauge = Gauge('router_cpu_usage_percent', 'Uso de CPU del router en porcentaje.')
ram_used_gauge = Gauge('router_ram_used_percent', 'Porcentaje de RAM usada en el router.')

# Datos del router
router_ip = '10.10.20.48'
username = 'developer'
password = 'C1sco12345'

def get_json(url):
    """Hace la solicitud y devuelve JSON o None."""
    headers = {'Accept': 'application/yang-data+json'}
    try:
        r = requests.get(url, auth=(username, password), headers=headers, verify=False, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error solicitando {url}: {e}")
        return None

def find_numeric_value(data, keywords):
    """
    Busca recursivamente un valor numérico que contenga alguna palabra clave.
    keywords = lista de palabras que queremos encontrar en la clave.
    """
    if isinstance(data, dict):
        for k, v in data.items():
            if any(kw.lower() in k.lower() for kw in keywords) and isinstance(v, (int, float)):
                return v
            result = find_numeric_value(v, keywords)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_numeric_value(item, keywords)
            if result is not None:
                return result
    return None

def get_cpu_usage():
    url = f"https://{router_ip}/restconf/data/Cisco-IOS-XE-process-cpu-oper:cpu-usage"
    data = get_json(url)
    if data:
        print("\n=== CPU JSON ===")
        print(json.dumps(data, indent=2))
        value = find_numeric_value(data, ["five-minute", "5min", "fiveMinute"])
        if value is not None:
            return float(value)
    return None

def get_ram_usage():
    url = f"https://{router_ip}/restconf/data/Cisco-IOS-XE-process-memory-oper:memory-usage-processes"
    data = get_json(url)
    if data:
        print("\n=== RAM JSON ===")
        print(json.dumps(data, indent=2))
        total = find_numeric_value(data, ["total-memory", "totalMem"])
        used = find_numeric_value(data, ["used-memory", "usedMem"])
        if total and used:
            return (used / total) * 100
    return None

if __name__ == '__main__':
    print("Iniciando exportador de métricas en el puerto 8000...")
    start_http_server(8000)

    while True:
        cpu_value = get_cpu_usage()
        if cpu_value is not None:
            cpu_gauge.set(cpu_value)
            print(f"CPU: {cpu_value}%")

        ram_value = get_ram_usage()
        if ram_value is not None:
            ram_used_gauge.set(ram_value)
            print(f"RAM: {ram_value:.2f}%")

        time.sleep(15)
