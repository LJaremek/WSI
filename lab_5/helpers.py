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


def draw_network_epochs(measurements, learning_rate):
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    epochs = len(measurements["accuracy"]["train"])

    fig.suptitle(f"Lr={learning_rate}", fontsize=16)

    axes[0, 0].plot(measurements["accuracy"]["train"])
    axes[0, 0].plot(measurements["accuracy"]["test"])
    axes[0, 0].set_title("accuracy")
    axes[0, 0].set_xticks(range(0, epochs))
    axes[0, 0].set_yticks([x/10 for x in range(0, 11)])

    axes[0, 1].plot(measurements["recall"]["train"])
    axes[0, 1].plot(measurements["recall"]["test"])
    axes[0, 1].set_title("recall")
    axes[0, 1].set_xticks(range(0, epochs))
    axes[0, 1].set_yticks([x/10 for x in range(0, 11)])

    axes[1, 0].plot(measurements["cost"]["train"])
    axes[1, 0].plot(measurements["cost"]["test"])
    axes[1, 0].set_title("cost")
    axes[1, 0].set_xlabel("epochs")
    axes[1, 0].set_xticks(range(0, epochs))
    axes[1, 0].set_yticks([x/10 for x in range(0, 11)])

    axes[1, 1].plot(measurements["precision"]["train"])
    axes[1, 1].plot(measurements["precision"]["test"])
    axes[1, 1].set_title("precision")
    axes[1, 1].set_xlabel("epochs")
    axes[1, 1].set_xticks(range(0, epochs))
    axes[1, 1].set_yticks([x/10 for x in range(0, 11)])

    fig.legend(["train", "val"], loc="upper left")
    plt.show()
