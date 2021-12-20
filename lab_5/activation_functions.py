from math import e


def relu(x: float) -> float:
    return max(0.0, x)


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + e**(-x))
