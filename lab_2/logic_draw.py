import matplotlib.pyplot as plt
import pygame

from logic_graph import Point, all_distance


class Paint:
    """
    Class to drawing the graphs.

    Input:
     * width: int - canvas width
     * height: int - canvas height
     * back_color: tuple - background color as (RED, GREEN, BLUE)
     * point_color: tuple - points color as (RED, GREEN, BLUE)
     * line_color: tuple - lines color as (RED, GREEN, BLUE)
    """
    def __init__(self, width: int = 500, height: int = 500,
                 back_color: tuple = (255, 255, 255),
                 point_color: tuple = (0, 0, 255),
                 line_color: tuple = (0, 0, 0)) -> None:
        self._w = width
        self._h = height
        self._back_color = back_color
        self._point_color = point_color
        self._line_color = line_color
        self._surface = pygame.display.set_mode((width, height))
        self._surface.fill(back_color)

    def draw_point(self, point: Point) -> None:
        """
        Draw the given Point on the canvas.

        Input:
         * point: Point
        """
        pygame.draw.circle(self._surface, self._point_color,
                           (point.x() + self._w//2, point.y() + self._h//2),
                           5)

    def draw_line(self, point1: Point, point2: Point) -> None:
        """
        Draw a line between the given Points on the canvas.

        Input:
         * point1: Point
         * point2: Point
        """
        pygame.draw.line(self._surface, self._line_color,
                         (point1.x() + self._w//2, point1.y() + self._h//2),
                         (point2.x() + self._w//2, point2.y() + self._h//2))

    def draw_cycle(self, cycle: list) -> None:
        """
        Draw all points from the given cycle on the canvas.

        Input:
         * cycle: list[Point]
        """
        for index, point in enumerate(cycle):
            self.draw_point(point)
            if index != len(cycle)-1:
                self.draw_line(point, cycle[index+1])
            else:
                self.draw_line(point, cycle[0])

    def show_perm(self):
        """
        Show the canvas as long as somebody close it.
        """
        stop = False
        while not stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop = True
            pygame.display.update()

    def show_temp(self):
        """
        Show the canvas one time.
        """
        pygame.display.update()

    def clear(self):
        """
        Clear the canvas.
        """
        self._surface.fill(self._back_color)


def draw_best_distances(distances: list, times=None):
    """
    Draw a graph with the best distances.

    Input:
     * distances: list[float]
    """
    plt.title("The best distances")
    plt.xlabel("generations")
    plt.xticks(range(0, len(distances)+1, len(distances)//10))
    plt.ylabel("distance")
    if times is not None:
        plt.plot(list(range(len(distances))), times, "-")
    for index, distance in enumerate(distances):
        plt.scatter(index, distance, alpha=0.3, color="blue")
    plt.show()


def draw_distances(all_distances: list):
    """
    Draw a graph with the best distances.

    Input:
     * all_distances: list[list[Point]]
    """
    plt.title("All distances")
    plt.xlabel("generations")
    plt.xticks(range(0, len(all_distances)+1, len(all_distances)//10))
    plt.ylabel("distance")
    x_list = []
    y_list = []
    for index, distances in enumerate(all_distances):
        for distance in distances:
            x_list.append(index)
            y_list.append(all_distance(distance))
    plt.scatter(x_list, y_list, alpha=0.3, color="blue")
    plt.show()

