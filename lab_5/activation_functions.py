from math import e, erf, log


def binary(x: float) -> float:
    if x < 0:
        return 0.0
    return 1


def gaussian(x: float) -> float:
    return e ** (-(x ** 2))


def gelu(x: float) -> float:
    return 1 / 2 * x * (1 + erf(x / (2 ** (1 / 2))))


def h_tan(x: float) -> float:
    return (e ** x - e ** (-x)) / (e ** x + e ** (-x))


def identity(x: float) -> float:
    return x


def prelu(x: float) -> float:
    if x < 0:
        return 0.01 * x
    return x


def relu(x: float) -> float:
    return max(0.0, x)


def sigmoid(x):
    return 1.0 / (1.0 + e ** (-x))


def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))


def silu(x: float) -> float:
    return x / (1 + e ** (-x))


def softplus(x: float) -> float:
    return log(1 + e ** x, e)
