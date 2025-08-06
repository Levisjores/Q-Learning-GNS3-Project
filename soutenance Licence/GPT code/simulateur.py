
import networkx as nx
from data.topologie import charger_topologie
from learning.q_learning import QLearningRouter
from ssh.ssh_client import appliquer_routage

# Charger la topologie GNS3
graphe = nx.Graph()
topologie = charger_topologie()
for src, voisins in topologie.items():
    for dst, poids in voisins.items():
        graphe.add_edge(src, dst, weight=poids)

# Initialiser l'agent Q-learning
agent = QLearningRouter(graphe)

# Apprentissage
agent.apprendre(episodes=1000)

# Extraire le meilleur chemin entre R1 et R5 par exemple
chemin = agent.meilleur_chemin('R1', 'R5')
print("Meilleur chemin de R1 à R5 :", chemin)

# Appliquer le routage sur les routeurs via SSH (exemple avec R1)
appliquer_routage('R1', chemin)
