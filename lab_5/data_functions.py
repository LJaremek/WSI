import matplotlib.pyplot as plt
from numpy import array


def print_number(number: array) -> None:
    for row in number:
        for el in row:
            el = round(float(el / 255), 1)
            if el < 0.5:
                print(".", end=" ")
            elif 0.5 < el < 1.0:
                print("x", end=" ")
            else:
                print("#", end=" ")
        print()


def show_number(number: array) -> None:
    plt.imshow(number, cmap=plt.cm.binary)
    plt.show()


def make_tuple(number: int) -> tuple:
    return [0.0 if i != number else 1.0 for i in range(10)]
