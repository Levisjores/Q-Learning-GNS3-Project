# metriques.py
"""
import subprocess
import random
import pandas as pd
import time

# IPs de tous les équipements
ROUTEUR_IPS = {
    "R1": "192.168.1.1",
    "R2": "192.168.2.1",
    "R3": "192.168.3.1",
    "R4": "192.168.4.1",
    "R5": "192.168.5.1",
    "R6": "192.168.6.1"
}

PC_IPS = {
    "PC1": "192.168.1.2",
    "PC3": "192.168.3.2",
    "PC4": "192.168.4.2",
    "PC5": "192.168.5.2",
    "PC6": "192.168.6.2"
}

ips = ROUTEUR_IPS.copy()
ips.update(PC_IPS)

def mesure_latence(ip):
    try:
        result = subprocess.check_output(
            ["ping", "-c", "5", ip],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=10
        )
        for line in result.splitlines():
            if "avg" in line or "mdev" in line:
                parts = line.split("=")[-1].strip().split("/")
                return float(parts[1])  # moyenne
    except Exception as e:
        print(f"[x] Erreur ping vers {ip} : {e}")
    return random.uniform(20, 100)

def mesure_perte(ip):
    try:
        result = subprocess.check_output(
            ["ping", "-c", "5", ip],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=10
        )
        for line in result.splitlines():
            if "packet loss" in line:
                parts = line.split(",")
                loss = parts[2].strip().split("%")[0]
                return float(loss)
    except Exception as e:
        print(f"[x] Erreur perte vers {ip} : {e}")
    return random.uniform(0, 20)

def mesure_bande_passante(ip):
    try:
        result = subprocess.check_output(
            ["iperf3", "-c", ip, "-p", "5201", "-t", "5"],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=10
        )
        for line in result.splitlines():
            if "receiver" in line and "Mbits/sec" in line:
                return float(line.split()[-2])
        return random.uniform(1, 10)
    except subprocess.CalledProcessError:
        print(f"[!] iperf3 échoué vers {ip} (pas de serveur ?)")
        return random.uniform(2, 5)
    except Exception as e:
        print(f"[!] Erreur iperf3 vers {ip} : {e}")
        return random.uniform(1, 3)

def collecter_metriques():
    done = set()
    data = []

    for u, ip_u in ips.items():
        for v, ip_v in ips.items():
            if u == v:
                continue
            if (u, v) in done or (v, u) in done:
                continue

            print(f"[📡] Mesure {u} ↔ {v} ...")

            lat = mesure_latence(ip_v)
            perte = mesure_perte(ip_v)
            bp = mesure_bande_passante(ip_v)

            # calcul du coût/poids
            poids = lat + (perte * 2) + (100 / bp if bp > 0 else 100)

            data.append({
                "src": u,
                "dst": v,
                "latence": round(lat, 2),
                "perte": round(perte, 2),
                "bande_passante": round(bp, 2),
                "poids": round(poids, 2)
            })

            done.add((u, v))

    return data

if __name__ == "__main__":
    print("🔍 Début de la collecte de métriques réseau...")
    start = time.time()

    data = collecter_metriques()
    df = pd.DataFrame(data)
    df.to_csv("metriques.csv", index=False)

    print(f"[✔] {len(data)} métriques enregistrées dans metriques.csv")
    print(f"[⏱] Durée : {round(time.time() - start, 2)} secondes")
"""



