from scapy.all import sr1, IP, ICMP
import csv
from datetime import datetime

routeurs = [
    {"ip": "192.168.1.1", "nom": "R1"},
    {"ip": "192.168.2.1", "nom": "R2"},
    # Ajoute R3 à R6
]

def collecter_tests():
    with open("metriques_fusionnees.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for r in routeurs:
            try:
                rtt = "-"
                pkt = IP(dst=r["ip"])/ICMP()
                rep = sr1(pkt, timeout=1, verbose=0)
                if rep:
                    rtt = f"{(rep.time - pkt.sent_time)*1000:.2f} ms"
                writer.writerow([
                    datetime.now(), r["nom"], "Scapy",
                    "-", "-", "-", f"RTT: {rtt}"
                ])
            except Exception as e:
                print(f"[Erreur Scapy] {r['nom']} : {e}")

if __name__ == "__main__":
    collecter_tests()
