from random import randint, choice
from time import sleep
import os

try:
    from termcolor import colored as c
except ModuleNotFoundError:
    def c(text: str, _) -> str:
        return text

from exceptions import MapSizeError


class Isolation:
    """
    The class represent the game Isolation.

    Input:
     * map: dict - the map like (x, y) = field
     * map_width: int
     * map_height: int
    """
    def __init__(self,
                 map: dict = None,
                 map_width: int = 7,
                 map_height: int = 7) -> None:
        if map_height*map_width == 1:
            raise MapSizeError(map_width, map_height)

        if map is None:
            self._map = self.new_map(map_width, map_height)
            players = self.random_players(map_width, map_height)
            self._player1, self._player2 = players
            self._map[self._player1] = "player1"
            self._map[self._player2] = "player2"
        else:
            self._map = map
            self._player1 = self.find_player("player1")
            self._player2 = self.find_player("player2")

        self._w = map_width
        self._h = map_height
        self._turn = "player1"

    def game_over(self) -> bool:
        """
        Returns a information if the game is over.

        Output:
         * game_over: bool
        """
        illegal = ("used", "player1", "player2")
        to_check = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if x == 0 == y:
                    continue
                to_check.append((x, y))

        for x_p, y_p in [self._player1, self._player2]:
            wrong = 0
            for x_c, y_c in to_check:
                location = (x_p + x_c, y_p + y_c)
                if ((location in self._map) and
                   (self._map[location] in illegal)):
                    wrong += 1
                elif (location not in self._map):
                    wrong += 1
                else:
                    wrong -= 1

            if wrong == 8:
                if self._player1 == (x_p, y_p):
                    self._winner = "player1"
                else:
                    self._winner = "player2"
                return True

        return False

    def _cls(self):
        """
        Clear the screen in a console.
        """
        os.system("cls" if os.name == "nt" else "clear")

    def new_map(self, width: int = 7, height: int = 7) -> dict:
        """
        Generate a new map with the given parameters.

        Input:
         * width: int - map width
         * height: int - map height

        Output:
         * the_map: dict like (x, y) = field
        """
        the_map = {}
        for x in range(width):
            for y in range(height):
                the_map[(x, y)] = "empty"
        return the_map

    def get_map(self) -> dict:
        """
        Returns the map of the game.

        Output:
         * the_map: dict like (x, y) = field
        """
        return self._map

    def find_player(self, player_name: str) -> tuple:
        """
        Return the coords of the given player.

        Output:
         * cords: tuple - x, y
        """
        for location in self._map:
            if self._map[location] == player_name:
                return location

    def set_map(self, new_map: dict,
                map_width: int,
                map_height: int,
                players: tuple) -> None:
        """
        Set a new map as a given map.

        Input:
         * new_map: dict like (x, y) = field
         * map_width: int
         * map_height: int
         * players: tuple[tuple] - ((x1, y,1), (x2, y2))
        """
        self._map = new_map
        self._player1, self._player2 = players
        self._map[self._player1] = "player1"
        self._map[self._player2] = "player2"
        self._w = map_width
        self._h = map_height

    def set_turn(self, player: str) -> None:
        """
        Change the player who will make a move.

        Input:
         * player: str - "player1" or "player2"
        """
        self._turn = player

    def random_players(self, width: int = 7, height: int = 7) -> dict:
        """
        Return coords of the random created players.

        Input:
         * width: int - width of the map
         * height: int - height of the map

        Output:
         * players: tuple[tuple] - ((x1, y,1), (x2, y2))
        """
        player1 = (randint(0, width-1), randint(0, height-1))
        player2 = (randint(0, width-1), randint(0, height-1))
        while player1 == player2:
            player1 = (randint(0, width-1), randint(0, height-1))
        return (player1, player2)

    def turn(self) -> str:
        """
        Return who will make a move.

        Input:
         * player: str - "player1" or "player2"
        """
        return self._turn

    def _change_turn(self) -> None:
        """
        Change the players turn.
        If turn was player1, set player2.
        If turn was player2, set player1.
        """
        if self._turn == "player1":
            self._turn = "player2"
        else:
            self._turn = "player1"

    def _override_player(self, new_player: tuple) -> None:
        """
        Set a new player coords.

        Input:
         * new_player: tuple - (x, y)
        """
        if self.turn() == "player1":
            self._player1 = new_player
        else:
            self._player2 = new_player

    def move(self, direction: str) -> bool:
        """
        Make the move of the player whose turn it is now.

        Input:
         * direction: str - n, s, w, e, nw, ne, sw, se

        Output:
         * success: bool - False if the player cannot make a move
        """
        if self.turn() == "player1":
            x, y = self._player1
            player = self._player1
            player_name = "player1"
        else:
            x, y = self._player2
            player = self._player2
            player_name = "player2"

        illegal = ("used", "player1", "player2")

        if direction == "n":
            if (
               ((x, y-1) in self._map) and
               (self._map[(x, y-1)] not in illegal)
               ):
                self._map[(x, y)] = "used"
                self._map[(x, y-1)] = player_name
                player = (x, y-1)
            else:
                return False
        elif direction == "s":
            if (
               ((x, y+1) in self._map) and
               (self._map[(x, y+1)] not in illegal)
               ):
                self._map[(x, y)] = "used"
                self._map[(x, y+1)] = player_name
                player = (x, y+1)
            else:
                return False
        elif direction == "w":
            if (
               ((x-1, y) in self._map) and
               (self._map[(x-1, y)] not in illegal)
               ):
                self._map[(x, y)] = "used"
                self._map[(x-1, y)] = player_name
                player = (x-1, y)
            else:
                return False
        elif direction == "e":
            if (
               ((x+1, y) in self._map) and
               (self._map[(x+1, y)] not in illegal)
               ):
                self._map[(x, y)] = "used"
                self._map[(x+1, y)] = player_name
                player = (x+1, y)
            else:
                return False
        elif direction == "nw":
            if (
               ((x-1, y-1) in self._map) and
               (self._map[(x-1, y-1)] not in illegal)
               ):
                self._map[(x, y)] = "used"
                self._map[(x-1, y-1)] = player_name
                player = (x-1, y-1)
            else:
                return False
        elif direction == "ne":
            if (
               ((x+1, y-1) in self._map) and
               (self._map[(x+1, y-1)] not in illegal)
               ):
                self._map[(x, y)] = "used"
                self._map[(x+1, y-1)] = player_name
                player = (x+1, y-1)
            else:
                return False
        elif direction == "sw":
            if (
               ((x-1, y+1) in self._map) and
               (self._map[(x-1, y+1)] not in illegal)
               ):
                self._map[(x, y)] = "used"
                self._map[(x-1, y+1)] = player_name
                player = (x-1, y+1)
            else:
                return False
        elif direction == "se":
            if (
               ((x+1, y+1) in self._map) and
               (self._map[(x+1, y+1)] not in illegal)
               ):
                self._map[(x, y)] = "used"
                self._map[(x+1, y+1)] = player_name
                player = (x+1, y+1)
            else:
                return False

        self._override_player(player)

        self._change_turn()

        return True

    def draw(self,
             free_space: str = "▫",
             player_one: str = "A",
             player_two: str = "B",
             used_space: str = "x") -> None:
        """
        Draw the map on the console with the given syntax.
        """
        self._cls()
        top_wall = "╔" + "═"*self._h*2 + "╗"
        bot_wall = "╚" + "═"*self._h*2 + "╝"
        wall_color = "blue"
        print(c(top_wall, wall_color))
        for x in range(self._w):
            print(c("║", wall_color), end="")
            for y in range(self._h):
                if self._map[(x, y)] == "empty":
                    print(c(free_space, "green"), end=" ")
                elif self._map[(x, y)] == "player1":
                    print(c(player_one, "white"), end=" ")
                elif self._map[(x, y)] == "player2":
                    print(c(player_two, "white"), end=" ")
                elif self._map[(x, y)] == "used":
                    print(c(used_space, "red"), end=" ")
            print(c("║", wall_color))
        print(c(bot_wall, wall_color))


if __name__ == "__main__":
    game = Isolation(None, 10, 10)
    iters = 0
    game.draw()
    print("Iteration:", iters)
    while not game.game_over():
        iters += 1
        correct_move = False
        while not correct_move:
            direction = choice(("n", "ne", "e", "se", "s", "sw", "w", "nw"))
            correct_move = game.move(direction)
        game.draw()
        print("Iteration:", iters)
        sleep(0.5)

