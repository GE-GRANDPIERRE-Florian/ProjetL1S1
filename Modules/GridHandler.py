if __name__ != "__main__":
    import Modules.slide as slide

import random, enum


class GameState(enum.Enum):
    PLAYING = 0
    TIE = 1
    WIN = 2


class Grid:
    def __init__(self, size: int) -> None:
        self.__grid: list[list[int]] = [[0 for _ in range(size)] for _ in range(size)]
        self.size: int = size
        self.__v_sliders: list[slide.Slider] = [
            slide.Slider(
                self.size, 6, self.size // 2
            ) for _ in range(self.size)
        ]
        self.__h_sliders: list[slide.Slider] = [
            slide.Slider(
                self.size, 6, self.size // 2
            ) for _ in range(self.size)
        ]
        self.winning_player : int = - 1
        self.player_list : list = []

    def get_defeated_player(self) -> list[int]:
        """
        Fucntion that return the list of the player that can't play the game anymore
        INPUT:
            - None
        OUTPUT:
            - A list of integer that represent the ids of the player that are deafeted in the game
        EDIT:
            - None
        <-----------------DOCTEST---------------->
        >>> random.seed(7)
        >>> grid = Grid(3)
        >>> grid.place_ball(1, 0, 0)
        True
        >>> grid.place_ball(3, 0, 1)
        True
        >>> grid.create_sliders()
        >>> grid.fall_ball()
        [(1, (0, 0), True)]
        >>> grid.get_defeated_player()
        [1]
        """
        defeated_player = []
        for player in self.player_list:
            if not self.has_ball_left(player):
                defeated_player.append(player)
        return defeated_player

    def get_state(self) -> GameState:
        """
        Function that tells if someone wins and the id of the wining player
        INPUT :
            - plauer_list : list of integers, represents the ids of the players playing
        OUTPUT:
            - The current game state (Represented by the enum type GameState)
        EDIT:
            - Changes the variable winning player if there is one
        <------------------------DOCTEST----------------------------->
        TODO
        """
        players_alive: list[int] = []
        for player in self.player_list:
            if self.has_ball_left(player):
                players_alive.append(player)
        if len(players_alive) > 1:
            return GameState.PLAYING
        elif len(players_alive) == 1:
            self.winning_player = players_alive[0]
            return GameState.WIN
        else:
            return GameState.TIE


    def place_ball(self, ball_id: int, x: int, y: int) -> bool:
        """
        Function that place a ball inside the grid and return a boolean
        value that indicate if the placement of the ball was succesful
        (This modify the Grid) (ball id of 0 clear the space)
        INPUT:
            - ball_id: Int, indentifier of the player who placed the ball
            - x: Int, column of th ball
            - y: Int, line of the ball
        RETURNS:
            - A boolean value that correspond to the succes or not of the ball placement
                (If the space is already taken False, else True)
        EDIT:
            - self.__grid : Add a ball to the self.__grid[y][x] if there is not
              a ball already placed at those coodronate
        <-------------------------------DOCTEST-------------------------------->
        >>> grid = Grid(3)
        >>> grid.place_ball(1, 2, 2)
        True
        >>> grid.get_grid()
        [[0, 0, 0], [0, 0, 0], [0, 0, 1]]
        >>> 
        >>> grid.place_ball(2, 2, 2)
        False
        >>> grid.get_grid()
        [[0, 0, 0], [0, 0, 0], [0, 0, 1]]
        >>> grid.place_ball(2, 1, 2)
        True
        >>> grid.get_grid()
        [[0, 0, 0], [0, 0, 0], [0, 2, 1]]
        """
        if self.__grid[y][x] == 0 and not self.is_hole_beneath(x, y):
            self.__grid[y][x] = ball_id
            if ball_id not in self.player_list:
                self.player_list.append(ball_id)
            return True
        return False

    def count_player_ball(self, player_id: int) -> int:
        """
        Function that return the number of balls a player has left
        INPUT:
            - player_id: integer that represent the id of the player we check
        OUTPUT:
            - An integer value that represent the number of ball this player has
        EDIt:
            - None
        TODO Doctest
        """
        count = 0
        for line in self.__grid:
            if player_id in line:
                for elt in line:
                    if elt == player_id:
                         count += 1
        return count

    def forfeit_texte(self):
        winning_player = max(self.player_list, key=lambda x: self.count_player_ball(x))
        return f"Joueur {winning_player} Gagne !!!"

    def is_hole_beneath(self, x: int, y: int) -> bool:
        """
        Function that check if there is a hole beneath the point of coodonate
        (x, y)
        INPUT:
            - x (int) : column of the point checked
            - y (int) : line of the point checked
        OUTPUT:
            - A boolean value that represent if the ball should fall or not
        EDIT:
            - None
        <------------------------------DOCTEST--------------------------------->

        >>> random.seed(7)
        >>> g = Grid(3)
        >>> g.create_sliders()
        >>> g.get_slider(0, False).__str__()
        '[True, False, False]'
        >>> g.get_slider(0, True).__str__()
        '[True, False, False]'
        >>> g.is_hole_beneath(0,0)
        True
        >>> g.slide_slider(True, 0, -1)
        True
        >>> g.is_hole_beneath(0,0)
        False
        """
        return self.__h_sliders[y].is_hole(x) and self.__v_sliders[x].is_hole(y)

    def is_full(self) -> bool:
        """
        Function that check if the board is full
        INPUT:
            - None
        OUTPUT:
            - Boolean value that indicate if the board is full
        EDIT:
            - None
        <------------------------------DOCTEST--------------------------------->
        >>> g_1 = Grid(2)
        >>> g_1.place_ball(1, 0, 0)
        True
        >>> g_1.place_ball(1, 0, 1)
        True
        >>> g_1.place_ball(1, 1, 0)
        True
        >>> g_1.is_full()
        False
        >>> g_1.place_ball(1, 1, 1)
        True
        >>> g_1.is_full()
        True
        """
        for ligne in self.__grid:
            if 0 in ligne:
                return False
        return True

    def randomly_place_ball(self, ball_per_player: int, nb_player: int):
        """
        Function that place balls at random
        INPUT:
            - ball_per_player (int): number of ball each player have
            - nb_player (int): number of player in the game
        OUTPUT:
            None
        EDIT:
            - Changes self.__grid to add the balls
        <----------------------------DOCTEST----------------------------------->
        >>> random.seed(86420137)
        >>> g = Grid(3)
        >>> g.randomly_place_ball(2, 2)
        >>> g.get_grid()
        [[0, 1, 2], [0, 0, 0], [2, 1, 0]]
        """
        for i in range(1, nb_player + 1):
            for _ in range(ball_per_player):
                if self.is_full():
                    raise ValueError("Cannot add more balls")  # /!\
                coordonate: tuple[int, int] = (
                    random.randint(0, self.size - 1),
                    random.randint(0, self.size - 1)
                )
                ball_placed: bool = self.place_ball(
                    i,
                    coordonate[0],
                    coordonate[1]
                )
                while not ball_placed:
                    coordonate = (
                        random.randint(0, self.size - 1),
                        random.randint(0, self.size - 1)
                    )
                    ball_placed = self.place_ball(
                        i,
                        coordonate[0],
                        coordonate[1]
                    )

    def slide_slider(self, is_vertical: bool, slider_id: int, dir: int) -> bool:
        """
        Function that slide a selected slider in the selected direction
        INPUT:
            - is_vertical (bool): indicate if we want to slide a vertical slider or not
            - slider_id (int): Id of the slider the user want to slide
            - dir (int): Direction in which the user want to move the slide (-1 or 1)
        OUTPUT:
            - A boolean value that correspond to the succes or not of the sliding
        EDIT:
            - This methods modify the slider of id slider_id
        
        <-----------------------------DOCTEST---------------------------------->

        >>> random.seed(86420137)
        >>> grid = Grid(3)
        >>> grid.get_slider(1, True).get_holes()
        [False, False, False]
        >>> grid.create_sliders()
        >>> grid.get_slider(1, True).get_holes()
        [False, True, False]
        >>> grid.slide_slider(True, 1, -1)
        True
        >>> grid.get_slider(1, True).get_holes()
        [True, False, False]
        """
        if not dir in (-1, 1): return False
        if slider_id >= self.size: return False
        if is_vertical: return self.__v_sliders[slider_id].slide(dir)
        return self.__h_sliders[slider_id].slide(dir)

    def fall_ball(self) -> list[tuple[int, tuple[int, int], bool]]:
        """
        Function that make the balls that are above an hole fall and return the
        list of the coordonate of the balls that fell
        INPUT:
            - None
        OUTPUT:
            - A list containing the coordonate of the balls that fell and the id of the
              player who owns it
        EDIT:
            - Modify the matrix of ball
        <----------------------------DOCTEST----------------------------------->
        
        >>> random.seed(7)
        >>> grid = Grid(3)
        >>> grid.place_ball(1, 0, 0)
        True
        >>> grid.place_ball(1, 1, 0)
        True
        >>> grid.place_ball(3, 0, 1)
        True
        >>> grid.get_grid()[0][0]
        1
        >>> grid.get_grid()[0][1]
        1
        >>> grid.get_grid()[1][0]
        3
        >>> grid.create_sliders()
        >>> grid.fall_ball()
        [(1, (0, 0), False)]

        >>> grid.slide_slider(True, 1, -1)
        True
        >>> grid.slide_slider(False, 0, 1)
        True
        >>> grid.fall_ball()
        [(1, (1, 0), True)]
        >>> grid.get_grid()[0][0]
        0
        >>> grid.get_grid()[1][0]
        3
        """
        fallen_ball: list[tuple[int, tuple[int, int], bool]] = []
        for i, line in enumerate(self.__grid):
            for j, elt in enumerate(line):
                if self.is_hole_beneath(j, i) and elt != 0:
                    line[j] = 0
                    fallen_ball.append((elt, (j, i), not self.has_ball_left(elt)))
        return fallen_ball

    def has_ball_left(self, player_id: int) -> bool:
        """
        Function that return True if the player still has balls on the board and
        False otherwise
        INPUT:
            - player_id (int): The id of the player and their balls
        OUTPUT:
            - A boolean value that indicate if the player still has ball on the 
            board
        EDIT:
            - None
        <--------------------------DOCTEST------------------------------------->
        >>> random.seed(7)
        >>> grid = Grid(3)
        >>> grid.place_ball(1, 0, 0)
        True
        >>> grid.place_ball(3, 0, 1)
        True
        >>> grid.has_ball_left(1)
        True
        >>> grid.has_ball_left(3)
        True
        >>> grid.create_sliders()
        >>> grid.fall_ball()
        [(1, (0, 0), True)]
        >>> grid.has_ball_left(1)
        False
        >>> grid.has_ball_left(3)
        True
        """
        for line in self.__grid:
            if player_id in line:
                return True
        return False

    def create_sliders(self) -> None:
        """
        Function that create the sliders
        INPUT:
            - None
        OUTPUT:
            - None
        EDIT:
            - Create holes in the sliders (both vertical and horizontal)
        <-----------------------------DOCTEST---------------------------------->
        >>> random.seed(86420137)
        >>> grid = Grid(3)

        >>> grid.get_slider(1, True).get_holes()
        [False, False, False]
        >>> grid.get_slider(0, True).get_holes()
        [False, False, False]
        >>> grid.get_slider(2, True).get_holes()
        [False, False, False]
        >>> grid.get_slider(1, False).get_holes()
        [False, False, False]
        >>> grid.get_slider(0, False).get_holes()
        [False, False, False]
        >>> grid.get_slider(2, False).get_holes()
        [False, False, False]

        >>> grid.create_sliders()

        >>> grid.get_slider(1, True).get_holes()
        [False, True, False]
        >>> grid.get_slider(0, True).get_holes()
        [False, True, False]
        >>> grid.get_slider(2, True).get_holes()
        [False, False, False]
        >>> grid.get_slider(1, False).get_holes()
        [False, False, False]
        >>> grid.get_slider(0, False).get_holes()
        [False, False, False]
        >>> grid.get_slider(2, False).get_holes()
        [False, True, False]
        """
        for elt in self.__v_sliders + self.__h_sliders:
            elt.generate_holes()

    def get_slider(self, id: int, vertical: bool) -> slide.Slider:
        """
        Function that return the selected slider 
        """
        if vertical:
            try:
                return self.__v_sliders[id]
            except:
                return self.__v_sliders[0]
        try:
            return self.__h_sliders[id]
        except:
            return self.__h_sliders[0]

    def get_grid(self) -> list[list[int]]:
        """
        Function that return the grid containing the balls
        INPUT:
            - None
        OUTPUT:
            - A list 
        """
        return self.__grid


if __name__ == '__main__':
    import doctest
    import slide

    print(doctest.testmod())
