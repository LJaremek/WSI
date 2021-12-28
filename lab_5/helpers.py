import numpy as np


def cost_derivative(output_activation: np.array, y: np.array) -> np.array:
    return output_activation - y
