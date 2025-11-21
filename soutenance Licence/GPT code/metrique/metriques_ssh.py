import paramiko
import csv
from datetime import datetime

# Liste des routeurs à interroger
routeurs = [
    {"host": "192.168.1.1", "username": "admin", "password": "cisco", "nom": "R1"},
    {"host": "192.168.2.1", "username": "admin", "password": "cisco", "nom": "R2"},
    # Ajoute R3 à R6 ici...
]

def extraire_stats(show_output):
    lines = show_output.splitlines()
    stats = {
        "input_rate": None,
        "output_rate": None,
        "input_errors": None,
        "output_errors": None
    }
    for line in lines:
        if "input rate" in line:
            stats["input_rate"] = line.strip()
        elif "output rate" in line:
            stats["output_rate"] = line.strip()
        elif "input errors" in line:
            stats["input_errors"] = line.strip()
        elif "output errors" in line:
            stats["output_errors"] = line.strip()
    return stats

def collecter_ssh():
    with open("metriques_fusionnees.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for r in routeurs:
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(r["host"], username=r["username"], password=r["password"])
                stdin, stdout, stderr = client.exec_command("show interfaces")
                sortie = stdout.read().decode()
                stats = extraire_stats(sortie)
                writer.writerow([
                    datetime.now(), r["nom"], "SSH",
                    stats["input_rate"], stats["output_rate"],
                    stats["input_errors"], stats["output_errors"]
                ])
                client.close()
            except Exception as e:
                print(f"[Erreur SSH] {r['nom']} : {e}")

if __name__ == "__main__":
    collecter_ssh()
