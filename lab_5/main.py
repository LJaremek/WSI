from time import perf_counter
from typing import List, Tuple

import idx2numpy
import numpy as np

import helpers
from network import Network

all_images_file = "dataset/train-images.idx3-ubyte"
all_images = idx2numpy.convert_from_file(all_images_file)
all_labels_file = "dataset/train-labels.idx1-ubyte"
all_labels = idx2numpy.convert_from_file(all_labels_file)


def main() -> None:
    network_input_size = all_images[0].flatten().size  # number of pixels in photo
    network_output_size = 10  # numbers in <0, 9>

    network = Network([network_input_size, 50, network_output_size], learning_rate=0.1)

    data = [(image, label) for image, label in zip(all_images, all_labels)]
    np.random.shuffle(data)

    to_split = int(len(data) * 0.8)
    train_data = data[:to_split]
    test_data = data[to_split:]

    number_of_epochs = 50
    batch_size = 16

    for epoch in range(number_of_epochs):
        epoch_start = perf_counter()
        print(f"Epoch {epoch}")

        np.random.shuffle(train_data)

        for i in range(0, len(train_data) - batch_size, batch_size):
            mini_batch: List[Tuple[np.array, np.array]] = []

            for index, number in enumerate(train_data[i : i + batch_size]):
                number_pixels, number_label = number
                pixels: np.array = number_pixels.flatten() / 255
                pixels = np.reshape(pixels, (784, 1))
                result: int = int(number_label)
                results: np.array = helpers.make_output(result)

                mini_batch.append((pixels, results))

            network.train(mini_batch)

        epoch_end = perf_counter()
        print(f"Elapsed time: {epoch_end - epoch_start:.2f}")

        good_sum = 0
        for index, number in enumerate(test_data):
            number_pixels, number_label = number

            pixels: np.array = number_pixels.flatten() / 255
            pixels_2 = np.reshape(pixels, (784, 1))

            result: int = int(number_label)
            output = network.feed_forward(pixels_2)
            good_sum += result == output.argmax()

        print(f"{good_sum} / {len(test_data)}")


if __name__ == "__main__":
    main()
