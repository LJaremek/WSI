import numpy as np

from network import Network

NETWORK_INPUT_SIZE = 2
NETWORK_OUTPUT_SIZE = 2


def get_xor_sample():
    x = np.random.randint(2, size=(2, 1))
    y = np.zeros((2, 1))

    result = x[0][0] ^ x[1][0]
    y[result][0] = 1.0
    return x, y


def main() -> None:
    network = Network([NETWORK_INPUT_SIZE, 2, NETWORK_OUTPUT_SIZE])

    batch_size = 4
    for j in range(100000):
        mini_batch = []
        for i in range(batch_size):
            mini_batch.append(get_xor_sample())

        network.train(mini_batch)

        x, y = get_xor_sample()
        out = network.feed_forward(x)
        print(y[0][0], y[1][0], " - ", out[0][0], out[1][0])

        result_index = out.argmax()
        z = np.zeros((2, 1))
        z[result_index] = 1.0

        print(y[0][0] == z[0][0] and y[1][0] == z[1][0])


if __name__ == "__main__":
    main()
