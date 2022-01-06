from random import randint, choice

from map_generator import gen_map, way_exist, open_map

MOVES = ("w", "s", "a", "d")


def random_coords(the_map: list, aim_coords: tuple, free: str = " ") -> tuple:
    x = randint(1, len(the_map)-2)
    y = randint(1, len(the_map[0])-2)
    is_way = way_exist(the_map, (x, y), aim_coords, free)

    while the_map[x][y] != free or not is_way:
        x = randint(1, len(the_map)-2)
        y = randint(1, len(the_map[0])-2)
        is_way = way_exist(the_map, (x, y), aim_coords, free)

    return x, y


def the_best_move(q_table: list, x: int, y: int):
    index = q_table[x][y].index(max(q_table[x][y]))
    return MOVES[index]


def next_move(x: int, y: int, move: str) -> tuple:
    moves = {"w": (x-1, y),
             "s": (x+1, y),
             "a": (x, y-1),
             "d": (x, y+1)}
    return moves[move]


def make_q_table(width: int, height: int):
    return [[
            [0 for _ in range(len(MOVES))]
            for _ in range(width)]
            for _ in range(height)]


def get_map(the_map: list, map_path: str, map_dict: dict) -> list:
    if the_map is not None:
        pass  # the_map = the_map
    elif the_map is None and map_path != "random":
        the_map = open_map(map_path)
    elif the_map is None and map_path == "random":
        the_map = gen_map(map_dict["width"],
                          map_dict["height"],
                          free=map_dict["free"],
                          wall=map_dict["wall"])

    return the_map


def draw_arrows(the_map: list, q_table: list) -> None:
    arrows = ["⇧", "⇩", "⇦", "⇨"]
    for y_index, row in enumerate(the_map):
        for x_index, cell in enumerate(row):
            index = q_table[y_index][x_index].index(
                max(q_table[y_index][x_index])
                )
            print(arrows[index], end="")
        print()


def random_player(start_coords: tuple,
                  end_coords: tuple,
                  map_dict: dict,
                  the_map: list = None,
                  map_path: str = "random",
                  aim_coords: tuple = None):

    WALL = map_dict["wall"]

    the_map = get_map(the_map, map_path, map_dict)

    x, y = start_coords
    move_counter = 0

    while (x, y) != end_coords:
        move = choice(MOVES)
        old_x, old_y = x, y
        x, y = next_move(old_x, old_y, move)
        move_counter += 1
        if the_map[x][y] == WALL:
            x, y = old_x, old_y

    return move_counter


def train_player(epochs: int,
                 map_dict: dict,
                 fields_dict: dict,
                 the_map: list = None,
                 map_path: str = "random",
                 q_table: list = None,
                 aim_coords: tuple = None,
                 beta: float = 0.9,
                 gamma: float = 0.9):

    FREE = map_dict["free"]
    WALL = map_dict["wall"]
    WIDTH = map_dict["width"]
    HEIGHT = map_dict["height"]

    the_map = get_map(the_map, map_path, map_dict)

    if q_table is None:
        q_table = make_q_table(WIDTH, HEIGHT)

    collisions_with_walls = 0

    for i in range(epochs):
        if i == epochs-1:
            path = []
        x, y = random_coords(the_map, aim_coords, FREE)
        while (x, y) != aim_coords:
            if i == epochs-1:
                path.append((x, y))
            move = the_best_move(q_table, x, y)
            old_x, old_y = x, y
            x, y = next_move(old_x, old_y, move)

            field = the_map[x][y]
            if field == WALL:
                x, y = old_x, old_y
                q_table[x][y][MOVES.index(move)] -= 1000
                collisions_with_walls += 1
                continue

            reward = fields_dict[field]

            old_q = q_table[old_x][old_y][MOVES.index(move)]
            new_q = old_q + beta*(reward + gamma*max(q_table[x][y]) - old_q)
            q_table[old_x][old_y][MOVES.index(move)] = new_q

    return q_table, path


def get_way(q_table: list,
            start_coords: tuple,
            end_coords: tuple,
            map_dict: dict,
            map_path: str = "",
            the_map: list = None):

    the_map = get_map(the_map, map_path, map_dict)

    the_way = [start_coords]

    x, y = start_coords
    while (x, y) != end_coords:
        move = the_best_move(q_table, x, y)
        old_x, old_y = x, y
        x, y = next_move(old_x, old_y, move)

        field = the_map[x][y]
        if field == map_dict["wall"]:
            return False

        the_way.append((x, y))

    return the_way
