#fonctions pour analyser les imputs pour ensuite pouvoir les traduire (a revoir)
# On définit un dictionnaire avec une commande simple : 'ligne'
commandes = {
    'ligne': [10, 20, 30, 40]  # Paramètres x1, y1, x2, y2 pour dessiner une ligne
}

def verifier_commande(commandes):
    for commande, params in commandes.items():
        try:
            # Si la commande est 'ligne', on vérifie que ses paramètres sont corrects
            if commande == 'ligne':
                if len(params) == 4 and all(isinstance(p, int) for p in params):
                    print(f"Commande '{commande}' exécutée avec succès avec les paramètres {params}.")
                else:
                    raise ValueError(f"Les paramètres de la commande '{commande}' sont incorrects : {params}")
        except ValueError as e:
            print(f"Erreur : {e}")

# Appel de la fonction
verifier_commande(commandes)



# Dictionnaire de commandes avec les paramètres pour dessiner un triangle
commandes = {
    'triangle': [10, 20, 30, 40, 50, 60]  # Coordonnées x1, y1, x2, y2, x3, y3
}

# Fonction pour vérifier les commandes et leurs paramètres
def verifier_commande(commandes):
    for key, value in commandes.items():
        try:
            # Vérification pour une commande 'triangle'
            if key == 'triangle':
                if (
                    len(value) == 6 and # len compte le nombre d'élément
                    all(isinstance(p, int) for p in value) and # la commande all vérifie dans un premier instant que chaque élément sont des entiers
                    all(p >= 0 for p in value) # la commande all vérifie que tous les éléments soit positif ou nul 
                ):
                    print(f"Commande '{key}' exécutée avec succès avec les paramètres {value}.")
                else:
                    raise ValueError(f"Les paramètres de la commande '{key}' sont incorrects : {value}")
        except ValueError as e:
            print(f"Erreur : {e}")

# Appel de la fonction pour vérifier la commande triangle
verifier_commande(commandes)

