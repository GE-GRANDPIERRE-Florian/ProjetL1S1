#from Modules.PopupMenu import Inter_menu
#from Modules.PlayerSelectScreen import *
#import doctest
import Modules.Dependencies.fltk as fltk
import Modules.GameConstant as GC
import doctest


class Joueurs:
    """
    Class qui détermine les joueurs
    """

    def __init__(self, numero_joueur, couleur, est_hote=False, est_bot=False):
        """
        Initialisation
        """
        self.numero_joueur = numero_joueur
        self.couleur = couleur
        if not est_bot:
            self.nom = "J" + str(numero_joueur)
        else:
            self.nom = "B" + str(numero_joueur)
        self.est_hote = est_hote
        self.est_bot = est_bot


class Bouton_menu:
    def __init__(self, x_1, y_1, x_2, y_2, texte_btn):
        """
        Constructeur de la classe Bouton
        """
        self.point_a = (x_1, y_1)
        self.point_b = (x_2, y_2)
        self.texte_btn = texte_btn

    def dessiner_rect(self, tag="affi_menu", remp="#eae8af",
                      epaisseur=5, taille=20):
        """
        Fonction qui dessine les boutons (rectangle)
        et rajoute le texte
        """
        fltk.rectangle(self.point_a[0], self.point_a[1],
                       self.point_b[0], self.point_b[1],
                       epaisseur=epaisseur, remplissage=remp,
                       tag=tag)
        milieu_x = (self.point_b[0] + self.point_a[0]) / 2
        milieu_y = (self.point_b[1] + self.point_a[1]) / 2

        fltk.texte(milieu_x, milieu_y + 8, self.texte_btn,
                   ancrage="center", taille=taille, tag=tag)

    def clic(self, position_x, position_y):
        """
        On vérifie si on a la souris sur le bouton
        """
        if self.point_a[0] < position_x < self.point_b[0]:
            if self.point_a[1] < position_y < self.point_b[1]:
                return True


class Inter_menu:
    """
    Class qui permet d'afficher les fenêtres dans le menu, comme le
    règlement, l'historique,..."""

    def __init__(self, nom, x1, y1, x2, y2, texte=""):
        """
        Initialisation
        """
        self.nom = nom
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.texte = texte

    def dessiner_inter(self):
        """
        Méthode qui permet d'afficher la fenêtre

        OUTPUT:
            croix (objet)
        """
        fltk.rectangle(self.x1, self.y1, self.x2, self.y2,
                       epaisseur=5, remplissage="#ffe392", tag="Inter")
        fltk.ligne(self.x1 + 20, self.y1 + 80,
                   self.x2 - 20, self.y1 + 80, epaisseur=3, tag="Inter")

        milieu_x = (self.x1 + self.x2) / 2
        milieu_y = (2 * self.y1 + 80) / 2
        fltk.texte(milieu_x, milieu_y, self.nom,
                   ancrage="center", taille=20, tag="Inter")
        # On créer la croix
        croix = Bouton_menu(self.x2 - 40, self.y1 - 40,
                            self.x2 + 40, self.y1 + 40, "X")
        croix.dessiner_rect("Inter", "#ff3d3d")
        # On écrit le texte si besoin
        if self.texte != "":
            for i in range(len(self.texte)):
                fltk.texte(540, 190 + 30 * (i + 1), self.texte[i], taille=10,
                           ancrage="center", tag="Sep")
        return croix


def separation_joueur():
    """
    FONCTION D'AFFICHAGE

    Fonction qui permet de faire les séparations entre les joueurs
    dans la fenêtre Jouer, c'est à dire les _| dans les coins

    INPUT:
        aucun

    OUTPUT:
        aucun
    """
    # Séparation des cases pour les joueurs (4 joueurs max)
    for i in range(4):
        j = 240 * i
        fltk.ligne(90 + j, 250, 150 + j, 250, epaisseur=4, tag="Sep")
        fltk.ligne(90 + j, 530, 150 + j, 530, epaisseur=4, tag="Sep")
        fltk.ligne(90 + j, 250, 90 + j, 310, epaisseur=4, tag="Sep")
        fltk.ligne(90 + j, 470, 90 + j, 530, epaisseur=4, tag="Sep")
        fltk.ligne(220 + j, 250, 280 + j, 250, epaisseur=4, tag="Sep")
        fltk.ligne(220 + j, 530, 280 + j, 530, epaisseur=4, tag="Sep")
        fltk.ligne(280 + j, 250, 280 + j, 310, epaisseur=4, tag="Sep")
        fltk.ligne(280 + j, 470, 280 + j, 530, epaisseur=4, tag="Sep")


