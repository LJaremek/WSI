from __future__ import annotations

from logic import *


class Node:
    def __init__(self, value,
                 parent: Node = None,
                 children: list = None):
        self._value = value
        self._parent = parent
        self.set_children(children)

    def get_value(self) -> Node:
        return self._value

    def get_parent(self) -> Node:
        return self._parent

    def get_children(self) -> list:
        return self._children

    def set_value(self, value: Node) -> None:
        self._value = value

    def set_parent(self, parent: Node) -> None:
        self._parent = parent
        # parent.add_child(self)
        
    def add_child(self, new_child: Node) -> None:
        self._children.append(new_child)

    def set_children(self, children: list) -> None:
        if children is None:
            self._children = None
            return

        self._children = []
        for child in children:
            child = Node(child, self)
            self.add_child(child)


class DecisionTree:
    def __init__(self, data_frame: list):
        self._df = data_frame
        self._main_node = None

    def get_data_frame(self) -> list:
        return self._df
    
    def _get_entropies(self, data_frame: list) -> list:
        entropies = []
        for index in range(len(data_frame[0])-1):
            entropies.append((index, inf_gain(index, -1, data_frame)))
        return entropies
    
    def _get_max_entropy(self, entropies: list) -> tuple:
        """
        Return tuple with the highest entropy.
        
        Input:
         * entropies: list[tuple[index: int, entropy: float]]
        
        Output:
         * result: tuple[index: int, entropy: float]
        """
        return sorted(entropies, key=lambda x: x[1])[0]
    
    def _build_node(self, parent: Node, data_frame: list) -> None:
        entropies = self._get_entropies()
        the_best = self._get_max_entropy(entropies)[0]
        children = get_unique_values(the_best, self._df)

        the_node = Node(the_best, parent, None)
        parent.add_child(the_node)

        if True:
            pass

        for child in children:
            self._build_node(the_node, del_column(the_best, data_frame))

    def build_tree(self) -> None:
        entropies = self._get_entropies()
        the_best = self._get_max_entropy(entropies)[0]
        children = get_unique_values(the_best, self._df)
        self._main_node = Node(the_best, None, None)
        for children in self._main_node.get_children():
            self._build_node(self._main_node, del_column(the_best, self._df))


if __name__ == "__main__":
    data = [["A", 1, 0],
            ["B", 1, 1],
            ["B", 2, 1],
            ["B", 2, 0],
            ["B", 3, 1]]
    data = get_data_frame()
    for row in data:
        print(row)
    tree = DecisionTree(data)
    tree.build_tree()
