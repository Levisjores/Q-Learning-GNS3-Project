
import time
from algorithmes.q_learning import QLearningRouter
import paramiko

# Définition du graphe réseau avec latences (valeurs fictives à adapter dynamiquement)
graph = {
    'A': {'B': 10, 'C': 15},
    'B': {'C': 5, 'D': 20},
    'C': {'D': 10, 'E': 25},
    'D': {'E': 5}
}

# Initialisation de l'agent IA
agent = QLearningRouter(graph, episodes=500)
agent.learn(goal='E')
chemin = agent.get_best_path('A', 'E')
print("🧠 Chemin optimal IA (Q-learning) :", " → ".join(chemin))

# Fonction pour appliquer le routage sur un routeur distant via SSH
def appliquer_routage_par_ssh(hote, utilisateur, mot_de_passe, route_cible, passerelle, systeme='cisco'):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hote, username=utilisateur, password=mot_de_passe, look_for_keys=False)
    shell = client.invoke_shell()

    if systeme == 'cisco':
        commandes = [
            "enable",
            mot_de_passe,  # enable password
            "conf t",
            f"ip route {route_cible} {passerelle}",
            "end",
            "write"
        ]
    elif systeme == 'linux':
        commandes = [
            "sudo vtysh",
            "conf t",
            f"ip route {route_cible} {passerelle}",
            "end",
            "write"
        ]
    for cmd in commandes:
        shell.send(cmd + "\n")
        time.sleep(1)
    print("✅ Routage appliqué via SSH à", hote)
    client.close()

# Exemple : appliquer la route de A vers E via B sur un routeur Cisco
appliquer_routage_par_ssh(
    hote="192.168.10.1",
    utilisateur="cisco",
    mot_de_passe="cisco",
    route_cible="192.168.30.0 255.255.255.0",
    passerelle="192.168.10.2",
    systeme="cisco"
)

# Pour routeur Linux FRRouting, changez les paramètres :
# appliquer_routage_par_ssh(
#     hote="192.168.10.3",
#     utilisateur="gns3",
#     mot_de_passe="gns3",
#     route_cible="192.168.30.0/24",
#     passerelle="192.168.10.2",
#     systeme="linux"
# )
