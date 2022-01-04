from random import randint

from numpy import (array, array_equal, delete, flip, fliplr, flipud, insert,
                   unique)

image = array(
    [
        array([0, 0, 0, 0, 0]),
        array([0, 0, 0, 0, 0]),
        array([0, 1, 1, 1, 0]),
        array([0, 1, 0, 1, 0]),
        array([0, 1, 1, 1, 0]),
        array([0, 0, 0, 1, 0]),
        array([0, 1, 1, 1, 0]),
    ]
)


def _check_row(image: array, index: int) -> bool:
    return bool(len(unique(image[index])) == 1 and unique(image[index]) == array([0]))


def _check_column(image: array, index: int) -> bool:
    for row in image:
        if row[index] != 0:
            return False
    return True


def _insert_row(image: array, index: int) -> array:
    if index == -1:
        index = len(image)
    image = insert(image, index, array([0 for _ in range(len(image[0]))]), axis=0)

    if index == 0:
        image = delete(image, -1, axis=0)
    elif index + 1 == len(image):
        image = delete(image, 0, axis=0)

    return image


def _insert_colunn(image: array, index: int) -> array:
    image = insert(image, index, 0, axis=1)

    if index == 0:
        image = delete(image, -1, axis=1)
    elif index == -1:
        image = delete(image, 0, axis=1)

    return image


def augmentation(images: array, labels: array) -> array:
    new_images = []
    new_labels = []
    for index in range(len(images)):
        image = images[index].copy()
        new_image = image.copy()
        label = labels[index]

        if label in (8, 0):
            los = randint(0, 2)

            if los == 0:
                new_image = fliplr(new_image)
            elif los == 1:
                new_image = flipud(new_image)

        if label in (6, 9):
            los = randint(0, 1)

            if los == 0:
                new_image = flip(new_image)
                if label == 6:
                    label = 9
                else:
                    label = 6

        los = randint(1, 4)
        if los == 1:
            while _check_column(new_image, -1) and _check_column(new_image, -2):
                new_image = _insert_colunn(new_image, 0)

        if los == 2:
            while _check_column(new_image, 0) and _check_column(new_image, 1):
                new_image = _insert_colunn(new_image, -1)

        if los == 3:
            while _check_row(new_image, -1) and _check_row(new_image, -2):
                new_image = _insert_row(new_image, 0)

        if los == 4:
            while _check_row(new_image, 0) and _check_row(new_image, 1):
                new_image = _insert_row(new_image, -1)

        if not array_equal(image, new_image):
            new_images.append(new_image)
            new_labels.append(label)

    return new_images, new_labels


if __name__ == "__main__":
    import idx2numpy

    all_images_file = "dataset/train-images.idx3-ubyte"
    all_images = idx2numpy.convert_from_file(all_images_file)
    all_labels_file = "dataset/train-labels.idx1-ubyte"
    all_labels = idx2numpy.convert_from_file(all_labels_file)
    images, labels = augmentation(all_images[:20], all_labels[:20])
    print(len(images), len(labels))
    print(labels)
    print(list(all_labels[:20]))
