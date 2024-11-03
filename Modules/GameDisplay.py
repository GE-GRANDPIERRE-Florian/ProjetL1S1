import Modules.Dependencies.fltk as fl
import Modules.GridHandler as grid
from Modules.Menu import Joueurs

width, height = 1080, 720

box_size = 60
rad_box = box_size / 4
nb_box = 5  # 5, 7 ou 9
# nb_case_slider = 2 * nb_box + 1 
# pour la V2 quand les tirettes ne seront pas circulaires

# liste temporaire pour tests sur l'affichage des balles
list_ball = [[4, 0, 1, 2, 3],
             [1, 2, 0, 1, 0],
             [1, 0, 2, 0, 2],
             [2, 1, 0, 1, 1],
             [2, 0, 1, 1, 0], ]


def disp_all_sliders(play_space: grid.Grid):
    """
        Function that display all the sliders
        INPUT:
            - width, height (float): window size
        OUTPUT:
            - None
        EDIT:
            - Display
        <-------------------------------DOCTEST-------------------------------->
        """
    # on affiches les tirettes

    for slider in range(play_space.size):
        # tirettes verticales :
        fl.rectangle(width / 2 - (nb_box * box_size) / 2 + slider * box_size,
                     height / 2 - nb_box / 2 * box_size,
                     width / 2 - (nb_box * box_size) / 2 + slider * box_size + box_size,
                     height / 2 + nb_box / 2 * box_size,
                     remplissage='yellow')
    # on affiche les tirettes horizontales
    for slider in range(play_space.size):
        # tirettes horizontales :
        fl.rectangle(width / 2 - nb_box * box_size / 2,
                     height / 2 - nb_box * box_size / 2 + slider * box_size,
                     width / 2 + nb_box * box_size / 2,
                     height / 2 - nb_box * box_size / 2 + slider * box_size + box_size,
                     remplissage='#1c626e')
    draw_holes(play_space)


def draw_holes(play_space: grid.Grid):
    """
    Function that draw the holes inside the sliders
    INPUT:
        - play_space: The place where the game is played (contain the grid and the sliders)
    OUTPUT:
        -  None
    EDIT:
        - Display
    """
    for i in range(play_space.size):
        for j in range(play_space.size):
            if play_space.is_hole_beneath(j, i):
                fl.cercle(width / 2 - nb_box * box_size / 2 + j * box_size + box_size / 2,
                          height / 2 - nb_box * box_size / 2 + i * box_size + box_size / 2,
                          rad_box*1.5, remplissage='#404040')
            elif play_space.get_slider(i, False).get_holes()[j]:
                fl.cercle(width / 2 - nb_box * box_size / 2 + j * box_size + box_size / 2,
                          height / 2 - nb_box * box_size / 2 + i * box_size + box_size / 2,
                          rad_box*1.5, remplissage='#c957c0') # TODO ; Change the color



def affiche_boules(centre_x, centre_y, rayon, c_primaire, c_secondaire):
    """
    Fonction qui affiche les boules

    INPUT:
        centre_x (int) 
        centre_y (int)
        rayon (int)
        c_primaire (str : hexadecimal)
        c_secondaire (str : hexadecimal)

    OUTPUT:
        None
    """
    # On affiche les balles
    k = rayon / 10
    fl.cercle(centre_x, centre_y, rayon,
              remplissage=c_primaire, tag="Para_j")
    fl.cercle(centre_x + 5 * k, centre_y - k * 4, rayon / 10,
              remplissage=c_secondaire, epaisseur=0, tag="Para_j")
    fl.cercle(centre_x + 2 * k, centre_y - k * 3, rayon / 10,
              remplissage=c_secondaire, epaisseur=0, tag="Para_j")
    fl.cercle(centre_x + 5 * k, centre_y - k, rayon / 10,
              remplissage=c_secondaire, epaisseur=0, tag="Para_j")


def disp_a_ball(ball: float, ligne: float, clr_prim: str, clr_sec: str):
    affiche_boules(width / 2 - (nb_box * box_size) / 2 + ball * box_size + box_size / 2,
                   height / 2 - (nb_box * box_size) / 2 + ligne * box_size + box_size / 2,
                   rad_box, clr_prim, clr_sec)


def disp_ball2(player_list: list[Joueurs], play_space: grid.Grid) -> None:
    """
        Function that display all the player's balls
        INPUT:
            - player_list: a list of player (custom class)
            - play_space: The place where the game is played (contain the grid and the sliders)
        OUTPUT:
            - None
        EDIT:
            - None
        <-------------------------------DOCTEST-------------------------------->
        Display so no doctest
    """
    player_dict = {}
    for player in player_list:
        player_dict[player.numero_joueur] = player

    _grid = play_space.get_grid()
    for i, line in enumerate(_grid):
        for j, elt in enumerate(line):
            if elt in player_dict:
                player = player_dict[elt]
                affiche_boules(
                    width / 2 - (nb_box * box_size) / 2 + j * box_size + box_size / 2,
                    height / 2 - (nb_box * box_size) / 2 + i * box_size + box_size / 2,
                    rad_box, player.couleur.primary_colour, player.couleur.primary_colour
                )


