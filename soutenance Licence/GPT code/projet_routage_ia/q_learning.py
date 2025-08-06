# Implémentation de Q-Learning

# q_learning.py

import numpy as np

class QLearning:
    def __init__(self, etats, alpha=0.7, gamma=0.8):
        self.etats = etats
        self.alpha = alpha  # taux d'apprentissage
        self.gamma = gamma  # facteur de réduction
        self.nb_etats = len(etats)
        self.index = {etat: i for i, etat in enumerate(etats)}
        self.reverse_index = {i: etat for etat, i in self.index.items()}
        self.Q = np.zeros((self.nb_etats, self.nb_etats))

    def apprendre(self, transitions, epochs=500):
        """
        transitions : liste de tuples (etat_src, etat_dst, poids)
        """
        for _ in range(epochs):
            for src, dst, poids in transitions:
                i = self.index[src]
                j = self.index[dst]
                r = self.calculer_recompense(poids)
                max_q = np.max(self.Q[j])
                self.Q[i, j] += self.alpha * (r + self.gamma * max_q - self.Q[i, j])

    def calculer_recompense(self, poids):
        return max(1, 100 - poids)  # récompense inverse du coût

    def chemin_optimal(self, source, destination):
        chemin = [source]
        courant = source
        while courant != destination:
            i = self.index[courant]
            j = np.argmax(self.Q[i])
            suivant = self.reverse_index[j]
            if suivant in chemin:
                break
            chemin.append(suivant)
            courant = suivant
        return chemin

    def get_q_table(self):
        return self.Q

    def sauvegarder(self, q_path="q_table.pkl", index_path="etat_index.pkl"):
        import pickle
        with open(q_path, "wb") as f:
            pickle.dump(self.Q, f)
        with open(index_path, "wb") as f:
            pickle.dump(self.index, f)

    def charger(self, q_path="q_table.pkl", index_path="etat_index.pkl"):
        import pickle
        with open(q_path, "rb") as f:
            self.Q = pickle.load(f)
        with open(index_path, "rb") as f:
            self.index = pickle.load(f)
            self.reverse_index = {i: etat for etat, i in self.index.items()}
