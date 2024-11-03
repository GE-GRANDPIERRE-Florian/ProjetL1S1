from Modules.colours import BallColours

COLOURS: tuple = (
            BallColours("#ff4a4a", "#c80000", "Rouge", True),
            BallColours("#ffbd4a", "#e69200", "Orange", False),
            BallColours("#8fff4a", "#34d500", "Vert", False),
            BallColours("#4afffa", "#00b6b6", "Bleu", False),
            BallColours("#a54aff", "#5300b6", "Violet", False),
            BallColours("#ff4ae6", "#b600b3", "Rose", False)
            )
# On récupère les lignes
texte_regle = []
with open("Ressources/Regles.txt", "r", encoding="utf-8") as f:
    for ligne in f:
        texte_regle.append(ligne)

# On récupère les lignes
texte_historique = []
with open("Ressources/Historique.txt", "r", encoding="utf-8") as f:
    for ligne in f:
        texte_historique.append(ligne)

DOES_SLIDER_LOOP : bool = False