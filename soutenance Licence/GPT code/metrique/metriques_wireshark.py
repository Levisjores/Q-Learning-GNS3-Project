import pyshark
import csv
import os
from datetime import datetime

def analyser_pcap(fichier):
    try:
        cap = pyshark.FileCapture(fichier, only_summaries=True)
        total_packets = sum(1 for _ in cap)
        cap.close()
        return total_packets
    except Exception as e:
        print(f"Erreur avec {fichier} : {e}")
        return 0

def collecter_wireshark():
    dossier = "./pcap"  # Dossier contenant les .pcap
    with open("metriques_fusionnees.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for fichier in os.listdir(dossier):
            if fichier.endswith(".pcap"):
                nom = fichier.replace(".pcap", "")
                nb_paquets = analyser_pcap(os.path.join(dossier, fichier))
                writer.writerow([
                    datetime.now(), nom, "Wireshark",
                    f"{nb_paquets} paquets", "-", "-", "-"
                ])

if __name__ == "__main__":
    collecter_wireshark()
