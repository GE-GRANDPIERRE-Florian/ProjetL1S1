import time

import Modules.Dependencies.fltk as fl
import Modules.GridHandler as GHandler
import Modules.LanguageHandler as lang
import Modules.Menu as Menu
import Modules.GameConstant as c
import Modules.GameDisplay as display
import Modules.bot as bot
import argparse


def print_sliders():
    """
    Function tha print the sliders
    INPUT:
        - 
    """
    for sliders in grid._Grid__h_sliders:
        print(sliders)

    print("\n")

    for i in range(len(grid.get_grid())):
        print(end="[")
        for sliders in grid._Grid__v_sliders:
            print(sliders.get_holes()[i], end=", ")
        print(end="]\n")


def matrix_to_str(matrix: list[list], max_char_lengh : int) -> str:
    """
    Function that return a string of the matrix ready for printing (we don't
    print it directly because i don't know how to use doctest with print)
    INPUT:
        - matrix (list[list]) : A matrix of element
        - max_char_lengh (int) : Maximum number of charracter that an element of
                                 the maxtrix has
    OUTPUT:
        - A string version of the matrice
    EDIT:
        - Nothing
    <---------------------------------DOCTEST---------------------------------->
    """
    generated_str : str = ""
    for line in matrix:
        for elt in line:
            str_elt : str = str(elt)
            generated_str += str_elt + " " * (max_char_lengh - len(str_elt) ) + ","
        generated_str = generated_str[:len(generated_str) - 1]
        generated_str += "\n"
    return generated_str


def next_turn(current_turn: int):
    turn = (current_turn + 1) % len(players)
    i = 0
    while turn + 1 in gameplay_grid.get_defeated_player() and i < 4:
        turn = (turn + 1) % len(players)
        i += 1  # avoid infinite loops
    return turn


parser = argparse.ArgumentParser()
parser.add_argument("--graphics", action='store_true')
parser.add_argument("--lang", type=str)
args = parser.parse_args()

if args.lang is not None and args.lang in lang.languages_aivalable:
    language:  lang.Langue = lang.languages_aivalable[args.lang]
else:
    language:  lang.Langue = lang.languages_aivalable["fr_FR"]


if args.graphics:
    fl.cree_fenetre(1080, 720)
    players, grid_size, has_sfx, c.DOES_SLIDER_LOOP, window_size, nb_ball = Menu.main_menu()
    fl.ferme_fenetre()
    fl.cree_fenetre(window_size[0], window_size[1])
    display.width = int(window_size[0])
    display.height = int(window_size[1])
    gameplay_grid = GHandler.Grid(grid_size)
    bot_list = {}
    current_turn = 0
    for player in players:
        if player.est_bot:
            bot_list[player.numero_joueur] = (bot.Bot(player.numero_joueur, gameplay_grid))
    gameplay_grid.create_sliders()
    gameplay_grid.randomly_place_ball(nb_ball, len(players))
    gameplay_grid.fall_ball()
    display.init_display(gameplay_grid)
    display.update_display(players, gameplay_grid, current_turn)
    defeated_player = []
    forfeit = False
    while True:
        ev = fl.donne_ev()
        tev = fl.type_ev(ev)
        if tev == "Quitte":
            quit()
        if tev == "ClicGauche" and not players[current_turn].est_bot:
            result_clic = display.detect(fl.abscisse(ev), fl.ordonnee(ev))
            if result_clic is not None:
                gameplay_grid.slide_slider(*result_clic)
                gameplay_grid.fall_ball()
                current_turn = next_turn(current_turn)
                display.update_display(players, gameplay_grid, current_turn)
        elif players[current_turn].est_bot:
            time.sleep(1.5)
            _bot = bot_list[players[current_turn].numero_joueur]
            _bot.make_move()
            gameplay_grid.fall_ball()
            current_turn = next_turn(current_turn)
            display.update_display(players, gameplay_grid, current_turn)

        if gameplay_grid.get_state() != GHandler.GameState.PLAYING:
            break

        if tev == "Touche" and fl.touche(ev).upper() == "F":
            forfeit = True
            break

        fl.mise_a_jour()

    fl.efface_tout()

    if forfeit:
        fl.texte(int(window_size[0]) / 2, int(window_size[1]) / 2,
                gameplay_grid.forfeit_texte(), 'black', taille=40, ancrage="center")

    elif gameplay_grid.get_state() == GHandler.GameState.TIE:
        fl.texte(int(window_size[0]) / 2, int(window_size[1]) / 2, "Egalité !!!", 'black', taille=40, ancrage="center")

    elif gameplay_grid.get_state() == GHandler.GameState.WIN:
        fl.texte(int(window_size[0]) / 2, int(window_size[1]) / 2,
                f"Joueur {gameplay_grid.winning_player} gagne !!!", 'black', taille=40, ancrage="center")

    while True:
        tev = fl.type_ev(fl.donne_ev())
        if tev == "Quitte":
            quit()
        fl.mise_a_jour()

else:
    grid = GHandler.Grid(size=7)
    grid.create_sliders()
    grid.randomly_place_ball(3, 1)
    grid.fall_ball()
    
    print(matrix_to_str(grid.get_grid(), 1))
    print_sliders()

    player_input : str = input(language.get_text("ASK_SLIDER"))
    p_dir : str = input(language.get_text("ASK_DIR"))

    while player_input.upper() != "Q":
        try:
            is_vertical: bool = player_input[0].upper() == "V"
            slider_id: int = int(player_input[1])
            direction: int = int(p_dir)
            succes : bool = grid.slide_slider(
                    is_vertical, slider_id, direction
                )
            if succes:
                print(language.get_text("SLIDER_MOVE"))
                
                print(grid.fall_ball())
                print(matrix_to_str(grid.get_grid(), 1), end="\n\n")

                print_sliders()
                
                if grid.has_ball_left(1):
                    player_input: str = input(language.get_text("ASK_SLIDER"))
                    p_dir: str = input(language.get_text("ASK_DIR"))
                else:
                    print(language.get_text("WIN"))
                    break

            else:
                print(language.get_text("IMPOSSIBLE_SLIDE"))
                player_input: str = input(language.get_text("ASK_SLIDER"))
                p_dir: str = input(language.get_text("ASK_DIR"))

        except Exception as e:
            print("\n")
            print(language.get_text("MONTY_PYTHON_REF"))
            print(language.get_text("CRASH_MSG") + "\n", e)
            quit()