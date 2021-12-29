import matplotlib.pyplot as plt
import numpy as np


def cost_derivative(output_activation: np.array, y: np.array) -> np.array:
    return output_activation - y


def print_number(number: np.array) -> None:
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


def show_number(number: np.array) -> None:
    plt.imshow(number, cmap=plt.cm.binary)
    plt.show()


def make_output(number: int) -> np.array:
    n = np.zeros((10, 1))
    n[number][0] = 1.0
    return n


def draw_frequency_histogram(labels):
    u = np.unique(labels, return_counts=True)
    data = {str(x): u[1][x] for x in range(10)}
    names = list(data.keys())
    values = list(data.values())

    plt.ylabel("Image count")
    plt.xlabel("Digit class")

    plt.bar(names, values)
    plt.show()


def draw_network_epochs(train_epochs, test_epochs):
    plt.xticks(range(0, len(train_epochs)))

    plt.plot(train_epochs)
    plt.plot(test_epochs)
    plt.title("model accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epoch")
    plt.legend(["train", "val"], loc="upper left")
    plt.show()
