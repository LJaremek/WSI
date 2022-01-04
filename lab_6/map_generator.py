from random import randint
from copy import deepcopy


def way_exist(the_map: list,
              start: tuple,
              stop: tuple,
              free: str = " "
              ) -> bool:
    the_map = deepcopy(the_map)
    to_check = [start]

    while len(to_check) != 0:
        x, y = to_check.pop(0)
        if (x, y) == stop:
            return True

        the_map[x][y] = "."

        fields = [(x+1, y),
                  (x-1, y),
                  (x, y+1),
                  (x, y-1)]

        for x, y in fields:
            if the_map[x][y] == free:
                to_check.append((x, y))

    return False


def gen_map(width: int = 10,
            height: int = 10,
            start: tuple = (0, 1),
            end: tuple = None,
            free: str = " ",
            wall: str = "#"
            ) -> list:

    if end is None:
        end = (height-2, width-2)

    the_map = [list(wall*width),
               list(wall*width)]
    for _ in range(height-2):
        the_map.insert(1, list(wall+free*(width-2)+wall))

    used = width*height//5
    tries = 0
    while used != 0:
        x = randint(1, width-1)
        y = randint(1, height-1)

        if the_map[x][y] != wall:
            the_map[x][y] = wall

            if way_exist(the_map, start, end, free):
                used -= 1
            else:
                tries += 1
                the_map[x][y] = free

        if tries > 20:
            used -= 1

    return the_map
