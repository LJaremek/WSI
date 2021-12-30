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

test_images_file = "dataset/t10k-images.idx3-ubyte"
test_images = idx2numpy.convert_from_file(test_images_file)
test_labels_file = "dataset/t10k-labels.idx1-ubyte"
test_labels = idx2numpy.convert_from_file(test_labels_file)


def calculate(network: Network,
              data,
              matrix: list) -> int:
    good_sum = 0
    for _, number in enumerate(data):
        pixels, number_label = number
        output = network.feed_forward(pixels)
        good_sum += number_label == output.argmax()

        result: int = int(number_label)
        matrix[result][output.argmax()] += 1

    return good_sum


def make_confusion_matrix(matrix) -> dict:
    confusion_matrix = {}
    for number in range(10):
        confusion_matrix[number] = {"tp": 0, "tn": 0, "fn": 0, "fp": 0}

    for number in range(10):
        confusion_matrix[number]["tp"] = matrix[number][number]
        confusion_matrix[number]["tn"] = sum(
            [row[i] for i, row in enumerate(matrix) if i != number]
        )
        confusion_matrix[number]["fp"] = sum(
            [row[number] for i, row in enumerate(matrix) if i != number]
        )
        confusion_matrix[number]["fn"] = sum(
            matrix[number][:number] + matrix[number][number + 1:]
        )

    return confusion_matrix


def get_recall_fallout_precision_accuracy(
                                          confusion_matrix: dict
                                         ) -> Tuple[float, float, float, float]:
    for key in confusion_matrix:
        try:
            recall = sum([confusion_matrix[key]["tp"]]) / (
                sum([confusion_matrix[key]["tp"]]) +
                sum([confusion_matrix[key]["fn"]])
            )
        except ZeroDivisionError:
            recall = -1
        try:
            fallout = sum([confusion_matrix[key]["fp"]]) / (
                sum([confusion_matrix[key]["fp"]]) +
                sum([confusion_matrix[key]["tn"]])
            )
        except ZeroDivisionError:
            fallout = -1
        try:
            precision = sum([confusion_matrix[key]["tp"]]) / (
                sum([confusion_matrix[key]["tp"]]) +
                sum([confusion_matrix[key]["fp"]])
            )
        except ZeroDivisionError:
            precision = -1
        try:
            accuracy = (sum([confusion_matrix[key]["tp"]]) +
                        sum([confusion_matrix[key]["tn"]])) / (
                sum([confusion_matrix[key]["tp"]])
                + sum([confusion_matrix[key]["fn"]])
                + sum([confusion_matrix[key]["tn"]])
                + sum([confusion_matrix[key]["fn"]])
            )
        except ZeroDivisionError:
            accuracy = -1

    return recall, fallout, precision, accuracy


def main() -> None:
    # number of pixels in photo
    network_input_size = all_images[0].flatten().size

    # numbers in <0, 9>
    network_output_size = 10

    network = Network([network_input_size, 10, 10, network_output_size],
                      learning_rate=0.1)

    train_data = [
        ((image.flatten() / 255).reshape((network_input_size, 1)), int(label))
        for image, label in zip(all_images, all_labels)
    ]
    np.random.shuffle(train_data)

    test_data = [
        ((image.flatten() / 255).reshape((network_input_size, 1)), int(label))
        for image, label in zip(test_images, test_labels)
    ]
    np.random.shuffle(test_data)

    number_of_epochs = 20
    batch_size = 16

    epochs_test_data = []
    epochs_train_data = []

    train_matrix, test_matrix = [
                                    [[0 for _ in range(10)] for _ in range(10)]
                                    for _ in range(2)
                                ]

    for epoch in range(number_of_epochs):
        epoch_start = perf_counter()
        print(f"Epoch {epoch}")

        np.random.shuffle(train_data)

        for i in range(0, len(train_data) - batch_size, batch_size):
            mini_batch: List[Tuple[np.array, np.array]] = []

            for _, number in enumerate(train_data[i: i + batch_size]):
                pixels, number_label = number
                results: np.array = helpers.make_output(number_label)
                mini_batch.append((pixels, results))

            network.train(mini_batch)

        epoch_end = perf_counter()
        print(f"Elapsed time: {epoch_end - epoch_start:.2f}")

        test_ok = calculate(network, test_data, test_matrix)
        train_ok = calculate(network, train_data, train_matrix)

        test_confusion_matrix = make_confusion_matrix(test_matrix)
        train_confusion_matrix = make_confusion_matrix(train_matrix)

        test_paremeters = (
            get_recall_fallout_precision_accuracy(test_confusion_matrix)
        )
        train_paremeters = (
            get_recall_fallout_precision_accuracy(train_confusion_matrix)
        )

        parameters = ["recall   ", "fallout   ", "precision", "accuracy"]
        print("PARAM\t\tTRAIN\tTEST")
        for index, name in enumerate(parameters):
            print(name,
                  round(train_paremeters[index], 2),
                  round(test_paremeters[index], 2),
                  sep="\t"
                  )

        # epochs_train_data.append((recall, fallout, precision, accuracy))

        epochs_train_data.append(train_ok / len(train_data))
        epochs_test_data.append(test_ok / len(test_data))

        msg = f"Train: {train_ok} / {len(train_data)} |"
        msg += f" Test: {test_ok} / {len(test_data)}\n"
        print(msg)

    helpers.draw_network_epochs(epochs_train_data, epochs_test_data)


if __name__ == "__main__":
    main()
