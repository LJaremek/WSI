from __future__ import annotations

import numpy as np
from numpy.random import uniform
from typing import List, Tuple

from activation_functions import sigmoid


def random_numbers(n: int) -> np.array:
    return uniform(low=-1.0, high=1.0, size=(n,))


def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))


def cost_derivative(output_activation: np.array, y: np.array) -> np.array:
    return output_activation - y


class NeuronLayer:
    def __init__(self,
                 number_of_neurons: int,
                 number_of_input_neurons: int) -> None:
        self.number_of_neurons = number_of_neurons
        self.number_of_input_neurons = number_of_input_neurons

        self.weights = uniform(low=-1.0, high=1.0, size=(self.number_of_neurons, self.number_of_input_neurons))
        self.biases = uniform(low=-0.2, high=0.2, size=(self.number_of_neurons, 1))

        self.z = np.zeros((self.number_of_neurons, 1))
        self.a = np.zeros((self.number_of_neurons, 1))

    def feed_forward(self, inputs: np.array) -> np.array:
        self.z = np.dot(self.weights, inputs) + self.biases
        self.a = sigmoid(self.z)
        return self.a


class Network:
    def __init__(self, list_of_numbers_of_neurons: List[int]) -> None:
        self.layers: List[NeuronLayer] = []
        self.list_of_numbers_of_neurons: List[int] = \
            list_of_numbers_of_neurons

        for i in range(1, len(self.list_of_numbers_of_neurons)):
            layer = NeuronLayer(self.list_of_numbers_of_neurons[i],
                                self.list_of_numbers_of_neurons[i - 1])

            self.layers.append(layer)

    def feed_forward(self, inputs: np.array) -> np.array:
        last_outputs = inputs.copy()

        for i in range(len(self.layers)):
            last_outputs = self.layers[i].feed_forward(last_outputs)

        return last_outputs

    def get_layer(self, layer_index: int) -> NeuronLayer:
        return self.layers[layer_index]

    def train(self, mini_batch: List[Tuple[np.array, np.array]]):
        delta_biases = [np.zeros(layer.biases.shape) for layer in self.layers]
        delta_weights = [np.zeros(layer.weights.shape) for layer in self.layers]

        for sample in mini_batch:
            x, y = sample

            delta_biases_backprop, delta_weights_backprop = self.backprop(x, y)

            for layer_index in range(len(self.layers)):
                delta_biases[layer_index] = delta_biases[layer_index] + delta_biases_backprop[layer_index]
                delta_weights[layer_index] = delta_weights[layer_index] + delta_weights_backprop[layer_index]

        for layer_index in range(len(self.layers)):
            delta_biases[layer_index] *= 1.0 / len(mini_batch)
            delta_biases[layer_index] *= 0.1

            delta_weights[layer_index] *= 1.0 / len(mini_batch)
            delta_weights[layer_index] *= 0.1

        self.update_weights_and_biases(delta_biases, delta_weights)

    def backprop(self, inputs: np.array, y: np.array):
        self.feed_forward(inputs)

        last_layer = self.layers[-1]

        c_d = cost_derivative(last_layer.a, y)
        s_d = sigmoid_derivative(last_layer.z)

        to_change_biases = list()
        to_change_weights = list()

        delta: np.array = c_d * s_d

        to_change_biases.insert(0, delta.copy())
        to_change_weights.insert(0, np.dot(delta, self.layers[-2].a.T))

        for l in range(len(self.layers) - 2, -1, -1):
            z = self.layers[l].z

            w1 = self.layers[l + 1].weights.T
            w2 = delta.copy()

            c_d2 = np.dot(w1, w2)
            s_d2 = sigmoid_derivative(z)

            delta = c_d2 * s_d2

            to_change_biases.insert(0, delta.copy())
            if l == 0:
                to_change_weights.insert(0, np.dot(delta, inputs.T))
            else:
                to_change_weights.insert(0, np.dot(delta, self.layers[l - 1].a.T))

        return to_change_biases, to_change_weights

    def update_weights_and_biases(self, delta_biases: List[np.array], delta_weights: List[np.array]):
        for index, layer in enumerate(self.layers):
            layer.biases = layer.biases - delta_biases[index]
            layer.weights = layer.weights - delta_weights[index]


def main():
    inputs = uniform(low=0.0, high=1.0, size=(3,))
    nn = Network([3, 2, 2])
    outputs = np.zeros(2)
    outputs[1] = 1.0

    nn.backprop(inputs, outputs)


if __name__ == "__main__":
    main()
