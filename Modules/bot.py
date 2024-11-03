import copy
import random

import Modules.GridHandler as g

self_damage_penalty: float = 5.0
self_ko_penalty: float = 100.0
ko_reward: float = 4.5
enemy_damaged_reward: float = 3.0
impossible_move_penalty: float = 10000.0


def evaluate_move(
        fallen_ball_list,  # TODO: add accurate type hint
        player_id: int
) -> float:
    """
    Function that evaluate the results of a move and return a floating point number
    that represent how good the move is
    INPUT:
        - fallen_ball_list : A list containing the coordonate of tha balls that fell and the id of the
            player who owns it, as well as if the move us possible in the first place
        - player_id: The id of the player tha performed the move
    OUTPUT:
        - A floating point value that represent the score of the move
    EDIT:
        - None
    <---------------------------DOCTEST------------------------------------>
    >>> evaluate_move((tuple(), True), 1)
    0.0
    >>> evaluate_move((((1, (0, 0), False),), True), 1)
    -5.0
    >>> evaluate_move((((1, (0, 0), False),), True), 2)
    3.0
    >>> evaluate_move(((( 1, (0, 0), True),), True), 1)
    -105.0
    >>> evaluate_move((((1, (0, 0), True),), True), 2)
    7.5
    """
    # (,), True) (((0, 0), 1, False)
    end_score: float = 0.0
    for fallen_ball in fallen_ball_list[0]:
        if fallen_ball[0] == player_id:
            end_score -= self_damage_penalty + int(fallen_ball[2]) * self_ko_penalty
        else:
            end_score += enemy_damaged_reward + int(fallen_ball[2]) * ko_reward
    return end_score #  - impossible_move_penalty * int(fallen_ball_list[1])


class Bot:
    def __init__(self, identity: int, grid: g.Grid) -> None:
        self.play_space: g.Grid = grid
        self.id: int = identity
        self.banned_move: list = []

    def simulate_move(self, slider_id: str, dir: int):
        """
        Function that simulate a slider move and return
        the result of the movement.
        """
        simulated_board: g.Grid = copy.deepcopy(self.play_space)
        slide_possible: bool = simulated_board.slide_slider(slider_id[0] == "V", int(slider_id[1]), dir)
        fell: list = simulated_board.fall_ball()
        return fell, slide_possible

    def get_moves(self) -> list:
        """
        Function That return the possibles moves
        INPUT:
            - None
        OUTPUT:
            - A list of tuple where the first element is the slider
              description and the other is the direction, the list is shuffled as
              a way to randomize the output when two choices are tied.
        EDIT:
            - None

        <-------------------------DOCTEST------------------------------------------>

        >>> random.seed(0)
        >>> grid = g.Grid(3)
        >>> bot = Bot(1, grid)
        >>> bot.get_moves()
        [('V0', 1), ('H1', 1), ('H1', -1), ('V2', 1), ('H2', -1), ('V1', -1), ('V1', 1), ('H0', 1), ('V2', -1), ('V0', -1), ('H2', 1), ('H0', -1)]
        >>> bot.get_moves()
        [('V2', 1), ('V0', -1), ('V1', 1), ('H0', 1), ('H0', -1), ('H2', 1), ('H1', 1), ('V0', 1), ('H2', -1), ('V2', -1), ('V1', -1), ('H1', -1)]
        """
        move_list = []
        for letter in "VH":
            for i in range(self.play_space.size):
                move_list.append((letter + str(i), -1))
                move_list.append((letter + str(i), 1))
        random.shuffle(move_list)
        return move_list

    def decide_move(self) -> tuple[str, int]:
        """
        Function that return which move gets made
        INPUT:
            - None
        OUTPUT:
            - A tuple in which the first element is the id of the slider
              and the second  is the direction of the move
        EDIT:
            - None
        <------------------------DOCTEST------------------------------>>>> random.seed(0)
        >>> random.seed(0)
        >>> grid = g.Grid(3)
        >>> grid.randomly_place_ball(2, 2)
        >>> bot = Bot(1, grid)
        >>> bot.decide_move()
        ('V2', 1)
        >>> bot.decide_move()
        ('V0', -1)
        """
        move_list = self.get_moves()
        move_result_list = [self.simulate_move(move[0], move[1]) for move in move_list]
        score_list: list[float] = [evaluate_move(result, self.id) for result in move_result_list]
        best_move_index: int = score_list.index(max(score_list))
        return move_list[best_move_index]

    def make_move(self):
        """
        Function that does the move decided by, decide_move
        INPUT:
            - None
        OUTPUT:
            - None
        EDIT:
            - Move Sliders in the playspace
        """
        move: tuple[str, int] = self.decide_move()
        self.play_space.slide_slider(move[0][0] == "V", int(move[0][1]), move[1])
