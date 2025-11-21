import numpy as np
import json
from collections import defaultdict

class QLearningAgent:
    def __init__(self, topology_file="config/topology.json"):
        with open(topology_file) as f:
            self.topology = json.load(f)
        self.q_table = defaultdict(lambda: np.zeros(len(self.topology["routers"])))
        
    def choose_route(self, source, destination):
        possible_routes = self._get_routes(source, destination)
        state = hash((source, destination))
        action = np.argmax(self.q_table[state])
        return possible_routes[action]

    def _get_routes(self, src, dst):
        # Implémentez BFS/DFS pour générer tous les chemins possibles
        pass