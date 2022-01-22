import matplotlib.pyplot as plt

from data_reader import open_file

data = open_file()


def draw_count_plot() -> None:
    classes = [row[0] for row in data]
    values = [classes.count(label) for label in set(classes)]
    classes = list(set(classes))

    plt.bar(classes, values, color="maroon", width=0.4)

    plt.xlabel("Class names")
    plt.ylabel("Number of classes")
    plt.title("The number of classes in the data set")
    plt.show()


def draw_dependencies_plot(index_1: int, index_2: int) -> None:
    class_1 = []
    class_2 = []
    class_3 = []
    for row in data:
        if row[0] == "1":
            class_1.append((float(row[index_1]), float(row[index_2])))
        elif row[0] == "2":
            class_2.append((float(row[index_1]), float(row[index_2])))
        elif row[0] == "3":
            class_3.append((float(row[index_1]), float(row[index_2])))

    plt.plot([the_tuple[0] for the_tuple in class_1],
             [the_tuple[1] for the_tuple in class_1],
             "o",
             color="red",
             label="class 1")
    plt.plot([the_tuple[0] for the_tuple in class_2],
             [the_tuple[1] for the_tuple in class_2],
             "o",
             color="green",
             label="class 2")
    plt.plot([the_tuple[0] for the_tuple in class_3],
             [the_tuple[1] for the_tuple in class_3],
             "o",
             color="blue",
             label="class 3")

    plt.xlabel(f"Values of {index_1} attribute")
    plt.ylabel(f"Values of {index_2} attribute")
    plt.title("The influence of attributes on classes")
    plt.legend()
    plt.show()
