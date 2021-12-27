from typing import List, Tuple

import idx2numpy
import numpy as np
import matplotlib.pyplot as plt

from network import Network

all_data_file = "dataset/train-images.idx3-ubyte"
all_data = idx2numpy.convert_from_file(all_data_file)
all_labl_file = "dataset/train-labels.idx1-ubyte"
all_labl = idx2numpy.convert_from_file(all_labl_file)

NETWORK_INPUT_SIZE = all_data[0].flatten().size  # number of pixels in photo
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


def make_output(number: int) -> np.array:
    n = np.zeros((10, 1))
    n[number][0] = 1.0
    return n


def main() -> None:
    network = Network([NETWORK_INPUT_SIZE, 50, 50, NETWORK_OUTPUT_SIZE])

    data = all_data.copy()
    # np.random.shuffle(data)
    # data = all_data[:10000]

    to_split = int(len(data)*0.8)
    train_data = data[:to_split]
    test_data = data[to_split:]

    BATCH_SIZE = 16

    for i in range(0, len(train_data-BATCH_SIZE), BATCH_SIZE):

        mini_batch: List[Tuple[np.array, np.array]] = []
        for index, number in enumerate(train_data[i:i + BATCH_SIZE]):
            pixels: np.array = number.flatten()/255
            pixels = np.reshape(pixels, (784, 1))
            result: int = int(all_labl[index])
            results: np.array = make_output(result)

            mini_batch.append(
                (pixels, results)
            )

        network.train(mini_batch)

    for index, number in enumerate(test_data):
        pixels: np.array = number.flatten()/255
        pixels_2 = np.reshape(pixels, (784, 1))

        result: int = int(all_labl[index + to_split])

        output = network.feed_forward(pixels_2)

        print(result == output.argmax(),
              result, output.argmax())


if __name__ == "__main__":
    main()
