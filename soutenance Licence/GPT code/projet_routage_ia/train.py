# Script pour entraîner le modèle Q-Learning


# train.py
"""
import pandas as pd
from q_learning import QLearning

# Chargement des métriques depuis le CSV
df = pd.read_csv("metriques.csv")

# Extraire tous les états (nœuds)
noeuds = sorted(set(df["src"]).union(df["dst"]))

# Construire les transitions (src, dst, poids)
transitions = [
    (row["src"], row["dst"], row["poids"])
    for _, row in df.iterrows()
]

# Créer une instance du modèle IA
ql = QLearning(etats=noeuds)

# Entraîner le modèle avec les transitions
ql.apprendre(transitions, epochs=500)

# Sauvegarder la Q-table et les index
ql.sauvegarder()

print("[✔] Entraînement terminé avec Q-learning. Fichiers q_table.pkl et etat_index.pkl sauvegardés.")
"""


"""
# train.py

import pandas as pd
import numpy as np
import pickle
import glob
import os

ALPHA = 0.8
GAMMA = 0.8
EPISODES = 5000

def charger_derniere_metrique():
    fichiers = glob.glob("metriques_*.csv")
    if not fichiers:
        raise FileNotFoundError("Aucun fichier metriques_*.csv trouvé.")
    return max(fichiers, key=os.path.getctime)

def charger_donnees():
    fichier = charger_derniere_metrique()
    print(f"[📥] Chargement des métriques : {fichier}")
    df = pd.read_csv(fichier)

    noeuds = sorted(set(df["src"]).union(df["dst"]))
    etat_index = {nom: i for i, nom in enumerate(noeuds)}
    n = len(noeuds)

    R = np.full((n, n), -1.0)

    for _, row in df.iterrows():
        i = etat_index[row["src"]]
        j = etat_index[row["dst"]]
        reward = max(0, 100 - row["poids"])
        R[i][j] = reward
        R[j][i] = reward

    return R, etat_index

def entrainer_q_learning(R, episodes=EPISODES):
    n = R.shape[0]
    Q = np.zeros_like(R)

    for _ in range(episodes):
        etat = np.random.randint(0, n)
        while True:
            actions_possibles = np.where(R[etat] >= 0)[0]
            if len(actions_possibles) == 0:
                break
            action = np.random.choice(actions_possibles)
            Q[etat][action] = R[etat][action] + GAMMA * np.max(Q[action])
            if np.random.rand() < 0.2:
                break
            etat = action
    return Q

if __name__ == "__main__":
    R, etat_index = charger_donnees()
    Q = entrainer_q_learning(R)

    with open("q_table.pkl", "wb") as f:
        pickle.dump(Q, f)
    with open("etat_index.pkl", "wb") as f:
        pickle.dump(etat_index, f)

    print("[✅] Entraînement terminé. Q-table sauvegardée.")
"""


#la update


# train.py

import pandas as pd
import numpy as np
import networkx as nx
import pickle
import glob

def charger_csv_recent():
    fichiers = glob.glob("metriques_*.csv")
    if not fichiers:
        raise FileNotFoundError("Aucun fichier métrique trouvé.")
    fichiers.sort()
    return fichiers[-1]

def construire_graphe(df):
    G = nx.Graph()
    for _, ligne in df.iterrows():
        G.add_edge(ligne["src"], ligne["dst"], poids=ligne["poids"])
    return G

def q_learning(graph, episodes=1000, alpha=0.6, gamma=0.8, epsilon=0.2):
    noeuds = list(graph.nodes())
    n = len(noeuds)
    Q = np.zeros((n, n))
    etat_index = {etat: i for i, etat in enumerate(noeuds)}

    for episode in range(episodes):
        etat = np.random.choice(noeuds)
        i = etat_index[etat]

        while True:
            voisins = list(graph.neighbors(etat))
            if not voisins:
                break

            if np.random.rand() < epsilon:
                suivant = np.random.choice(voisins)
            else:
                suivant = max(voisins, key=lambda x: Q[i][etat_index[x]])

            j = etat_index[suivant]
            poids = graph[etat][suivant]["poids"]
            recompense = 1 / (poids + 1e-6)

            Q[i][j] = (1 - alpha) * Q[i][j] + alpha * (recompense + gamma * np.max(Q[j]))
            etat = suivant
            i = j

            if np.random.rand() < 0.1:
                break

    return Q, etat_index

if __name__ == "__main__":
    print("📥 Chargement du fichier métrique le plus récent...")
    nom_csv = charger_csv_recent()
    df = pd.read_csv(nom_csv)
    print(f"✅ Fichier chargé : {nom_csv}")

    print("🔄 Construction du graphe d’apprentissage...")
    G = construire_graphe(df)

    print("🎓 Entraînement du modèle Q-learning...")
    Q, etat_index = q_learning(G)

    with open("q_table.pkl", "wb") as f:
        pickle.dump(Q, f)
    with open("etat_index.pkl", "wb") as f:
        pickle.dump(etat_index, f)

    print("✅ Q-table et état index sauvegardés avec succès.")
