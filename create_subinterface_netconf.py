from ncclient import manager
from lxml import etree

# Solicita datos al usuario
main_interface = input("Nombre de la interfaz principal (ej. GigabitEthernet3): ").strip()
vlan_id = input("ID de VLAN (ej. 20): ").strip()
ip_address = input("Dirección IP (ej. 192.168.20.1): ").strip()
subnet_mask = input("Máscara de subred (ej. 255.255.255.0): ").strip()

subinterface_name = f"{main_interface}.{vlan_id}"

# Plantilla XML para crear subinterfaz
config = f"""
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <GigabitEthernet>
        <name>{subinterface_name}</name>
        <encapsulation>
          <dot1Q>
            <vlan-id>{vlan_id}</vlan-id>
          </dot1Q>
        </encapsulation>
        <ip>
          <address>
            <primary>
              <address>{ip_address}</address>
              <mask>{subnet_mask}</mask>
            </primary>
          </address>
        </ip>
      </GigabitEthernet>
    </interface>
  </native>
</config>
"""

# Datos del router (sandbox)
router = {
    "host": "10.10.20.48",
    "port": 830,
    "username": "developer",
    "password": "C1sco12345"
}

# Establece conexión NETCONF y aplica configuración
with manager.connect(
    host=router["host"],
    port=router["port"],
    username=router["username"],
    password=router["password"],
    hostkey_verify=False
) as m:
    netconf_reply = m.edit_config(target="running", config=config)
    print(netconf_reply)
