
# Définition statique de la topologie réseau (à adapter dynamiquement si besoin)

def charger_topologie():
    return {
        'A': {'B': 10, 'C': 15},
        'B': {'C': 5, 'D': 20},
        'C': {'D': 10, 'E': 25},
        'D': {'E': 5}
    }
