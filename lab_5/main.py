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


def calculate(network: Network, data):
    good_sum = 0
    for index, number in enumerate(data):
        pixels, number_label = number
        output = network.feed_forward(pixels)
        good_sum += number_label == output.argmax()

    return good_sum


def main() -> None:
    network_input_size = all_images[0].flatten().size  # number of pixels in photo
    network_output_size = 10  # numbers in <0, 9>

    network = Network([network_input_size, 10, 10, network_output_size], learning_rate=0.1)

    data = [
        ((image.flatten() / 255).reshape((network_input_size, 1)), int(label))
        for image, label in zip(all_images, all_labels)
    ]

    # data = sorted(data, key=lambda x: x[1])
    np.random.shuffle(data)

    to_split = int(len(data) * 0.8)
    train_data = data[:to_split]
    test_data = data[to_split:]

    number_of_epochs = 20
    batch_size = 16

    epochs_test_data = []
    epochs_train_data = []

    for epoch in range(number_of_epochs):
        epoch_start = perf_counter()
        print(f"Epoch {epoch}")

        np.random.shuffle(train_data)

        for i in range(0, len(train_data) - batch_size, batch_size):
            mini_batch: List[Tuple[np.array, np.array]] = []

            for index, number in enumerate(train_data[i : i + batch_size]):
                pixels, number_label = number
                results: np.array = helpers.make_output(number_label)
                mini_batch.append((pixels, results))

            network.train(mini_batch)

        epoch_end = perf_counter()
        print(f"Elapsed time: {epoch_end - epoch_start:.2f}")

        test_ok = calculate(network, test_data)
        train_ok = calculate(network, train_data)

        epochs_train_data.append(train_ok / len(train_data))
        epochs_test_data.append(test_ok / len(test_data))

        print(f"Train: {train_ok} / {len(train_data)} | Test: {test_ok} / {len(test_data)}")

    helpers.draw_network_epochs(epochs_train_data, epochs_test_data)


if __name__ == "__main__":
    main()
