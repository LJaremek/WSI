from random import randint
from copy import deepcopy


def open_map(path: str) -> list:
    the_map = []

    with open(path, "r", -1, "utf-8") as file:
        for row in file:
            the_map.append(list(row.strip()))

    return the_map


def save_map(the_map: list, file_name: str = "my_map.txt") -> None:
    with open(file_name, "w", -1, "utf-8") as file:
        for row in the_map:
            print(row, file=file)


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

        the_map[x][y] = "x"

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
    """
    12x12 is max for my lap
    """

    if end is None:
        end = (height-2, width-2)

    the_map = [list(wall*width),
               list(wall*width)]
    for _ in range(height-2):
        the_map.insert(1, list(wall + free*(width-2) + wall))

    used = width*height//5
    tries = 0
    while used > 0:
        x = randint(1, height-1)
        y = randint(1, width-1)
        if the_map[x][y] != wall:
            the_map[x][y] = wall

            if way_exist(the_map, start, end, free):
                used -= 1
            else:
                tries += 1
                the_map[x][y] = free

            if tries > 20:
                tries = 0
                used -= 1

    return the_map


if __name__ == "__main__":
    the_map = gen_map(12, 12)
    [print(row) for row in the_map]

    f = open("testing_map.txt", "w")
    [print("".join(row), file=f) for row in the_map]
    f.close()
