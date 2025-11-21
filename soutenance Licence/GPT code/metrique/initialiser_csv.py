import os
import csv

fichier = "metriques_fusionnees.csv"

def initialiser_csv():
    if not os.path.exists(fichier):
        with open(fichier, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date", "Routeur", "Méthode", "Input", "Output", "Input errors", "Autres"])
        print("✅ Fichier metriques_fusionnees.csv initialisé.")
    else:
        print("✅ Le fichier existe déjà.")

if __name__ == "__main__":
    initialiser_csv()
