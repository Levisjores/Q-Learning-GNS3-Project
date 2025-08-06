
import subprocess
import re

def mesurer_latence(ip_dest):
    try:
        output = subprocess.check_output(["ping", "-c", "1", "-w", "1", ip_dest], stderr=subprocess.DEVNULL).decode()
        match = re.search(r'time=(\d+\.\d+)', output)
        if match:
            return float(match.group(1))
        else:
            return 999.0  # si pas de réponse
    except Exception:
        return 999.0

# Exemple : print(mesurer_latence("192.168.10.2"))
