# main.py

import subprocess
import os
import pickle
import pandas as pd
import numpy as np
import time
import glob

def lancer_script(nom_fichier):
    if os.name == 'nt':
        subprocess.run(["python", nom_fichier])
    else:
        subprocess.run(["python3", nom_fichier])

def charger_q_table():
    with open("q_table.pkl", "rb") as f:
        Q = pickle.load(f)
    with open("etat_index.pkl", "rb") as f:
        etat_index = pickle.load(f)
    index_etat = {v: k for k, v in etat_index.items()}
    return Q, etat_index, index_etat

def chemin_optimal(Q, etat_index, source, destination):
    i = etat_index[source]
    j = etat_index[destination]
    chemin = [i]
    while i != j:
        i = Q[i].argmax()
        if i in chemin:
            break
        chemin.append(i)
    return [k for k in [index_etat[x] for x in chemin]]

def reset_donnees():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dossier_backup = f"backup_{timestamp}"
    os.makedirs(dossier_backup, exist_ok=True)

    fichiers = glob.glob("metriques_*.csv") + ["q_table.pkl", "etat_index.pkl"]

    fichiers_trouves = False

    for fichier in fichiers:
        if os.path.exists(fichier):
            fichiers_trouves = True
            nom_backup = os.path.join(dossier_backup, fichier)
            shutil.move(fichier, nom_backup)
            print(f"📁 Sauvegardé dans {nom_backup}")

    if fichiers_trouves:
        print(f"✅ Données sauvegardées dans le dossier : {dossier_backup}")
    else:
        print("📭 Aucun fichier à sauvegarder.")

def menu():
    while True:
        print("\n🧠 MENU PRINCIPAL - Routage Intelligent IA\n")
        print("1️⃣  Lancer la collecte avancée des métriques")
        print("2️⃣  Entraîner le modèle Q-learning")
        print("3️⃣  Visualiser le graphe avec métriques")
        print("4️⃣  Tester un chemin optimal (source → destination)")
        print("5️⃣  Quitter")
        print("6️⃣  🔁 Réinitialiser les données (CSV + Q-table)\n")

        choix = input("👉 Choisis une option (1 à 6) : ").strip()

        if choix == "1":
            lancer_script("metriques.py")
        elif choix == "2":
            lancer_script("train.py")
        elif choix == "3":
            lancer_script("visualisation.py")
        elif choix == "4":
            try:
                Q, etat_index, index_etat = charger_q_table()
                noeuds = list(etat_index.keys())
                print(f"🔗 Noeuds disponibles : {', '.join(noeuds)}")
                src = input("🌐 Source : ").strip()
                dst = input("🎯 Destination : ").strip()

                if src not in etat_index or dst not in etat_index:
                    print("❌ Noeud invalide.")
                    continue

                chemin = chemin_optimal(Q, etat_index, src, dst)
                print(f"✅ Chemin optimal : {' ➡️ '.join(chemin)}")
            except FileNotFoundError:
                print("❌ Q-table non trouvée. Lance l’entraînement d’abord (option 2).")
        elif choix == "5":
            print("👋 Fin du programme.")
            break
        elif choix == "6":
            reset_donnees()
        else:
            print("❌ Choix invalide.")

if __name__ == "__main__":
    menu()
