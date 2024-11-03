import random
import Modules.GameConstant as c

class Slider:
    def __init__(self, board_length: int, sup_length: int, num_holes: int) -> None:
        assert sup_length % 2 == 0, "Additional lengthe cannot be sepparated in two equal parts"
        self.__holes : list[bool] = [False for _ in range(board_length + sup_length)]
        self.__start_point : int = (sup_length // 2)
        self.__end_point : int = len(self.__holes) - self.__start_point
        self.__max_gap_btw_holes : int = sup_length // 2
        self.__num_holes : int = num_holes
    
    def generate_holes(self):
        """
        Function that generate holes inside of the Slider
        """
        i : int = random.randint(1, self.__max_gap_btw_holes + 1)
        j : int = 0
        while (i < len(self.__holes) and j < self.__num_holes):
            self.__holes[i] = True
            i = i + random.randint(1, self.__max_gap_btw_holes + 1)
            j += 1
    
    def slide(self, dir: int) -> bool:
        """
        Function that slide the direction of dir (-1 = left or up and 1 = right or down)
        Its like the slider was pushed from the dir And return the succes of the action
        INPUT:
            - dir: int (The direction in which we slide the slider)
        OUTPUT:
            - Succes of the action (True if the player slid the slider succesfully)
        
        --------------------------DOCTEST---------------------------------------

        >>> random.seed(86420137)
        >>> obj = Slider(7, 4, 6)
        >>> obj.generate_holes()
        >>> obj.slide(-1)
        True
        >>> obj.get_holes()
        [False, True, True, False, True, False, False]
        >>> obj.slide(-1)
        True
        >>> obj.get_holes()
        [False, False, True, True, False, True, False]
        >>> obj.slide(-1)
        False        
        """
        if c.DOES_SLIDER_LOOP:
           self.__start_point = (self.__start_point - dir) % len(self.__holes)
           self.__end_point = ((self.__end_point - dir) % len(self.__holes))
           return True
           
        if self.__start_point - dir < 0:
            return False

        if self.__end_point - dir > len(self.__holes):
            return False
        
        self.__start_point = self.__start_point - dir
        self.__end_point = self.__end_point - dir
           
        return True
    
    def is_hole(self, place: int) -> bool:
        """
        Function that check if there is a hole at *place* in the slider
        INPUT:
            - place (int) : Place where we want to check for the presence of an
                            hole (relative to the grid)
        OUTPUT:
            - A boolean value that indicate if there is a hole in the place
              that are being checked
        EDIT:
            - NONE
        <-------------------------------DOCTEST-------------------------------->
        
        >>> random.seed(86420137)
        >>> s = Slider(5, 4, 4)
        >>> s.generate_holes()
        >>> s.get_holes()
        [True, True, False, True, False]
        >>> s.is_hole(0)
        True
        >>> s.slide(1)
        True
        >>> s.slide(1)
        True
        >>> s.is_hole(0)
        False
        """
        return self.get_holes()[place]

    def get_holes(self, all: bool = False):
        if all:
            return self.__holes
        if self.__start_point < self.__end_point:
            return self.__holes[self.__start_point:self.__end_point]
        else:
            return self.__holes[self.__start_point:] + self.__holes[:self.__end_point]


    def __str__(self) -> str:
        return str(self.get_holes())
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()