def generate_button(grid_size: int):
    """
    Function that generate the coordinate of the buttons based on the grid size
    INPUT:
        - grid_size : integer that represent the size of the grid
    OUTPUT:
        - None
    EDIT:
        - None
    <----------------------DOCTEST------------------------>
    """

    horizontal_left = []
    horizontal_right = []
    vertical_down = []
    vertical_top = []
    for btn in range(grid_size):
        # liste de liste des boutons horizontaux gauches
        horizontal_left.append([width / 2 - box_size * 2 - (nb_box * box_size) / 2,
                                height / 2 - nb_box * box_size / 2 + btn * box_size,
                                width / 2 - box_size - (nb_box * box_size) / 2,
                                height / 2 - nb_box * box_size / 2 + btn * box_size + box_size])
        # liste de liste des boutons horizontaux droits
        horizontal_right.append([width / 2 + (nb_box * box_size) / 2 + box_size,
                                 height / 2 - nb_box * box_size / 2 + btn * box_size,
                                 width / 2 + (nb_box * box_size) / 2 + box_size * 2,
                                 height / 2 - nb_box * box_size / 2 + btn * box_size + box_size])
        # liste de liste des boutons verticaux hauts
        vertical_top.append([width / 2 - (nb_box * box_size) / 2 + btn * box_size,
                             height / 2 - box_size * 2 - nb_box / 2 * box_size,
                             width / 2 - (nb_box * box_size) / 2 + btn * box_size + box_size,
                             height / 2 - box_size - nb_box / 2 * box_size])
        # liste de liste des boutons verticaux bas
        vertical_down.append([width / 2 - (nb_box * box_size) / 2 + btn * box_size,
                              height / 2 + nb_box / 2 * box_size + box_size,
                              width / 2 - (nb_box * box_size) / 2 + btn * box_size + box_size,
                              height / 2 + nb_box / 2 * box_size + box_size * 2])
    return horizontal_left, horizontal_right, vertical_down, vertical_top


HG = []
HD = []
VH = []
VB = []


def disp_all_btns():
    """
        Function that display all the buttons
        INPUT:
            - HG (list): list of coordinates of left horizontal buttons in
            list by list form
            - HD (list): list of coordinates of right horizontal buttons in
            list by list form
            - VH (list): list of coordinates of upside vertical buttons in
            list by list form
            - VB (list): list of coordinates of downside vertical buttons in
            list by list form
        OUTPUT:
            - None
        EDIT:
            - None
        <-------------------------------DOCTEST-------------------------------->
        """
    for btn in range(0, nb_box):
        # boutons horizontaux gauches
        fl.rectangle(HG[btn][0], HG[btn][1], HG[btn][2], HG[btn][3],
                     remplissage='#566573')
        # boutons horizontaux droits
        fl.rectangle(HD[btn][0], HD[btn][1], HD[btn][2], HD[btn][3],
                     remplissage='#566573')
        # boutons verticaux hauts
        fl.rectangle(VH[btn][0], VH[btn][1], VH[btn][2], VH[btn][3],
                     remplissage='#566573')
        # boutons verticaux bas
        fl.rectangle(VB[btn][0], VB[btn][1], VB[btn][2], VB[btn][3],
                     remplissage='#566573')

def draw_current_player(current_player_id: int, player_list: list[Joueurs]):
    """
    Function that draw the text that indicate which player is currently playing
    INPUT:
        - current_player_id: integer that represent the id of the current player
        - player_list: list of all the players
    OUTPUT:
        - None
    EDIT:
        - Display
    """
    fl.texte(0, 0,
            f"Tour de {player_list[current_player_id].nom}",
            player_list[current_player_id].couleur.primary_colour)

def detect(x, y):
    """
        Function that detect if the player click on a button and return which
        one if so
        INPUT:
            - x (float): abscissa of the player's click
            - y (float): ordinate of the player's click
        OUTPUT:
            - .....
        EDIT:
            - None
        <-------------------------------DOCTEST-------------------------------->
        """
    for btn in range(0, nb_box):
        # detecter clic sur boutons horizontaux gauches
        if HG[btn][0] < x < HG[btn][2]:
            if HG[btn][1] < y < HG[btn][3]:
                return True, btn, 1
        # detecter clic sur boutons horizontaux droits
        if HD[btn][0] < x < HD[btn][2]:
            if HD[btn][1] < y < HD[btn][3]:
                return True, btn, -1
        # detecter clic sur boutons verticaux hauts
        if VH[btn][0] < x < VH[btn][2]:
            if VH[btn][1] < y < VH[btn][3]:
                return False, btn, 1
        # detecter clic sur boutons verticaux bas
        if VB[btn][0] < x < VB[btn][2]:
            if VB[btn][1] < y < VB[btn][3]:
                return False, btn, -1


def init_display(play_space: grid.Grid):
    """
    Function that initialise the display
    INPUT:
        - play_space: The place where the game is played (contain the grid and the sliders)
    """
    global VB, VH, HG, HD, nb_box
    nb_box = play_space.size
    VB, VH, HG, HD = generate_button(play_space.size)


def update_display(player_list: list[Joueurs], play_space: grid.Grid, current_player_id: int):
    """
    Function that updates the display of the game
    INPUT:
        - player_list: list of the players (custom class)
        - play_space: The place where the game is played (contain the grid and the sliders)
    """
    fl.efface_tout()
    disp_all_sliders(play_space)
    disp_ball2(player_list, play_space)
    draw_current_player(current_player_id, player_list)
    disp_all_btns()


def jeu(player_list: list[Joueurs], play_space: grid.Grid):
    a = True
    while a:
        ev = fl.donne_ev()
        tev = fl.type_ev(ev)
        if tev == 'Touche':  # on indique la touche pressée
            print('Appui sur la touche', fl.touche(ev))
        elif tev == "ClicGauche":
            print("clic en", fl.abscisse(ev), fl.ordonnee(ev))
        elif tev == 'Quitte':  # on sort de la boucle
            break

        else:  # dans les autres cas, on ne fait rien
            pass

        fl.mise_a_jour()
    fl.ferme_fenetre()


if __name__ == '__main__':
    import doctest
    jeu()
    doctest.testmod()
