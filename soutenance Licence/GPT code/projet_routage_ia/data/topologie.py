# Définition de la topologie GNS3

# data/topologie.py

# Définition des noeuds (routeurs et PCs)
NOEUDS = [
    "R1", "R2", "R3", "R4", "R5", "R6",
    "PC1", "PC3", "PC4", "PC5", "PC6"
]

# Connexions physiques selon ta configuration (interface série et f0/0)
LIENS = [
    ("R1", "R6"),  # S1/0 <-> S1/0
    ("R1", "R2"),  # S1/1 <-> S1/1
    ("R2", "R6"),  # S2/0 <-> S2/0
    ("R2", "R3"),  # S1/2 <-> S1/2
    ("R2", "R4"),  # S1/4 <-> S1/4
    ("R2", "R5"),  # S1/3 <-> S1/3
    ("R3", "R4"),  # S1/1 <-> S1/1
    ("R4", "R5"),  # S1/0 <-> S1/0

    # Connexions aux PCs
    ("R1", "PC1"),  # R1 f0/0 <-> switch <-> PC1
    ("R3", "PC3"),  # R3 f0/0 <-> switch <-> PC3
    ("R4", "PC4"),  # R4 f0/0 <-> switch <-> PC4
    ("R5", "PC5"),  # R5 f0/0 <-> switch <-> PC5
    ("R6", "PC6"),  # R6 f0/0 <-> switch <-> PC6
]

# Liste des IPs pour chaque routeur (f0/0)
ROUTEUR_IPS = {
    "R1": "192.168.1.1",
    "R2": "192.168.2.1",  # non connecté à un PC
    "R3": "192.168.3.1",
    "R4": "192.168.4.1",
    "R5": "192.168.5.1",
    "R6": "192.168.6.1",
}

# Liste des IPs des PCs connectés aux routeurs
PC_IPS = {
    "PC1": "192.168.1.3",
    "PC3": "192.168.3.3",
    "PC4": "192.168.4.3",
    "PC5": "192.168.5.3",
    "PC6": "192.168.6.3",
}
