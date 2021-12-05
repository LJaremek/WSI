from __future__ import annotations

from logic import *


class Node:
    def __init__(self, value,
                 parent: Node = None,
                 children: list = None):
        self._value = value
        self._parent = parent
        self.set_children(children)

    def __str__(self) -> str:
        return str(self._value)

    def __repr__(self) -> str:
        return str(self._value)

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
        self._children = []

        if children is None:
            return

        for child in children:
            child = Node(child, self)
            self.add_child(child)


class DecisionTree:
    def __init__(self, data_frame: list):
        self._df = data_frame
        self._main_node = None

    def get_data_frame(self) -> list:
        return self._df

    def get_main_node(self) -> Node:
        return self._main_node

    def predict(self, row: list) -> str:
        pass

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
        return sorted(entropies, key=lambda x: x[1])[-1]

    def _build_leaves(self, parent: Node, data_frame: list) -> None:
        values = get_unique_values(0, data_frame)
        for value in values:
            new_leaf = Node(value, parent, None)
            parent.add_child(new_leaf)
    
    def _build_node(self, parent: Node, data_frame: list) -> None:
        entropies = self._get_entropies(data_frame)
        the_best_index = self._get_max_entropy(entropies)[0]
        children = devide_data_frame(the_best_index, data_frame)
        print(children)

        the_node = Node(the_best_index, parent, None)
        parent.add_child(the_node)

        for child in children:
            if i(0, child) == 0 or len(child[0]) == 1:  # liść
                self._build_leaves(self._main_node, child)
            else:
                self._build_node(self._main_node, child)

    def build_tree(self) -> None:
        entropies = self._get_entropies(self._df)
        the_best_index = self._get_max_entropy(entropies)[0]
        children = devide_data_frame(the_best_index, self._df)
        for child in children:
            for row in child:
                print(row)
            print()

        self._main_node = Node(the_best_index, None, None)

        for child in children:
            if i(0, child) == 0:  # liść
                self._build_leaves(self._main_node, child)
            else:
                self._build_node(self._main_node, child)

    def print_tree(self) -> None:
        to_print = [(self._main_node, 0)]
        while to_print != []:
            node, deep = to_print.pop(0)
            for child in node.get_children():
                to_print.append((child, deep+1))
            print("\t"*deep, node)
            
            


if __name__ == "__main__":
    data = [["A", 1, 0],
            ["B", 1, 1],
            ["B", 2, 1],
            ["B", 2, 0],
            ["B", 3, 1]]
    # data = get_data_frame()
    for row in data:
        print(row)
    tree = DecisionTree(data)
    tree.build_tree()
    # tree.print_tree()
    # print(tree.get_main_node())
    # print(tree.get_main_node().get_children())
