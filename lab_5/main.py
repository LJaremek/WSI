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

LIST_MATRIX = List[List[int]]


def create_confusion_matrix_and_cost(network: Network, data) -> Tuple[LIST_MATRIX, float]:
    confusion_matrix = [[0 for _ in range(10)] for _ in range(10)]
    cost_sum = 0
    for _, number in enumerate(data):
        pixels, number_label = number
        output = network.feed_forward(pixels)
        result: int = int(number_label)
        results: np.array = helpers.make_output(number_label)
        cost_sum += network.final_cost(results)

        confusion_matrix[result][output.argmax()] += 1

    cost = cost_sum / len(data)
    return confusion_matrix, cost


def create_measurements(matrix: LIST_MATRIX) -> dict:
    measurements = {}
    for number in range(10):
        measurements[number] = {"tp": 0, "tn": 0, "fn": 0, "fp": 0}

    for number in range(10):
        measurements[number]["tp"] = matrix[number][number]
        measurements[number]["tn"] = sum([row[i] for i, row in enumerate(matrix) if i != number])
        measurements[number]["fp"] = sum(
            [row[number] for i, row in enumerate(matrix) if i != number]
        )
        measurements[number]["fn"] = sum(matrix[number][:number] + matrix[number][number + 1 :])

    return measurements


def get_measurements(
    measurement: dict,
) -> Tuple[float, float, float, float]:
    for key in measurement:
        try:
            recall = sum([measurement[key]["tp"]]) / (
                sum([measurement[key]["tp"]]) + sum([measurement[key]["fn"]])
            )
        except ZeroDivisionError:
            recall = -1
        try:
            fallout = sum([measurement[key]["fp"]]) / (
                sum([measurement[key]["fp"]]) + sum([measurement[key]["tn"]])
            )
        except ZeroDivisionError:
            fallout = -1
        try:
            precision = sum([measurement[key]["tp"]]) / (
                sum([measurement[key]["tp"]]) + sum([measurement[key]["fp"]])
            )
        except ZeroDivisionError:
            precision = -1
        try:
            accuracy = (sum([measurement[key]["tp"]]) + sum([measurement[key]["tn"]])) / (
                sum([measurement[key]["tp"]])
                + sum([measurement[key]["fn"]])
                + sum([measurement[key]["tn"]])
                + sum([measurement[key]["fn"]])
            )
        except ZeroDivisionError:
            accuracy = -1

    return recall, fallout, precision, accuracy


def prepare_data(images, labels) -> List[Tuple[np.array, int]]:
    network_input_size = images[0].flatten().size

    return [
        ((image.flatten() / 255).reshape((network_input_size, 1)), int(label))
        for image, label in zip(images, labels)
    ]


def main() -> None:
    # number of pixels in photo
    network_input_size = all_images[0].flatten().size

    # numbers in <0, 9>
    network_output_size = 10

    learning_rate = 0.1

    network = Network([network_input_size, 5, network_output_size], learning_rate=learning_rate)

    train_data = prepare_data(all_images, all_labels)
    np.random.shuffle(train_data)

    test_data = prepare_data(test_images, test_labels)
    np.random.shuffle(test_data)

    number_of_epochs = 5
    batch_size = 16

    parameters = ["recall", "fallout", "precision", "accuracy"]
    all_measurements = {parameter: {"train": [], "test": []} for parameter in parameters}
    all_measurements["cost"] = {"train": [], "test": []}

    for epoch in range(number_of_epochs):
        epoch_start = perf_counter()
        print(f"Epoch {epoch}")

        np.random.shuffle(train_data)

        for i in range(0, len(train_data) - batch_size, batch_size):
            mini_batch: List[Tuple[np.array, np.array]] = []

            for _, number in enumerate(train_data[i : i + batch_size]):
                pixels, number_label = number
                results: np.array = helpers.make_output(number_label)
                mini_batch.append((pixels, results))

            network.train(mini_batch)

        epoch_end = perf_counter()
        print(f"Elapsed time: {epoch_end - epoch_start:.2f}")

        test_confusion_matrix, cost_test = create_confusion_matrix_and_cost(network, test_data)
        train_confusion_matrix, cost_train = create_confusion_matrix_and_cost(network, train_data)

        all_measurements["cost"]["train"].append(cost_train)
        all_measurements["cost"]["test"].append(cost_test)

        test_measurement = create_measurements(test_confusion_matrix)
        train_measurement = create_measurements(train_confusion_matrix)

        test_parameters = get_measurements(test_measurement)
        train_parameters = get_measurements(train_measurement)

        for index, name in enumerate(parameters):
            all_measurements[name]["train"].append(train_parameters[index])
            all_measurements[name]["test"].append(test_parameters[index])

        print(all_measurements)

    helpers.draw_network_epochs(all_measurements, learning_rate)


if __name__ == "__main__":
    main()
