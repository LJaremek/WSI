import idx2numpy
import numpy as np
import matplotlib.pyplot as plt

from network import Network

train_data_file = "dataset/train-images.idx3-ubyte"
train_data = idx2numpy.convert_from_file(train_data_file)
train_labl_file = "dataset/train-labels.idx1-ubyte"
train_labl = idx2numpy.convert_from_file(train_labl_file)

NETWORK_INPUT_SIZE = train_data[0].flatten().size  # number of pixels in photo
NETWORK_OUTPUT_SIZE = 10  # numbers in <0, 9>


def print_number(number: np.array) -> None:
    for row in number:
        for el in row:
            el = round(float(el/255), 1)
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


def main() -> None:
    network = Network([NETWORK_INPUT_SIZE, 50, NETWORK_OUTPUT_SIZE])

    for index, number in enumerate(train_data):
        pixels: np.array = number.flatten()/255
        result: int = int(train_labl[index])

        output = network.feed_forward(pixels)

        w = [0.0] * 10
        w[result] = 1.0

        cost_errors = network._layers[-1].cost_error(w)
        print(cost_errors)

        print(result == output.index(max(output)),
              result, output.index(max(output)))


if __name__ == "__main__":
    main()