def affiche_boules(centre_x, centre_y, rayon, c_primaire, c_secondaire):
    """
    FONCTION D'AFFICHAGE

    Fonction qui affiche les boules

    INPUT:
        centre_x (int)
        centre_y (int)
        rayon (int)
        c_primaire (str : hexadecimal)
        c_secondaire (str : hexadecimal)

    OUTPUT:
        aucun
    """
    # On affiche les balles
    k = rayon / 10
    fltk.cercle(centre_x, centre_y, rayon,
                remplissage=c_primaire, tag="Para_j")
    fltk.cercle(centre_x + 5 * k, centre_y - k * 4, rayon / 10,
                remplissage=c_secondaire, epaisseur=0, tag="Para_j")
    fltk.cercle(centre_x + 2 * k, centre_y - k * 3, rayon / 10,
                remplissage=c_secondaire, epaisseur=0, tag="Para_j")
    fltk.cercle(centre_x + 5 * k, centre_y - k, rayon / 10,
                remplissage=c_secondaire, epaisseur=0, tag="Para_j")


def change_valeur(ch_valeur, valeur_possible):
    """
    Fonction qui permet de prendre la valeur qui est après dans la liste

    INPUT:
        ch_valeur (str ou int)
        valeur_possible (liste (str  ou int))

    OUTPUT:
        ch_valeur (str ou int)
    ----------------------- DOCTEST -----------------------
    # Les tailles de fenetres
    >>> change_valeur("780x580", ["780x580", "920x680", "1080x720", "1280x920"])
    '920x680'

    >>> change_valeur("1080x720", ["780x580", "920x680", "1080x720", "1280x920"])
    '1280x920'

    >>> change_valeur("1280x920", ["780x580", "920x680", "1080x720", "1280x920"])
    '780x580'

    # Les tailles de grille
    >>> change_valeur(5, [5, 7, 9])
    7

    >>> change_valeur(7, [5, 7, 9])
    9

    >>> change_valeur(9, [5, 7, 9])
    5

    # Les nombres de billes
    >>> change_valeur(5, [3, 4, 5, 6, 7])
    6

    >>> change_valeur(7, [3, 4, 5, 6, 7])
    3

    >>> change_valeur(3, [3, 4, 5, 6, 7])
    4
    """
    id = valeur_possible.index(ch_valeur)
    ch_valeur = valeur_possible[(id + 1) % len(valeur_possible)]
    return ch_valeur


def affichage_joueurs(joueurs, taille_grille=5):
    """
    FONCTION AFFICHAGE + Boutons

    Fonction qui affiche les paramêtres des joueurs

    INPUT:
        joueurs (liste d'objets)
        taille_grille (int)
    OUTPUT:
        boutons_couleur (liste d'objets)
        boutons_autre (liste d'objets)
    """
    fltk.efface("Para_j")
    # Boutons pour les couleurs
    boutons_couleur = []
    # Boutons pour la grille et quitter
    boutons_autre = []
    # Choix de la grille
    fltk.texte(185, 470, "Taille grille:",
               ancrage="center", taille=8, tag="Para_j")
    texte_grille = str(taille_grille) + "x" + str(taille_grille)
    boutons_autre.append(Bouton_menu(110, 485, 260, 520, texte_grille))
    boutons_autre[0].dessiner_rect("Para_j", epaisseur=2, taille=10)
    for i in range(len(joueurs)):
        # On affiche le nom
        fltk.texte(185 + i * 240, 260, joueurs[i].nom, ancrage="center",
                   taille=15, tag="Para_j")
        # On créer le bouton pour la couleur
        boutons_couleur.append(Bouton_menu(110 + i * 240, 415,
                                           260 + i * 240, 450,
                                           joueurs[i].couleur.name))
        # On récupère les couleurs
        c_primaire = joueurs[i].couleur.primary_colour
        c_secondaire = joueurs[i].couleur.secondary_colour
        # On affiche les balles
        affiche_boules(185 + i * 240, 340, 50, c_primaire, c_secondaire)
        # On affiche les boutons
        boutons_couleur[i].dessiner_rect("Para_j", joueurs[i].couleur.primary_colour, 2, 10)
        if not joueurs[i].est_hote:
            boutons_autre.append(Bouton_menu(110 + i * 240, 485,
                                             260 + i * 240, 520, "Quitter"))
            boutons_autre[i].dessiner_rect("Para_j", epaisseur=2,
                                           taille=10, remp="white")
    if len(joueurs) > 1:
        Bouton_menu(340, 600, 740, 700, "Lancer").dessiner_rect("Lance", taille=25)
    else:
        fltk.efface("Lance")
    return boutons_couleur, boutons_autre