# metriques.py
"""
import subprocess
import random
import pandas as pd
import time
import datetime

ROUTEUR_IPS = {
    "R1": "192.168.1.1",
    "R2": "192.168.2.1",
    "R3": "192.168.3.1",
    "R4": "192.168.4.1",
    "R5": "192.168.5.1",
    "R6": "192.168.6.1"
}

PC_IPS = {
    "PC1": "192.168.1.3",
    "PC3": "192.168.3.3",
    "PC4": "192.168.4.3",
    "PC5": "192.168.5.3",
    "PC6": "192.168.6.3"
}

ips = ROUTEUR_IPS.copy()
ips.update(PC_IPS)

def mesure_ping(ip):
    try:
        result = subprocess.check_output(
            ["ping", "-c", "5", ip],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=10
        )
        lines = result.splitlines()
        rtt_line = [line for line in lines if "rtt" in line or "avg" in line][-1]
        stats = rtt_line.split("=")[1].split("/")

        latence = float(stats[1])
        stddev = float(stats[2]) if len(stats) >= 3 else 0.0

        perte_line = [line for line in lines if "packet loss" in line][0]
        perte = float(perte_line.split(",")[2].strip().split("%")[0])

        return latence, perte, stddev
    except Exception as e:
        print(f"[x] Erreur ping {ip} : {e}")
        return random.uniform(20, 100), random.uniform(0, 10), random.uniform(1, 10)

def mesure_bande_passante(ip):
    try:
        result = subprocess.check_output(
            ["iperf3", "-c", ip, "-p", "5201", "-t", "5"],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=10
        )
        for line in result.splitlines():
            if "receiver" in line and "Mbits/sec" in line:
                return float(line.split()[-2])
        return random.uniform(1, 10)
    except Exception as e:
        print(f"[!] iperf3 échoué vers {ip} : {e}")
        return random.uniform(2, 5)

def mesure_hops(ip):
    try:
        result = subprocess.check_output(
            ["traceroute", "-m", "10", ip],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=15
        )
        lines = result.strip().splitlines()
        for i, line in enumerate(lines[1:], start=1):  # skip 1st line (host)
            if ip in line:
                return i
        return len(lines)  # fallback
    except Exception as e:
        print(f"[x] traceroute échoué vers {ip} : {e}")
        return random.randint(1, 5)

def collecter_metriques():
    done = set()
    data = []

    for u, ip_u in ips.items():
        for v, ip_v in ips.items():
            if u == v or (u, v) in done or (v, u) in done:
                continue

            print(f"[📡] Mesure {u} ↔ {v} ...")

            latence, perte, congestion = mesure_ping(ip_v)
            bande_passante = mesure_bande_passante(ip_v)
            hops = mesure_hops(ip_v)
            goulot = 10 if bande_passante < 3 else 0

            poids = (
                latence +
                (perte * 2) +
                (hops * 5) +
                (congestion * 1.5) +
                (100 / bande_passante if bande_passante > 0 else 100) +
                goulot
            )

            data.append({
                "src": u,
                "dst": v,
                "latence": round(latence, 2),
                "perte": round(perte, 2),
                "congestion": round(congestion, 2),
                "hops": hops,
                "bande_passante": round(bande_passante, 2),
                "goulot": goulot > 0,
                "poids": round(poids, 2)
            })

            done.add((u, v))

    return data

if __name__ == "__main__":
    print("🔍 Début de la collecte avancée...")
    start = time.time()

    data = collecter_metriques()
    df = pd.DataFrame(data)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    df.to_csv(f"metriques_{timestamp}.csv", index=False)

    print(f"[✔] {len(data)} liens enregistrés.")
    print(f"[⏱] Durée : {round(time.time() - start, 2)} secondes")
"""


#la update

# metriques.py

import subprocess
import pandas as pd
import time
import datetime
import random
import glob
import os

# Liens entre routeurs (interfaces point-à-point)
LIENS_ROUTEURS = [
    ("R1", "R6", "10.0.1.1", "10.0.1.2"),
    ("R1", "R2", "10.0.2.1", "10.0.2.2"),
    ("R2", "R6", "10.0.3.1", "10.0.3.2"),
    ("R2", "R3", "10.0.4.1", "10.0.4.2"),
    ("R2", "R4", "10.0.5.1", "10.0.5.2"),
    ("R2", "R5", "10.0.6.1", "10.0.6.2"),
    ("R3", "R4", "10.0.7.1", "10.0.7.2"),
    ("R4", "R5", "10.0.8.1", "10.0.8.2"),
]

# IP classiques pour les PC et routeurs
ips = {
    "PC1": "192.168.1.2",
    "R1": "192.168.1.1",
    "PC3": "192.168.3.2",
    "R3": "192.168.3.1",
    "PC4": "192.168.4.2",
    "R4": "192.168.4.1",
    "PC5": "192.168.5.2",
    "R5": "192.168.5.1",
    "PC6": "192.168.6.2",
    "R6": "192.168.6.1"
}

