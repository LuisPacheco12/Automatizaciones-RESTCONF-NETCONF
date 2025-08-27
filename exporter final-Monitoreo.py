import requests
from prometheus_client import Gauge, start_http_server
import time
import urllib3
import json

# Deshabilitar advertencias de SSL para entornos de laboratorio
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Definición de métricas de Prometheus
cpu_gauge = Gauge('router_cpu_usage_percent', 'Uso de CPU del router en porcentaje.')
ram_holding_gauge = Gauge('router_ram_holding_bytes', 'Memoria total en uso por los procesos en bytes.')
interface_traffic_in_gauge = Gauge('router_interface_traffic_in_bytes', 'Bytes de entrada en una interfaz especifica.', ['interface'])

# Datos del router
router_ip = '10.10.20.48'
username = 'developer'
password = 'C1sco12345'

def get_cpu_usage():
    restconf_url = f"https://{router_ip}/restconf/data/Cisco-IOS-XE-process-cpu-oper:cpu-usage"
    headers = {'Accept': 'application/yang-data+json'}

    try:
        response = requests.get(restconf_url, auth=(username, password), headers=headers, verify=False, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        cpu_utilization = data.get('Cisco-IOS-XE-process-cpu-oper:cpu-usage', {}).get('cpu-utilization', {})
        cpu_value = cpu_utilization.get('five-minutes')
        
        if cpu_value is None:
            print("Error: No se encontró el valor de 'five-minutes' para la CPU.")
            return None
            
        return float(cpu_value)
    except Exception as e:
        print(f"Error al obtener CPU: {e}")
        return None

def get_ram_usage():
    restconf_url = f"https://{router_ip}/restconf/data/Cisco-IOS-XE-process-memory-oper:memory-usage-processes"
    headers = {'Accept': 'application/yang-data+json'}

    try:
        response = requests.get(restconf_url, auth=(username, password), headers=headers, verify=False, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        memory_container = data.get('Cisco-IOS-XE-process-memory-oper:memory-usage-processes', {})
        memory_processes = memory_container.get('memory-usage-process', [])
        
        if not memory_processes:
            print("Error: No se encontró la lista de procesos de memoria.")
            return None
        
        # Corrección: convertimos el valor a int antes de sumarlo
        total_holding_memory = sum(int(p.get('holding-memory', 0)) for p in memory_processes)
        return total_holding_memory
    except Exception as e:
        print(f"Error al obtener RAM: {e}")
        return None
    
def get_all_interfaces_traffic():
    restconf_url = f"https://{router_ip}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces"
    headers = {'Accept': 'application/yang-data+json'}

    try:
        response = requests.get(restconf_url, auth=(username, password), headers=headers, verify=False, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        interfaces = data.get('Cisco-IOS-XE-interfaces-oper:interfaces', {}).get('interface', [])
        
        # Iterar a través de la lista de interfaces
        for interface_data in interfaces:
            interface_name = interface_data.get('name')
            traffic_stats = interface_data.get('statistics', {})
            in_bytes = traffic_stats.get('in-octets')
            
            if in_bytes is not None and interface_name is not None:
                # Establecer el valor de la métrica con la etiqueta de la interfaz
                interface_traffic_in_gauge.labels(interface=interface_name).set(float(in_bytes))
                print(f"Trafico de entrada ({interface_name}): {in_bytes} bytes")
    except Exception as e:
        print(f"Error al obtener el tráfico de la interfaz: {e}")
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
            ram_holding_gauge.set(ram_value)
            print(f"RAM (holding): {ram_value} bytes")

        # Obtener y exponer las nuevas métricas de tráfico de todas las interfaces
        get_all_interfaces_traffic()


        time.sleep(15)