def changement_couleur(couleurs, ancienne_couleur=[]):
    """
    Fonction qui permet de vérifier si une couleur est déja choisi et
    change la couleur

    INPUT:
        couleurs (tuple d'objets)
        ancienne_couleur (objet)

    OUTPUT:
        nouv_couleur (objet)
        couleurs (tuple d'objets)
    """
    # La nouvelle couleur
    nouv_couleur = None
    # Pour savoir quand on lance la recherche
    rech = False
    # On récupère l'indice de l'ancienne couleur
    if ancienne_couleur != []:
        index_c = couleurs.index(ancienne_couleur)
    # On cherche la couleur qu'il y avait
    for i in range(len(couleurs)):
        if ancienne_couleur != []:
            if couleurs[i] == ancienne_couleur:
                rech = True
            if rech:
                if not GC.COLOURS[i].already_used:
                    nouv_couleur = couleurs[i]
                    GC.COLOURS[i].already_used = True
                    GC.COLOURS[index_c].already_used = False
                    break
        else:
            if not GC.COLOURS[i].already_used:
                nouv_couleur = couleurs[i]
                GC.COLOURS[i].already_used = True
                break
    # Si on a pas trouvé de nouvelle couleur
    # Si c'est le cas, c'est que les couleurs du joueur jusqu'à la
    # fin de la liste sont déja utilisé
    if nouv_couleur is None:
        for i in range(len(couleurs)):
            if not GC.COLOURS[i].already_used:
                GC.COLOURS[i].already_used = True
                nouv_couleur = GC.COLOURS[i]
                GC.COLOURS[index_c].already_used = False
                break
    return nouv_couleur, couleurs


def ajout_joueurs(ajout_j):
    """
    Fonction qui permet d'ajouter les joueurs

    INPUT:
        ajout_j (int) | nombres de joueurs que l'on peut encore ajouter

    OUTPUT:
        btn_bot (objet)
        btn_j (objet)
    """
    fltk.efface("Ajout")
    j = (4 - ajout_j) * 240
    btn_bot = Bouton_menu(130 + j, 400,
                          240 + j, 450,
                          "+Bot+")
    btn_bot.dessiner_rect("Ajout", epaisseur=2,
                          taille=10, remp="#c3fbfc")
    btn_j = Bouton_menu(130 + j, 340,
                        240 + j, 390,
                        "+Local+")
    btn_j.dessiner_rect("Ajout", epaisseur=2,
                        taille=10, remp="#c3fbfc")
    return btn_bot, btn_j


def fenetre_jouer(joueurs):
    """
    Fonction qui permet de choisir les joueurs / paramêtres de jeu

    INPUT:
        joueurs (liste d'objets)

    OUTPUT:
        affichage_joueurs(joueurs) (2 listes d'objets)
    """
    separation_joueur()
    btn_bot, btn_j = ajout_joueurs(4 - len(joueurs))
    btn_couleur, btn_autre = affichage_joueurs(joueurs)
    return btn_couleur, btn_autre, btn_bot, btn_j


def ouverture_fenetre(bouton_clic):
    """
    Fonction qui permet d'afficher les fenêtres

    INPUT:
        aucun

    OUTPUT:
        croix (objet)
    """
    if bouton_clic == "Règles":
        fenetre = Inter_menu("Règles", 200, 100, 880, 620, GC.texte_regle)
    if bouton_clic == "Paramètres":
        fenetre = Inter_menu("Paramètres", 200, 100, 880, 620)
    if bouton_clic == "Historique":
        fenetre = Inter_menu("Historique", 200, 100, 880, 620, GC.texte_historique)
    if bouton_clic == "Jouer":
        fltk.efface("affi_menu")
        fenetre = Inter_menu("Joueurs", 50, 150, 1030, 570)
    return fenetre.dessiner_inter()


def initialisation(boutons_menu):
    """
    Fonction qui permet d'initialiser l'interface

    INPUT:
        boutons_menu (liste d'objets)

    OUTPUT:
        aucun
    """
    fltk.texte(540, 100, "Pièges!", ancrage="center", taille=60,
               tag="affi_menu")
    for boutons in boutons_menu:
        boutons.dessiner_rect()


