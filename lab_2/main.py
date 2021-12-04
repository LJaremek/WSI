from time import time

from logic_draw import Paint, draw_best_distances, draw_distances
from logic_graph import tournament_selection, mutate_population
from logic_graph import random_population, all_distance
from logic_graph import standard_deviation
from logic_graph import random_graph


def evolutionary_algorithm(population: list, generations_number: int) -> list:
    the_best_distances = []
    all_distances = []
    for _ in range(generations_number):
        new_population = tournament_selection(population)
        mutated_population = mutate_population(new_population, 80, 80)
        new_population = mutated_population

        the_best = min(new_population, key=all_distance)
        the_best_distances.append(all_distance(the_best))
        all_distances.append(new_population)

        population = new_population
    return the_best_distances, all_distances, the_best


def main(draw_the_best_distances: bool,
         draw_all_distances: bool,
         draw_graph: bool,
         population: list,
         gens: int) -> float:
    results = evolutionary_algorithm(population, gens)
    the_best_distances, all_distances, the_best = results

    if draw_the_best_distances:
        draw_best_distances(the_best_distances)

    if draw_all_distances:
        draw_distances(all_distances)

    if draw_graph:
        paint = Paint(600, 600)
        paint.draw_cycle(the_best)
        paint.show_perm()

    return max(the_best_distances)


if __name__ == "__main__":
    x_range = 1
    times = []
    results = []
    for x in range(x_range):
        start_time = time()
        draw_the_best_distances = False
        draw_all_distances = False
        draw_graph = False

        points = random_graph([-200, 200], [-200, 200], 30)
        population = random_population(points, 30)
        generations = 300

        result = main(draw_the_best_distances,
                      draw_all_distances,
                      draw_graph,
                      population,
                      generations)
        times.append(time()-start_time)
        results.append(result)
    print(min(times), max(times), sum(times)/len(times),
          standard_deviation(times))
    print(min(results), max(results), sum(results)/len(results),
          standard_deviation(results))
    print()

