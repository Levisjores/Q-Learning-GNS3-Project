from netmiko import ConnectHandler
from pysnmp.hlapi import *

class NetworkManager:
    def __init__(self, router_ip):
        self.router = {
            'device_type': 'cisco_ios',
            'host': router_ip,
            'username': 'admin',
            'password': 'cisco123'
        }
    
    def update_route(self, destination, next_hop):
        commands = [
            f"ip route {destination} 255.255.255.0 {next_hop}",
            "end"
        ]
        self._send_commands(commands)

    def _send_commands(self, cmds):
        try:
            with ConnectHandler(**self.router) as conn:
                for cmd in cmds:
                    conn.send_command(cmd)
        except Exception as e:
            print(f"Erreur SSH: {e}")