def fenetre_para(boutons_para):
    """
    Fonction pour choisir afficher les paramètres choisis

    INPUT:
        boutons_para (tuple d'objets)

    OUTPUT:
        aucun
    """
    # On affiche les textes
    fltk.texte(350, 265, "Son :", ancrage="center", taille=20,
               tag="Btn_para")
    fltk.texte(370, 365, "Circulaire :", ancrage="center", taille=20,
               tag="Btn_para")
    fltk.texte(370, 465, "Fenêtre Jeu :", ancrage="center", taille=20,
               tag="Btn_para")
    fltk.texte(375, 565, "Nombre Bille :", ancrage="center", taille=20,
               tag="Btn_para")
    for boutons in boutons_para:
        if boutons.texte_btn == "OUI":
            boutons.dessiner_rect("Btn_para", "#a4ff9b")
        elif boutons.texte_btn == "NON":
            boutons.dessiner_rect("Btn_para", "#f56b6b")
        else:
            boutons.dessiner_rect("Btn_para")
    return boutons_para


def main_menu():
    """
    Fonction qui permet d'afficher et renvoyer les joueurs et la taille de grille

    INPUT:
        aucun

    OUTPUT:
        joueurs (liste d'objets)
        taille_grille (int)
    """
    # Création de la liste des joueurs et de l'hote
    joueurs = [Joueurs(1, GC.COLOURS[0], True)]
    # Création des boutons
    boutons_menu = (Bouton_menu(350, 270, 730, 390, "Règles"),
                    Bouton_menu(350, 400, 730, 520, "Jouer"),
                    Bouton_menu(350, 530, 730, 650, "Historique"),
                    Bouton_menu(780, 610, 1070, 710, "Paramètres"))
    # Boutons des paramètres (SON, EST_CIRCULAIRE, TAILLE FENETRE)
    boutons_para = (Bouton_menu(580, 220, 830, 300, "OUI"),
                    Bouton_menu(580, 320, 830, 400, "OUI"),
                    Bouton_menu(580, 420, 830, 500, "1080x720"),
                    Bouton_menu(580, 520, 830, 600, "5"))
    bouton_lancer = Bouton_menu(340, 600, 740, 700, "Lancer")
    # Les tailles de fenetres possibles
    taille_fen_possible = ("1080x720", "1280x920")
    # Les tailles de grilles possibles
    taille_gri_posssible = (5, 7, 9)
    # Nombre de grilles possibles
    nb_bille_poss = ("3", "4", "5")
    # Taille de grille par défaut
    taille_grille = 5
    # Le fond
    fltk.rectangle(0, 0, 1080, 720, remplissage="#faf8cb")
    est_ouvert = False
    menu_jouer = False
    menu_parametre = False
    initialisation(boutons_menu)
    while True:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)
        abs_souris = fltk.abscisse_souris()
        ord_souris = fltk.ordonnee_souris()
        fltk.efface("surbrille")
        if not est_ouvert:
            for boutons in boutons_menu:
                # Si on est bien sur un bouton
                if boutons.clic(abs_souris, ord_souris):
                    boutons.dessiner_rect("surbrille", "#fcf9b5")
                    if tev == "ClicGauche":
                        # On ouvre une fenêtre
                        croix = ouverture_fenetre(boutons.texte_btn)
                        est_ouvert = True
                        if boutons.texte_btn == "Jouer":
                            menu_jouer = True
                            btn_couleur, btn_autre, btn_bot, btn_j = fenetre_jouer(joueurs)
                        if boutons.texte_btn == "Paramètres":
                            menu_parametre = True
                            boutons_para = fenetre_para(boutons_para)
        else:
            # Si on a ouvert la fenetre paramètre
            if menu_parametre:
                if tev == "ClicGauche":
                    if boutons_para[0].clic(abs_souris, ord_souris):
                        if boutons_para[0].texte_btn == "NON":
                            boutons_para[0].texte_btn = "OUI"
                        else:
                            boutons_para[0].texte_btn = "NON"
                        fenetre_para(boutons_para)
                    if boutons_para[1].clic(abs_souris, ord_souris):
                        if boutons_para[1].texte_btn == "NON":
                            boutons_para[1].texte_btn = "OUI"
                        else:
                            boutons_para[1].texte_btn = "NON"
                        fenetre_para(boutons_para)
                    if boutons_para[2].clic(abs_souris, ord_souris):
                        boutons_para[2].texte_btn = change_valeur(boutons_para[2].texte_btn, taille_fen_possible)
                        fenetre_para(boutons_para)
                    if boutons_para[3].clic(abs_souris, ord_souris):
                        boutons_para[3].texte_btn = change_valeur(boutons_para[3].texte_btn, nb_bille_poss)
                        fenetre_para(boutons_para)

            # Si on a ouvert la fenêtre pour jouer
            if menu_jouer:
                # Actions pour le bouton d'ajout de bots
                if btn_bot.clic(abs_souris, ord_souris):
                    btn_bot.dessiner_rect("surbrille", "#e0fdfd",
                                          taille=10, epaisseur=3)
                    if tev == "ClicGauche":
                        non_utilise, couleurs = changement_couleur(GC.COLOURS,
                                                                   [])
                        joueurs.append(Joueurs(len(joueurs) + 1,
                                               non_utilise, est_bot=True))
                        btn_couleur, btn_autre = affichage_joueurs(joueurs, taille_grille)
                        btn_bot, btn_j = ajout_joueurs(4 - len(joueurs))
                # Actions pour le bouton d'ajout de joueur
                if btn_j.clic(abs_souris, ord_souris):
                    btn_j.dessiner_rect("surbrille", "#e0fdfd",
                                        taille=10, epaisseur=3)
                    if tev == "ClicGauche":
                        non_utilise, couleurs = changement_couleur(GC.COLOURS,
                                                                   [])
                        joueurs.append(Joueurs(len(joueurs) + 1,
                                               non_utilise))
                        btn_couleur, btn_autre = affichage_joueurs(joueurs, taille_grille)
                        btn_bot, btn_j = ajout_joueurs(4 - len(joueurs))
                # Si on clique pour changer la couleur
                if len(joueurs) > 1:
                    if bouton_lancer.clic(abs_souris, ord_souris):
                        bouton_lancer.dessiner_rect("surbrille", "#fcf9b5")
                        if tev == "ClicGauche":
                            if boutons_para[0].texte_btn == "OUI":
                                active_son = True
                            else:
                                active_son = False
                            if boutons_para[1].texte_btn == "OUI":
                                est_circulaire = True
                            else:
                                est_circulaire = False
                            taille_fen = tuple(boutons_para[2].texte_btn.split("x"))
                            nb_bille = int(boutons_para[3].texte_btn)
                            return joueurs, taille_grille, active_son, est_circulaire, taille_fen, nb_bille
                if tev == "ClicGauche":
                    for bouton in btn_couleur:
                        if bouton.clic(abs_souris, ord_souris):
                            id = btn_couleur.index(bouton)
                            joueurs[id].couleur, couleurs = changement_couleur(GC.COLOURS,
                                                                               joueurs[id].couleur)
                            btn_couleur, btn_autre = affichage_joueurs(joueurs, taille_grille)
                # Si on clique pour changer de grille ou enlever un joueur
                if tev == "ClicGauche":
                    for bouton in btn_autre:
                        if bouton.clic(abs_souris, ord_souris):
                            id = btn_autre.index(bouton)
                            # Si c'est le bouton grille
                            pass
                            # Si c'est un bouton quitter
                            if id > 0:
                                fltk.efface("Para_j")
                                # On remet la couleur en False
                                index_c = couleurs.index(joueurs[id].couleur)
                                joueurs.pop(id)
                                GC.COLOURS[index_c].already_used = False
                                # On change le numéro des joueurs
                                for i in range(id, len(joueurs)):
                                    joueurs[i].nom = joueurs[i].nom[0] + str(int(joueurs[i].nom[1]) - 1)
                                btn_bot, btn_j = ajout_joueurs(4 - len(joueurs))
                                btn_couleur, btn_autre = affichage_joueurs(joueurs, taille_grille)
                            # Sinon si c'est le bouton pour la grille
                            else:
                                taille_grille = change_valeur(taille_grille, taille_gri_posssible)
                                btn_couleur, btn_autre = affichage_joueurs(joueurs, taille_grille)

            if croix.clic(abs_souris, ord_souris):
                croix.dessiner_rect("surbrille", "#ff7b7b")
                if tev == "ClicGauche":
                    fltk.efface("Jouer")
                    fltk.efface("Para_j")
                    fltk.efface("Inter")
                    fltk.efface("Sep")
                    fltk.efface("Lance")
                    fltk.efface("Btn_para")
                    fltk.efface("Ajout")
                    menu_jouer = False
                    menu_parametre = False
                    initialisation(boutons_menu)
                    est_ouvert = False

        if tev == 'Quitte':  # on sort de la boucle
            break

        fltk.mise_a_jour()
