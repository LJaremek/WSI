# `if __name__ == "__main__":
#     print("Hello WSI!")
#     with open("t10k-labels.idx1-ubyte") as file:
#         for line in file:
#             print(line)`

import idx2numpy
import numpy as np
import matplotlib.pyplot as plt
file = "data/train-images.idx3-ubyte"
arr = idx2numpy.convert_from_file(file)
plt.imshow(arr[302], cmap=plt.cm.binary)
plt.show()
