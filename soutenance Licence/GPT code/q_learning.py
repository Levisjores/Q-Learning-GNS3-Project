
import random

class QLearningRouter:
    def __init__(self, graphe, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.graphe = graphe
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}

    def apprendre(self, episodes=500):
        noeuds = list(self.graphe.nodes())
        for _ in range(episodes):
            etat = random.choice(noeuds)
            objectif = random.choice(noeuds)
            while objectif == etat:
                objectif = random.choice(noeuds)

            while etat != objectif:
                if etat not in self.q_table:
                    self.q_table[etat] = {}

                actions = list(self.graphe[etat])
                if random.uniform(0, 1) < self.epsilon:
                    action = random.choice(actions)
                else:
                    q_vals = {a: self.q_table[etat].get(a, 0) for a in actions}
                    action = max(q_vals, key=q_vals.get)

                reward = -self.graphe[etat][action].get('weight', 1)
                next_etat = action

                if next_etat not in self.q_table:
                    self.q_table[next_etat] = {}

                max_q_next = max([self.q_table[next_etat].get(a, 0) for a in self.graphe[next_etat]], default=0)
                old_q = self.q_table[etat].get(action, 0)
                self.q_table[etat][action] = old_q + self.alpha * (reward + self.gamma * max_q_next - old_q)

                etat = next_etat

    def meilleur_chemin(self, source, destination):
        chemin = [source]
        etat = source
        while etat != destination:
            if etat not in self.q_table or not self.q_table[etat]:
                break
            etat = max(self.q_table[etat], key=self.q_table[etat].get)
            chemin.append(etat)
            if len(chemin) > len(self.graphe.nodes()):
                break
        return chemin
