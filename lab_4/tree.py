from __future__ import annotations

from logic import *


class Node:
    def __init__(self,
                 label: str,
                 value: str,
                 count: int,
                 parent: Node = None,
                 children: list = None):
        self._label = label
        self._value = value
        self._count = count
        self._parent = parent
        self.set_children(children)

    def __str__(self) -> str:
        return f"{self._key} -> {self._value}"

    def __repr__(self) -> str:
        return str(self._value)

    def get_label(self) -> str:
        return self._label

    def get_value(self) -> Node:
        return self._value
    
    def get_count(self) -> int:
        return self._count

    def get_parent(self) -> Node:
        return self._parent

    def get_children(self) -> list:
        return self._children
    
    def set_label(self, new_label: str) -> None:
        self._label = new_label
        
    def set_value(self, new_value: str) -> None:
        self._value = new_value
        
    def set_count(self, new_count: int) -> None:
        self._count = new_count

    def set_parent(self, parent: Node) -> None:
        self._parent = parent
        # parent.add_child(self)

    def set_children(self, children: list) -> None:
        self._children = []

        if children is None:
            return

        for child in children:
            child = Node(child, self)
            self.add_child(child)
    
    def add_child(self, new_child: Node) -> None:
        self._children.append(new_child)

    def leaf(self) -> bool:
        return self._children == []


class DecisionTree:
    def __init__(self, data_frame: list):
        self._df = data_frame
        self._main_node = None
        self._indexes = list(range(len(data_frame[0])-1))

    def get_data_frame(self) -> list:
        return self._df

    def get_main_node(self) -> Node:
        return self._main_node

    def predict(self, row: list) -> str:
        pass

    def _get_entropies(self, data_frame: DataFrame) -> list:
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

    def _build_leaves(self, key: str, parent: Node, data_frame: list) -> None:
        values = get_unique_values(0, data_frame)
        for value in values:
            new_leaf = Node(key, value, parent, None)
            parent.add_child(new_leaf)

    def _build_node(self,
                    key: str, value,
                    parent: Node, data_frame: list) -> None:
        entropies = self._get_entropies(data_frame)
        the_best_index = self._get_max_entropy(entropies)[0]
        children = devide_data_frame(the_best_index, data_frame)

        the_node = Node(key, value, parent, None)
        parent.add_child(the_node)

        for child in children:
            key = list(child.keys())[0]
            frame = child[key]
            if i(0, frame) == 0 or len(frame[0]) == 1:  # liść
                self._build_leaves(key, self._main_node, frame)
            else:
                self._build_node(key, the_best_index, self._main_node, frame)

    def build_tree(self) -> None:
        entropies = self._get_entropies(self._df)
        the_best_index = self._get_max_entropy(entropies)[0]
        children = devide_data_frame(the_best_index, self._df)

        self._main_node = Node("NULL", the_best_index, None, None)

        for child in children:
            key = list(child.keys())[0]
            frame = child[key]
            if i(0, frame) == 0:  # liść
                self._build_leaves(key, self._main_node, frame)
            else:
                self._build_node(key, the_best_index, self._main_node, frame)

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
    df = DataFrame(data, ["x1", "x2", "y"])
    tree = DecisionTree(df)
    tree.build_tree()
    
    # tree.print_tree()
    print(tree.get_main_node())
    [print(child) for child in tree.get_main_node().get_children()]
