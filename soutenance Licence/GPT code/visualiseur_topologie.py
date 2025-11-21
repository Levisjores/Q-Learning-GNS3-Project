# visualiseur.py

import networkx as nx
import matplotlib.pyplot as plt

def afficher_topologie(chemin, couts):
    # Création du graphe
    G = nx.Graph()

    # Définir les noeuds (routeurs)
    routeurs = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
    G.add_nodes_from(routeurs)

    # Définir les liens avec les poids (latence, coûts...)
    liens = [
        ('R1', 'R6', couts.get(('R1', 'R6'), 1)),
        ('R1', 'R2', couts.get(('R1', 'R2'), 1)),
        ('R2', 'R6', couts.get(('R2', 'R6'), 1)),
        ('R2', 'R3', couts.get(('R2', 'R3'), 1)),
        ('R2', 'R4', couts.get(('R2', 'R4'), 1)),
        ('R2', 'R5', couts.get(('R2', 'R5'), 1)),
        ('R3', 'R4', couts.get(('R3', 'R4'), 1)),
        ('R4', 'R5', couts.get(('R4', 'R5'), 1)),
    ]

    G.add_weighted_edges_from(liens)

    # Positionnement automatique
    pos = nx.spring_layout(G, seed=42)

    # Affichage des noeuds et liens
    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)

    # Chemin sélectionné par l'IA
    chemin_edges = [(chemin[i], chemin[i+1]) for i in range(len(chemin)-1)]
    nx.draw_networkx_edges(G, pos, edgelist=chemin_edges, width=3, edge_color='red')

    # Poids sur les liens
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("Topologie réseau - Chemin optimal")
    plt.show()
