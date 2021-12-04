from __future__ import annotations
from random import choice, randint, random
from copy import deepcopy


class Point:
    """
    The class represents a point on the Cartesian system.

    Input:
     * x: int
     * y: int
    """
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def __eq__(self, point: Point) -> bool:
        return (self._x == point.x()) and (self._y == point.y())

    def __repr__(self) -> str:
        return f"({self._x}, {self._y})"

    def x(self) -> int:
        """
        Returns the x of the Point.
        """
        return self._x

    def y(self) -> int:
        """
        Returns the y of the Point.
        """
        return self._y

    def distance_to(self, point: Point) -> float:
        """
        Calculation of the distance between the Point and the given point.

        Input:
         * point: Point

        Output:
         * distance: float
        """
        return ((self._x - point.x())**2 + (self._y - point.y())**2)**(1/2)


def points_distance(point1: Point, point2: Point) -> float:
    """
    Calculation of the distance between the given points.

    Input:
        * point1: Point
        * point2: Point

    Output:
        * distance: float
    """
    return ((point1.x() - point2.x())**2 + (point2.y() - point2.y())**2)**(1/2)


def all_distance(points: list) -> float:
    """
    Route calculation throughout the cycle.
    Points are given one by one. The last one is next to the first.

    Input:
        * points: list[Point]

    Output:
        * distance: float
    """
    distance = 0
    for index, point in enumerate(points):
        if index+1 < len(points):
            distance += points_distance(point, points[index+1])
        else:
            distance += points_distance(point, points[0])
    return distance


def random_graph(x_range: list, y_range: list, n: int = 10) -> list:
    """
    Generate a random graph (from the given x, y range)
    with n random points.

    Input:
     * x_range: list[int] - left and right sides of a x range
     * y_range: list[int] - left and right sides of a y range
     * n: int - number of points to generate

    Output:
     * list[Point]
    """
    points = []
    combinations = (abs(x_range[1] - x_range[0]+1)
                    * (abs(y_range[1] - y_range[0])+1))
    if combinations < n:
        n = combinations
    while len(points) != n:
        new_point = Point(randint(*x_range), randint(*y_range))
        if new_point not in points:
            points.append(new_point)
    return points


def random_cluster_graph(x_range: list, y_range: list,
                         n: int, cities_n: int = 4) -> list:
    """
    Generate a random cluster graph (from the given x, y range)
    with n random points and cities_n clusters.

    Input:
     * x_range: list[int] - left and right sides of a x range
     * y_range: list[int] - left and right sides of a y range
     * n: int - number of points to generate
     * cities_n: int - number of point clusters

    Output:
     - list[Point]
    """
    population = []
    the_cities = []
    while len(the_cities) != cities_n:
        random_city = Point(randint(*x_range), randint(*y_range))
        if random_city not in the_cities:
            the_cities.append(random_city)

    max_range = abs(x_range[1] - x_range[0]) + abs(y_range[1] - y_range[0])
    max_range //= 13

    while len(population) + cities_n != n:
        the_city = choice(the_cities)
        x, y = the_city.x(), the_city.y()

        new_x = x + randint(-max_range, max_range)
        while x_range[0] > new_x < x_range[1]:
            new_x = x + randint(-max_range, max_range)

        new_y = y + randint(-max_range, max_range)
        while y_range[0] > new_y < y_range[1]:
            new_y = y + randint(-max_range, max_range)

        new_point = Point(new_x, new_y)
        if new_point not in population:
            population.append(new_point)
    return population + the_cities


def random_homogeneous_graph(x_range: list, y_range: list, n: int) -> list:
    """
    Generate a random homogeneous graph (from the given x, y range)
    with n random points.

    Input:
     - x_range: list[int] - left and right sides of a x range
     - y_range: list[int] - left and right sides of a y range
     - n: int - number of points to generate

    Output:
     - list[Point]
    """
    population = []
    root = int(n**(1/2))
    max_range = abs(x_range[1] - x_range[0]) + abs(y_range[1] - y_range[0])
    max_range //= 2
    length = max_range // root

    for x in range(*x_range, length):
        for y in range(*y_range, length):
            population.append(Point(x, y))
    return population


def random_population(points: list, size: int) -> list:
    """
    Generate a random population of the given size from the given points.

    Input:
     - points: list[Point] - graph
     - size: int

    Output:
     - list[list[Point]] - graph list
    """
    population = []
    while len(population) != size:
        population.append(sorted(points, key=lambda k: random()))
    return population


def unique_values(population: list) -> int:
    """
    Return the number of unique values (persons) in the given population.

    Input:
     - population: list[list[Point]] - graph

    Output:
     - int - number of unique values
    """
    unique_people = []
    for person in population:
        if person not in unique_people:
            unique_people.append(person)
    return len(unique_people)


def tournament_selection(population: list) -> list:
    """
    Return the new population created by tournament selection.

    Input:
     - population: list[list[Point]] - graph

    Output:
     - list[list[Point]] - selected population
    """
    new_population = []
    while len(new_population) != len(population):
        player1 = choice(population)
        player2 = choice(population)
        if (player1 == player2) and (unique_values(population) != 1):
            continue
        if all_distance(player1) < all_distance(player2):
            new_population.append(player1)
        else:
            new_population.append(player2)
    return new_population


def change_positions(the_list: list, index0: int,
                     index1_0: int, index1_1) -> list:
    """
    Return the given list with swapped points with the given indexes.

    Input:
     - the_list: list[list[Point]]
     - index0: int
     - index1_0: int - index of the first point
     - index1_1: int - index of the second point

    Output:
     - list[list[Point]]
    """
    the_list[index0][index1_0], the_list[index0][index1_1] = \
        the_list[index0][index1_1], the_list[index0][index1_0]
    return the_list


def mutate_person(person: list, precent: int) -> list:
    """
    Return a new mutant person with the given probability of mutating the gene.

    Input:
     - person: list[Point]
     - precent: int - probability

    Output:
     - new_person: list[Point]
    """
    nperson = deepcopy(person)
    for index in range(len(nperson)):
        los = randint(0, 100)
        if precent < los:
            new_index = randint(0, len(nperson)-1)
            nperson[new_index], nperson[index] = \
                nperson[index], nperson[new_index]
    return nperson


def mutate_population(population: list,
                      pop_prec: int = 50, per_prec: int = 50) -> list:
    """
    Return a new population of mutants with
    the given probability of a person mutating
    and probability of a gene mutation.

    Input:
     - population: list[list[Point]]
     - pop_prec: int - probability of a person mutating
     - per_prec: int - probability of a gene mutating

    Output:
     - new_population: list[list[Point]]
    """
    new_population = []
    for person in population:
        los = randint(0, 100)
        if pop_prec < los:
            new_population.append(mutate_person(person, per_prec))
        else:
            new_population.append(deepcopy(person))
    return new_population


def standard_deviation(data: list) -> float:
    averange = sum(data)/len(data)
    the_sum = 0
    for number in data:
        the_sum += (averange - number)**(2)
    the_sum /= len(data)
    return the_sum**(1/2)

