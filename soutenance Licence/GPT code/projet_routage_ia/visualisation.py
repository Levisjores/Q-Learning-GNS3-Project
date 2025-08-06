# Script pour afficher le chemin choisi sur un graphe
# visualisation.py
"""
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from data.topologie import LIENS

# Chargement des métriques
df = pd.read_csv("metriques.csv")

# Création dictionnaires enrichis : (src, dst) → latence, perte, poids
infos_liens = {}
for _, row in df.iterrows():
    src, dst = row["src"], row["dst"]
    infos_liens[(src, dst)] = {
        "latence": round(row["latence"], 2),
        "perte": round(row["perte"], 2),
        "poids": round(row["poids"], 2)
    }
    infos_liens[(dst, src)] = infos_liens[(src, dst)]  # liens symétriques

# Chargement du modèle IA
with open("q_table.pkl", "rb") as f:
    Q = pickle.load(f)

with open("etat_index.pkl", "rb") as f:
    etat_index = pickle.load(f)
index_etat = {v: k for k, v in etat_index.items()}

# Chemin optimal
def chemin_q_learning(source, destination):
    chemin = [source]
    courant = source
    while courant != destination:
        idx = etat_index[courant]
        suivant_idx = Q[idx].argmax()
        suivant = index_etat[suivant_idx]
        if suivant in chemin:
            break
        chemin.append(suivant)
        courant = suivant
    return chemin

# Génération du graphe
def afficher_graphique(src, dst, chemin):
    G = nx.Graph()

    for u, v in LIENS:
        data = infos_liens.get((u, v), {"latence": 0, "perte": 0, "poids": 1})
        G.add_edge(u, v, **data)

    pos = nx.spring_layout(G, seed=42)
    arêtes_optimales = list(zip(chemin, chemin[1:]))

    # Création de labels riches : latence | perte | poids
    labels = {}
    for u, v in G.edges():
        info = G[u][v]
        lat = info.get("latence", 0)
        per = info.get("perte", 0)
        w = info.get("poids", 1)
        labels[(u, v)] = f"{lat}ms | {per}% | w={w}"
        simulé = "🛜" if "PC" not in u and "PC" not in v else ""
        labels[(u, v)] = f"{lat}ms | {per}% | w={w} {simulé}"


    plt.figure(figsize=(11, 7))
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1500, font_weight="bold")
    nx.draw_networkx_edges(G, pos, edgelist=arêtes_optimales, edge_color="red", width=3)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

    plt.title(f"🧠 Chemin IA optimal : {src} ➝ {dst}")
    plt.tight_layout()
    
    # Sauvegarde de l’image PNG
    nom_fichier = f"graph_{src}_to_{dst}.png".lower()
    plt.savefig(nom_fichier)
    print(f"[📸] Graphe sauvegardé dans le fichier : {nom_fichier}")
    
    plt.show()

# Interface utilisateur CLI
def main():
    noeuds = list(etat_index.keys())
    print("🧠 Routeurs/PC disponibles :", ", ".join(noeuds))
    src = input("👉 Source : ").strip().upper()
    dst = input("🎯 Destination : ").strip().upper()

    if src not in etat_index or dst not in etat_index:
        print("❌ Source ou destination invalide.")
        return

    chemin = chemin_q_learning(src, dst)
    print(f"✅ Chemin trouvé : {' ➝ '.join(chemin)}")
    afficher_graphique(src, dst, chemin)

if __name__ == "__main__":
    main()
!
"""







# visualisation.py

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import pickle
import glob
import os

def charger_derniere_metrique():
    fichiers = glob.glob("metriques_*.csv")
    if not fichiers:
        raise FileNotFoundError("Aucun fichier metriques_*.csv trouvé.")
    return max(fichiers, key=os.path.getctime)

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
    return chemin

def visualiser():
    df = pd.read_csv(charger_derniere_metrique())
    Q, etat_index, index_etat = charger_q_table()

    G = nx.Graph()
    for noeud in etat_index:
        G.add_node(noeud)

    for _, row in df.iterrows():
        src = row["src"]
        dst = row["dst"]
        label = (
            f"lat:{row['latence']}ms\n"
            f"perte:{row['perte']}%\n"
            f"hop:{row['hops']}\n"
            f"cong:{row['congestion']}\n"
            f"bp:{row['bande_passante']}Mbps"
        )
        G.add_edge(src, dst, weight=row["poids"], label=label)

    pos = nx.spring_layout(G, seed=42)
    weights = nx.get_edge_attributes(G, 'weight')
    labels = nx.get_edge_attributes(G, 'label')

    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1200, font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=7)

    plt.title("🛰️ Routage IA - Visualisation du Graphe avec Métriques")
    plt.tight_layout()
    plt.savefig("graphe_ia.png", dpi=300)
    print("[📸] Graphe sauvegardé : graphe_ia.png")
    plt.show()

if __name__ == "__main__":
    visualiser()
