from __future__ import annotations

from typing import List, Tuple

import numpy as np
from numpy.random import uniform

import activation_functions
import helpers


class NeuronLayer:
    def __init__(self, number_of_neurons: int, number_of_input_neurons: int) -> None:
        self._number_of_neurons = number_of_neurons
        self._number_of_input_neurons = number_of_input_neurons

        self._weights = uniform(
            low=-1.0,
            high=1.0,
            size=(self._number_of_neurons, self._number_of_input_neurons),
        )

        self._biases = uniform(low=-0.2, high=0.2, size=(self._number_of_neurons, 1))

        self._z = np.zeros((self._number_of_neurons, 1))
        self._a = np.zeros((self._number_of_neurons, 1))

    def feed_forward(self, inputs: np.array) -> np.array:
        self._z = np.dot(self._weights, inputs) + self._biases
        self._a = activation_functions.sigmoid(self._z)
        return self._a

    @property
    def biases(self) -> np.array:
        return self._biases

    @property
    def weights(self) -> np.array:
        return self._weights

    @property
    def a(self) -> np.array:
        return self._a

    @property
    def z(self) -> np.array:
        return self._z

    def set_biases(self, new_biases: np.array) -> None:
        self._biases = new_biases

    def set_weights(self, new_weights: np.array) -> None:
        self._weights = new_weights


class Network:
    def __init__(
        self,
        list_of_numbers_of_neurons: List[int],
        learning_rate: float = 0.01,
    ) -> None:
        self._layers: List[NeuronLayer] = []
        self._list_of_numbers_of_neurons: List[int] = list_of_numbers_of_neurons
        self._learning_rate = learning_rate

        for index in range(1, len(self._list_of_numbers_of_neurons)):
            layer = NeuronLayer(
                self._list_of_numbers_of_neurons[index],
                self._list_of_numbers_of_neurons[index - 1],
            )

            self._layers.append(layer)

    def feed_forward(self, inputs: np.array) -> np.array:
        last_outputs = inputs.copy()

        for layer_index in range(len(self._layers)):
            last_outputs = self._layers[layer_index].feed_forward(last_outputs)

        return last_outputs

    def get_layer(self, layer_index: int) -> NeuronLayer:
        return self._layers[layer_index]

    def train(self, mini_batch: List[Tuple[np.array, np.array]]) -> None:
        delta_biases = [np.zeros(layer.biases.shape) for layer in self._layers]
        delta_weights = [np.zeros(layer.weights.shape) for layer in self._layers]

        for sample in mini_batch:
            x, y = sample

            errors = self.backprop(x, y)
            (
                delta_weights_backprop,
                delta_biases_backprop,
            ) = self.get_delta_weights_and_biases_from_errors(x, errors)

            for layer_index in range(len(self._layers)):
                delta_biases[layer_index] += delta_biases_backprop[layer_index]
                delta_weights[layer_index] += delta_weights_backprop[layer_index]

        for layer_index in range(len(self._layers)):
            delta_biases[layer_index] *= 1.0 / len(mini_batch)
            delta_biases[layer_index] *= self._learning_rate

            delta_weights[layer_index] *= 1.0 / len(mini_batch)
            delta_weights[layer_index] *= self._learning_rate

        self.update_weights_and_biases(delta_weights, delta_biases)

    def backprop(self, inputs: np.array, y: np.array) -> List[np.array]:
        self.feed_forward(inputs)
        last_layer = self._layers[-1]

        cost_derivative = helpers.cost_derivative(last_layer.a, y)
        sigmoid_derivative = activation_functions.sigmoid_derivative(last_layer.z)

        errors = []
        delta: np.array = cost_derivative * sigmoid_derivative
        errors.insert(0, delta)

        for layer_index in range(len(self._layers) - 2, -1, -1):
            cost_derivative = np.dot(self._layers[layer_index + 1].weights.T, delta)
            sigmoid_derivative = activation_functions.sigmoid_derivative(
                self._layers[layer_index].z
            )

            delta = cost_derivative * sigmoid_derivative
            errors.insert(0, delta)

        return errors

    def get_delta_weights_and_biases_from_errors(self, inputs: np.array, errors: List[np.array]):
        to_change_biases = list()
        to_change_weights = list()

        for layer_index in range(len(self._layers) - 1, -1, -1):
            delta = errors[layer_index]
            to_change_biases.insert(0, delta.copy())

            if layer_index == 0:
                to_change_weights.insert(0, np.dot(delta, inputs.T))
            else:
                to_change_weights.insert(0, np.dot(delta, self._layers[layer_index - 1].a.T))

        return to_change_weights, to_change_biases

    def update_weights_and_biases(
        self, delta_weights: List[np.array], delta_biases: List[np.array]
    ) -> None:
        for index, layer in enumerate(self._layers):
            layer.set_biases(layer.biases - delta_biases[index])
            layer.set_weights(layer.weights - delta_weights[index])

    def cost(self, y: np.array):
        return 0.5 * (y - self._layers[-1].a) ** 2

    def final_cost(self, y: np.array):
        return sum(x for x in self.cost(y))
