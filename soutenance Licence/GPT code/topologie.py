
# Topologie GNS3 de la soutenance

def charger_topologie():
    return {
        'R1': {'R6': 1, 'R2': 1},
        'R2': {'R1': 1, 'R6': 1, 'R3': 1, 'R4': 1, 'R5': 1},
        'R3': {'R2': 1, 'R4': 1},
        'R4': {'R2': 1, 'R3': 1, 'R5': 1},
        'R5': {'R2': 1, 'R4': 1},
        'R6': {'R1': 1, 'R2': 1}
    }
