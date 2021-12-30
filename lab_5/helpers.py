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


def draw_network_epochs(measurements):
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    fig.suptitle('Sharing x per column, y per row')

    ((ax1, ax2), (ax3, ax4)) = axes

    epochs = len(measurements["accuracy"]["train"])
    plt.setp(axes, xticks=range(0, epochs))

    ax1.title.set_text("accuracy")
    ax1.legend(["train", "val"], loc="upper left")
    ax1.plot(measurements["accuracy"]["train"])
    ax1.plot(measurements["accuracy"]["test"])

    ax2.title.set_text("recall")
    ax2.legend(["train", "val"], loc="upper left")
    ax2.plot(measurements["recall"]["train"])
    ax2.plot(measurements["recall"]["test"])

    ax3.title.set_text("recall")
    ax3.legend(["train", "val"], loc="upper left")
    ax3.plot(measurements["recall"]["train"])
    ax3.plot(measurements["recall"]["test"])

    ax4.title.set_text("recall")
    ax4.legend(["train", "val"], loc="upper left")
    ax4.plot(measurements["recall"]["train"])
    ax4.plot(measurements["recall"]["test"])

    for ax in fig.get_axes():
        ax.label_outer()

    plt.title("")
    plt.show()
