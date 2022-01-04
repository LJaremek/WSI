from random import choice, randint
from copy import deepcopy

from map_generator import gen_map

WIDTH = 5
HEIGHT = 5
PLAYER = "@"
FREE = " "
WALL = "#"
AIM = "$"
FIELDS = {WALL: -1000,
          FREE: -1,
          AIM: 1000}

moves = list("wsad")

q_map = [[
        [0 for _ in range(len(moves))]
        for _ in range(WIDTH)]
        for _ in range(HEIGHT)]


the_map = []
with open("test_map.txt", "r", -1, "utf-8") as file:
    for row in file:
        the_map.append(list(row.strip()))


def find_player(the_map: list,
                player: str) -> tuple:
    for row_index, row in enumerate(the_map):
        try:
            column_index = row.index(player)
            x = row_index
            y = column_index
            return (x, y)
        except ValueError:
            pass


def make_move(the_map: list,
              direction: str,
              free_field: str = " ",
              player: str = "@") -> list:
    the_map = deepcopy(the_map)
    for row_index, row in enumerate(the_map):
        try:
            column_index = row.index(player)
            x = row_index
            y = column_index
            break
        except ValueError:
            pass

    moves = {"w": (x, y-1),
             "s": (x, y+1),
             "a": (x-1, y),
             "d": (x+1, y)}

    m_x, m_y = moves[direction]
    if the_map[m_x][m_y] == free_field:
        the_map[m_x][m_y] = player
        the_map[x][y] = free_field

    return the_map


def the_best_move(x: int, y: int):
    # if randint(0, 100) < 10:
    #     random_move = choice(moves)
    #     new_x, new_y = next_move(x, y, random_move)
    #     if (new_x >= HEIGHT or new_x < 0) or (new_y >= WIDTH or new_y < 0):
    #         pass
    #     else:
    #         # print("rand")
    #         return random_move
    index = q_map[x][y].index(max(q_map[x][y]))
    ## print("max", max(q_map[x][y]), "index", index, q_map[x][y])
    return moves[index]


def next_move(x: int, y: int, move: str) -> tuple:
    moves = {"w": (x-1, y),
             "s": (x+1, y),
             "a": (x, y-1),
             "d": (x, y+1)}
    ## print("act:", x, y, "next:", moves[move])
    return moves[move]


def game(the_map):
    the_map = gen_map(WIDTH, HEIGHT)
    the_map[-2][-2] = "$"

    f = open("fast_map.txt", "w")
    for row in the_map:
        print(row, file=f)
    f.close()

    beta = 0.9
    gamma = 0.9
    train_map = deepcopy(the_map)

    for i in range(100):
        print(i)
        x, y = (1, 1)

        while train_map[x][y] != AIM:
            ## print("-")
            ## print("act:", x, y)
            # print(f"---\n{x} {y}")
            move = the_best_move(x, y)
            # print(move)
            old_x, old_y = x, y
            x, y = next_move(old_x, old_y, move)
            ## print("new act:", x, y)

            field = train_map[x][y]
            # print(f"field '{field}'")
            if field == WALL:
                # print("WALL !")
                x, y = old_x, old_y
                q_map[x][y][moves.index(move)] -= 1000
                continue

            reward = FIELDS[field]

            try:
                old_q = q_map[old_x][old_y][moves.index(move)]
                new_q = old_q + beta*(reward + gamma*max(q_map[x][y]) - old_q)
                ## print(f"{x} {y} = {new_q}")
            except:
                print("!", x, y)
                input()

            q_map[old_x][old_y][moves.index(move)] = new_q


game(the_map)