def mesure_ping(ip):
    try:
        result = subprocess.check_output(
            ["ping", "-c", "5", ip],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=10
        )
        lines = result.splitlines()
        rtt_line = [line for line in lines if "rtt" in line][-1]
        stats = rtt_line.split("=")[1].split("/")

        latence = float(stats[1])
        stddev = float(stats[2]) if len(stats) >= 3 else 0.0

        perte_line = [line for line in lines if "packet loss" in line][0]
        perte = float(perte_line.split(",")[2].strip().split("%")[0])

        return latence, perte, stddev
    except Exception as e:
        print(f"[x] Erreur ping {ip} : {e}")
        return random.uniform(20, 100), random.uniform(0, 10), random.uniform(1, 10)

def mesure_bande_passante(ip):
    try:
        result = subprocess.check_output(
            ["iperf3", "-c", ip, "-p", "5201", "-t", "5"],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=10
        )
        for line in result.splitlines():
            if "receiver" in line and "Mbits/sec" in line:
                return float(line.split()[-2])
        return -1
    except Exception as e:
        print(f"[!] iperf3 non disponible vers {ip} : {e}")
        return -1

def mesure_hops(ip):
    try:
        result = subprocess.check_output(
            ["traceroute", "-m", "10", ip],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            timeout=15
        )
        lines = result.strip().splitlines()
        for i, line in enumerate(lines[1:], start=1):
            if ip in line:
                return i
        return len(lines)
    except Exception as e:
        print(f"[x] traceroute échoué vers {ip} : {e}")
        return random.randint(1, 5)

def calcul_poids(latence, perte, congestion, hops, bande_passante):
    goulot = 10 if bande_passante != -1 and bande_passante < 3 else 0
    poids = (
        latence +
        (perte * 2) +
        (hops * 5) +
        (congestion * 1.5) +
        ((100 / bande_passante) if bande_passante > 0 else 50) +  # pondération adaptable
        goulot
    )
    return round(poids, 2), goulot > 0

def collecter_metriques():
    done = set()
    data = []

    # Mesure des liens inter-routeurs
    for nom1, nom2, ip1, ip2 in LIENS_ROUTEURS:
        if (nom1, nom2) in done or (nom2, nom1) in done:
            continue
        print(f"[🔁] Mesure lien routeur : {nom1} ↔ {nom2}")
        latence, perte, congestion = mesure_ping(ip2)
        bande_passante = -1  # Non mesurable sur routeurs
        hops = mesure_hops(ip2)
        poids, goulot = calcul_poids(latence, perte, congestion, hops, bande_passante)

        data.append({
            "src": nom1,
            "dst": nom2,
            "latence": round(latence, 2),
            "perte": round(perte, 2),
            "congestion": round(congestion, 2),
            "hops": hops,
            "bande_passante": bande_passante,
            "goulot": goulot,
            "poids": poids
        })
        done.add((nom1, nom2))

    # Mesure des IPs classiques (routeur ↔ PC, PC ↔ PC)
    for u, ip_u in ips.items():
        for v, ip_v in ips.items():
            if u == v or (u, v) in done or (v, u) in done:
                continue

            print(f"[🔗] Mesure standard : {u} ↔ {v}")

            latence, perte, congestion = mesure_ping(ip_v)
            bande_passante = mesure_bande_passante(ip_v)
            hops = mesure_hops(ip_v)
            poids, goulot = calcul_poids(latence, perte, congestion, hops, bande_passante)

            data.append({
                "src": u,
                "dst": v,
                "latence": round(latence, 2),
                "perte": round(perte, 2),
                "congestion": round(congestion, 2),
                "hops": hops,
                "bande_passante": round(bande_passante, 2) if bande_passante != -1 else -1,
                "goulot": goulot,
                "poids": poids
            })

            done.add((u, v))

    return data

if __name__ == "__main__":
    print("🚀 Début de la collecte des métriques (adaptée aux routeurs Cisco)...")
    start = time.time()
    data = collecter_metriques()
    df = pd.DataFrame(data)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    df.to_csv(f"metriques_{timestamp}.csv", index=False)
    print(f"[✅] {len(data)} liens mesurés et enregistrés.")
    print(f"[⏱️] Temps total : {round(time.time() - start, 2)} sec")
