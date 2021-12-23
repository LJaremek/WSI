from __future__ import annotations

import numpy as np
from numpy.random import uniform
from typing import List
from random import randint

from activation_functions import sigmoid

"""

0   1   2   3
--------------
    b0
a1      c1
    b1
a2      c2
    b2
a3      c3
    b4

o - Neuron


w_a1 = [ a1b1, a1b2 ]
w_a2 = [ a2b1, a2b2 ]
w_a3 = [ a3b1, a3b2 ]

b_a1 = [ x ]
b_a2 = [ x ]
b_a3 = [ x ]

Przyklad:

Wejście
a1 = 0.2
a2 = 0.3
a3 = 0.9

Neuron b0:
weights = [ a1b0, a2b0, a3b0 ]

"""


def random_numbers(n: int) -> np.array:
    return uniform(low=-1.0, high=1.0, size=(n,))


class Neuron:
    def __init__(self, number_of_weights: int) -> None:
        self._weights: List[float] = random_numbers(number_of_weights)
        self._bias: float = randint(0, 10)/10
        self._activation_function = sigmoid
        self._output = None
        self._inputs = None

    def calculate(self, inputs: List[float]) -> float:
        self._inputs = inputs
        sum_output: float = 0.0
        for i in range(len(inputs)):
            sum_output += inputs[i] * self._weights[i]

        sum_output += self._bias
        self._output = self._activation_function(sum_output)
        return self._output

    @property
    def output(self):
        return self._output


class NeuronLayer:
    def __init__(self,
                 number_of_neurons: int,
                 number_of_input_neurons: int) -> None:
        self._number_of_neurons = number_of_neurons
        self._number_of_input_neurons = number_of_input_neurons

        self._neurons: List[Neuron] = []
        for i in range(number_of_neurons):
            self._neurons.append(
                Neuron(number_of_input_neurons)
            )

    def feed_forward(self, inputs: List[float]) -> List[float]:
        output: List[float] = []
        for i in range(len(self._neurons)):
            output.append(self._neurons[i].calculate(inputs))

        return output

    def cost_error(self, outputs: List[float]) -> List[float]:
        cost_output = []
        for i in range(len(self._neurons)):
            cost_output.append(
                (outputs[i] - self._neurons[i].output) ** 2
            )

        return cost_output

    @property
    def number_of_neurons(self) -> int:
        return self._number_of_neurons


class Network:
    def __init__(self, list_of_numbers_of_neurons: List[int]) -> None:

        self._layers: List[NeuronLayer] = []
        self._list_of_numbers_of_neurons: List[int] = \
            list_of_numbers_of_neurons

        for i in range(1, len(self._list_of_numbers_of_neurons)):
            layer = NeuronLayer(self._list_of_numbers_of_neurons[i],
                                self._list_of_numbers_of_neurons[i-1])

            self._layers.append(layer)

    def feed_forward(self, inputs: List[float]) -> List[float]:
        last_outputs = inputs

        for i in range(len(self._layers)):
            last_outputs = self._layers[i].feed_forward(last_outputs)

        return last_outputs

    def get_layer(self, layer_index: int) -> NeuronLayer:
        return self._layers[layer_index]


def main():
    # input
    inputs = [0.5, 0.2, 0.1]
    nn = Network([3, 2, 2])

    output = nn.feed_forward(inputs)
    print(output)


if __name__ == "__main__":
    main()
