from math import pi, e


def mean(numbers: list[float]) -> float:
    """
    Calcute the mean of a list of floats.

    Input:
     * numbers: list[float]

    Output:
     * mean of the list
    """
    return sum(numbers)/float(len(numbers))


def standard_deviation(numbers: list[float]) -> float:
    """
    Caculate the standard deviation of a list with floats.

    Input:
     * numbers: list[float]

    Output:
     * standard deviation of the list
    """
    avg = mean(numbers)
    variance = sum([(x-avg)**2 for x in numbers]) / float(len(numbers)-1)
    return variance**(1/2)


def gaussian_probability(x: float, mean: float, stdev: float) -> float:
    """
    Calculate the Gaussian probability distribution function for the given
    x, mean and standard deviation.

    Input:
     * x: float
     * mean: float
     * stdev: float

    Output:
     * float
    """
    exp = e**((-1/2)*(((x-mean)/stdev)**2))
    return (1 / (stdev*((2*pi)**(1/2)))) * exp
