from copy import deepcopy
from random import randint, choice
from time import sleep, time
import cProfile


from isolation import Isolation


def available_fields(the_map: dict, location: tuple, index: int = 0) -> list:
    """
    Return the availavle fields of the player.
    The function override the map and put a numbers on the available fields.

    Input:
     * the_map: dict like (x, y) = field
     * location: tuple - x, y
     * index: int - start number of indexing the fields

    Output:
     * available fields: list
    """
    fields = []
    x_p, y_p = location
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):

            if (x, y) == (0, 0):
                continue

            cords = (x_p+x, y_p+y)
            condition0 = cords in the_map
            if (not condition0):
                continue

            condition1 = the_map[cords] != "used"
            condition2 = type(the_map[cords]) != int
            if (condition1 and condition2):
                index += 1
                the_map[cords] = index
                fields.append((cords, index))
    return fields


def way_back(the_map: dict, start: tuple, stop: tuple) -> list:
    """
    Return the way back based on the map with numbers.

    Input:
     * the_map: dict like (x, y) = field
     * start: tuple - start point (x, y)
     * stop: tuple - end point (x, y)

    Output:
     * the way: list with (x, y) tuples
    """
    the_way = [start]
    x_p, y_p = start
    CORDS = [(1, 0), (0,  1), (-1, 0), (0,  -1),
             (1, 1), (-1, 1), (1, -1), (-1, -1)]
    while start != stop:
        copy_cords = deepcopy(CORDS)
        to_check = []
        for i in range(8):
            x, y = copy_cords.pop(randint(0, len(copy_cords)-1))
            if x == 0 == y:
                continue
            cords = (x_p+x, y_p+y)
            if (cords in the_map) and (type(the_map[cords]) == int):
                to_check.append(cords)
        results = [the_map[cords] for cords in to_check]
        min_index = results.index(min(results))
        min_cords = to_check[min_index]

        the_way.append(min_cords)
        start = min_cords
        x_p, y_p = start
    return the_way


def the_fast_way(the_map: dict,
                 source: tuple,
                 aim: tuple) -> list:
    """
    Return the fast way from the source to the aim.
    If there are no way: empty list

    Input:
     * the_map: dict like (x, y) = field
     * source: tuple - start point (x, y)
     * aim: tuple - end point (x, y)

    Output:
     * the fast way: list with (x, y) tuples
    """
    new_map = deepcopy(the_map)
    new_map[source] = 0
    to_check = available_fields(new_map, source, 0)
    global_index = len(to_check)
    while len(to_check) != 0:
        field, index = to_check.pop(0)
        if field == aim:
            return way_back(new_map, aim, source)
        else:
            new_map[field] = index
            new_to_check = available_fields(new_map, field, global_index)
            global_index += len(new_to_check)
            to_check += new_to_check
    return []


def get_all_scenarios(game: Isolation, player: str, n: int) -> list:
    """
    Generate all scenarios of the possible games.

    Input:
     * game: Isolation - start status of the game
     * player: str - "player1" or "player2"
     * n: int - number of moves to check

    Output:
     * scenarios: list[tuple] - one scenario is: start_move, the game, n
    """
    moves = ("n", "s", "w", "e", "nw", "ne", "sw", "se")
    scenarios = []
    for move in moves:
        new_game = deepcopy(game)
        new_game._turn = player
        if new_game.move(move):
            scenarios.append((move, new_game, 1))

    ready_scenarios = []
    while len(scenarios) != 0:
        start_move, game, move_number = scenarios.pop(0)

        new_start_move = deepcopy(start_move)
        new_game = deepcopy(game)
        if move_number == n:
            new_move_number = deepcopy(move_number)

            ready_scenarios.append((new_start_move,
                                    new_game,
                                    new_move_number))
            continue

        for move in moves:
            new_move_number = move_number + 1

            new_game.move(move)
            scenarios.append((new_start_move, new_game, new_move_number))
    return ready_scenarios


def min_max(scenarios: list, enemy: str) -> tuple:
    """
    Return the best scenario from the scenarios.

    Input:
     * scenarios: list[tuple] - one scenario is: start_move, the game, n
     * enemy: str - "player1" or "player2"

    Output:
     * resut: tuple - start move and points (value of the move)
    """
    the_best_starts = {}
    for scenario in scenarios:
        start_move, game, _ = scenario
        the_map = game.get_map()
        enemy_xy = game.find_player(enemy)
        points = len(available_fields(the_map, enemy_xy))

        if start_move not in the_best_starts:
            the_best_starts[start_move] = points
        else:
            the_best_starts[start_move] += points

    min_points = min(list(the_best_starts.values()))
    for start_move in the_best_starts:
        if the_best_starts[start_move] == min_points:
            return start_move, min_points


def heuristic(player: str,
              enemy: str,
              n: int,
              game: Isolation) -> tuple:
    """
    Return the best move for the player.

    Input:
     * player: str - "player1" or "player2"
     * enemy: str - "player1" or "player2"
     * n: int - number of moves to check
     * game: Isolation

    Output:
     * resut: tuple - start move and points (value of the move)
    """
    scnearios = get_all_scenarios(game, player, n)
    return min_max(scnearios, enemy)


def game_tree_random(map_width: int = 3,
                     map_height: int = 3,
                     iterations: int = 4,
                     sleep_time: float = 0.0):
    """
    Make a game between tree and random moves.
    """
    moves_time = []
    winners = []
    game = Isolation(None, map_width, map_height)
    game.draw()
    moves = 0
    while not game.game_over():
        sleep(sleep_time)
        player1 = game.turn()
        players = ["player1", "player2"]
        players.remove(player1)
        player2 = players[0]
        start = time()
        if player1 == "player1":
            move, _ = heuristic(player1, player2, iterations, game)
        else:
            move = choice(["n", "s", "w", "e", "nw", "ne", "sw", "se"])
        moves_time.append(time()-start)
        moves += 1
        game.move(move)
        game.draw()
    winners.append(game._winner)
    return moves_time, winners, moves


def game_tree_tree(map_width: int = 3,
                   map_height: int = 3,
                   iterations: int = 4,
                   sleep_time: float = 0.0):
    """
    Make a game between tree and tree moves.
    """
    moves_time = []
    winners = []
    game = Isolation(None, map_width, map_height)
    game.draw()
    moves = 0
    while not game.game_over():
        sleep(sleep_time)
        player1 = game.turn()
        players = ["player1", "player2"]
        players.remove(player1)
        player2 = players[0]
        start = time()
        move, _ = heuristic(player1, player2, iterations, game)
        moves_time.append(time()-start)
        game.move(move)
        game.draw()
        moves += 1
    winners.append(game._winner)
    return moves_time, winners, moves


def get_players_statistics():
    t = []
    w = []
    moves = []
    for i in range(50):
        res = game_tree_tree(map_width=7,
                             map_height=7,
                             iterations=5,
                             sleep_time=0.0)
        t += res[0]
        w += res[1]
        moves.append(res[2])

    print("min time:", min(t))
    print("avg time:", sum(t)/len(t))
    print("max time:", max(t))
    print("avg moves:", sum(moves)/len(moves))
    print("p1 wins:", w.count("player1"))
    print("p2 wins:", w.count("player2"))


def get_program_statistics():
    cProfile.run("game_tree_tree()", sort="cumtime")


if __name__ == "__main__":
    get_players_statistics()

