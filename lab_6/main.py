from q_learning import random_player, train_player, way_exist
from map_generator import gen_map, open_map

WIDTH = 10
HEIGHT = 10
FREE = " "
WALL = "#"
fields_dict = {WALL: -1000,
               FREE: -1}


def main(random_map: bool = False):
    map_dict = {"player": "@",
                "aim": "$",
                "free": " ",
                "wall": "#",
                "width": WIDTH,
                "height": HEIGHT}

    start = (1, 1)
    end = (HEIGHT-2, WIDTH-2)

    if random_map:
        the_map = gen_map(WIDTH, HEIGHT)
    else:
        the_map = open_map("testing_map_01.txt")

    random_moves = random_player(start_coords=start,
                                 end_coords=end,
                                 map_dict=map_dict,
                                 the_map=the_map,
                                 map_path=None)
    print(f"Random Player passes the map in {random_moves} moves.")

    print("Start training ...")
    q_table, path = train_player(epochs=1_00,
                                 map_dict=map_dict,
                                 the_map=the_map,
                                 fields_dict=fields_dict,
                                 map_path=None,
                                 q_table=None,
                                 aim_coords=end,
                                 beta=0.9,
                                 gamma=0.9)
    print("... end training.")
    print(f"QTable Player passes the map in {len(path)} moves.")

    # print("Start getting the way ...")
    # the_way = get_way(q_table=q_table,
    #                   start_coords=start,
    #                   end_coords=end,
    #                   map_dict=map_dict,
    #                   map_path=None,
    #                   the_map=the_map)
    # print("... end getting the way.")

    for x, y in path:
        the_map[x][y] = "x"
    for row in the_map:
        print("".join(row))

    # draw_arrows(the_map, q_table)


if __name__ == "__main__":
    main(True)
