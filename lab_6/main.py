from random import randint

from map_generator import gen_map, way_exist

WIDTH = 12
HEIGHT = 12
FREE = " "
WALL = "#"
FIELDS = {WALL: -1000,
          FREE: -1}

MOVES = ("w", "s", "a", "d")


def open_map(path: str) -> list:
    the_map = []

    with open(path, "r", -1, "utf-8") as file:
        for row in file:
            the_map.append(list(row.strip()))

    return the_map


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


def save_map(the_map: list, file_name: str = "my_map.txt") -> None:
    with open(file_name, "w", -1, "utf-8") as file:
        for row in the_map:
            print(row, file=file)


def make_q_table(width: int, height: int):
    return [[
            [0 for _ in range(len(MOVES))]
            for _ in range(width)]
            for _ in range(height)]


def get_map(the_map: list, map_path: str):
    if the_map is not None:
        pass  # the_map = the_map
    elif the_map is None and map_path != "random":
        the_map = open_map(map_path)
    elif the_map is None and map_path == "random":
        the_map = gen_map(WIDTH, HEIGHT, free=FREE, wall=WALL)

    return the_map


def train_player(epochs: int,
                 map_dict: dict,
                 the_map: list = None,
                 map_path: str = "random",
                 q_table: list = None,
                 aim_coords: tuple = None,
                 beta: float = 0.9,
                 gamma: float = 0.9):

    FREE = map_dict["free"]
    WALL = map_dict["wall"]

    the_map = get_map(the_map, map_path)

    if q_table is None:
        q_table = make_q_table(WIDTH, HEIGHT)

    for _ in range(epochs):
        x, y = random_coords(the_map, aim_coords, FREE)
        while (x, y) != aim_coords:
            move = the_best_move(q_table, x, y)
            old_x, old_y = x, y
            x, y = next_move(old_x, old_y, move)

            field = the_map[x][y]
            if field == WALL:
                x, y = old_x, old_y
                q_table[x][y][MOVES.index(move)] -= 1000
                continue

            reward = FIELDS[field]

            old_q = q_table[old_x][old_y][MOVES.index(move)]
            new_q = old_q + beta*(reward + gamma*max(q_table[x][y]) - old_q)
            q_table[old_x][old_y][MOVES.index(move)] = new_q

    return q_table


def get_way(q_table: list,
            start_coords: tuple,
            end_coords: tuple,
            map_dict: dict,
            map_path: str = "",
            the_map: list = None):

    the_map = get_map(the_map, map_path)

    the_way = [start_coords]

    x, y = start_coords
    while (x, y) != end_coords:
        move = the_best_move(q_table, x, y)
        old_x, old_y = x, y
        x, y = next_move(old_x, old_y, move)

        field = the_map[x][y]
        if field == WALL:
            x, y = old_x, old_y
            continue

        the_way.append((x, y))

    return the_way


def main(random_map: bool = False):
    map_dict = {"player": "@",
                "aim": "$",
                "free": " ",
                "wall": "#"}

    start = (1, 1)
    end = (HEIGHT-2, WIDTH-2)

    if random_map:
        the_map = gen_map(WIDTH, HEIGHT)
    else:
        the_map = open_map("testing_map_01.txt")

    print("Start training ...")
    q_table = train_player(epochs=1000,
                           map_dict=map_dict,
                           the_map=the_map,
                           map_path=None,
                           q_table=None,
                           aim_coords=end,
                           beta=0.9,
                           gamma=0.9)
    print("... end training.")

    print("Start getting the way ...")
    the_way = get_way(q_table=q_table,
                      start_coords=start,
                      end_coords=end,
                      map_dict=map_dict,
                      map_path=None,
                      the_map=the_map)

    for x, y in the_way:
        the_map[x][y] = "x"
    for row in the_map:
        print("".join(row))


if __name__ == "__main__":
    main(True)
