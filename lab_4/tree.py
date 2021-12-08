from __future__ import annotations

from logic import *


class Node:
    def __init__(self,
                 label: str,
                 value: str, # y
                 count: int = 0,
                 parent: Node = None,
                 children: list = None):
        self._label = label
        self._value = value # y
        self._count = count
        self._parent = parent
        self.set_children(children)

    def __str__(self) -> str:
        return f"{self._label} -> {self._value}"

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
    def __init__(self, data_frame: DataFrame):
        self._df = data_frame
        self._main_node = None
        self._indexes = list(range(len(data_frame[0])-1))

    def get_data_frame(self) -> DataFrame:
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

    def _build_leaves(self, 
                      key: str, 
                      parent: Node, 
                      data_frame: DataFrame) -> None:
        # print("LEAF", key)
        # print(data_frame)
        values = get_unique_values(-1, data_frame)
        for value in values:
            new_leaf = Node(key, value, 0, parent, None)
            parent.add_child(new_leaf)

    def _build_node(self,
                    parent_title: str,
                    value,
                    parent: Node, data_frame: DataFrame) -> None:
        # print("NODE", parent_title)
        # print(data_frame)
        entropies = self._get_entropies(data_frame)
        the_best_index = self._get_max_entropy(entropies)[0]
        children = data_frame.devide_data_frame(the_best_index)
        label = data_frame.get_label(the_best_index)

        the_node = Node(parent_title, label, value, parent, None)
        parent.add_child(the_node)

        for child in children:
            title = child.get_title()
            if i(0, child) == 0 or len(child.get_labels()) == 1:  # liść
                self._build_leaves(title, the_node, child)
            else:
                self._build_node(title, the_best_index, the_node, child)

    def build_tree(self) -> None:
        entropies = self._get_entropies(self._df)
        the_best_index = self._get_max_entropy(entropies)[0]
        children = self._df.devide_data_frame(the_best_index)
        label = self._df.get_label(the_best_index)

        self._main_node = Node("NULL", label, self._df.rows(), None, None)

        for child in children:
            title = child.get_title()
            if i(0, child) == 0:  # liść
                self._build_leaves(title, self._main_node, child)
            else:
                self._build_node(title, the_best_index, self._main_node, child)

    def print_tree(self) -> None:
        to_print = [(self._main_node, 0)]
        while to_print != []:
            node, deep = to_print.pop(0)
            for child in node.get_children():
                if child.leaf():
                    to_print.insert(0, (child, deep+1))
                else:
                    to_print.insert(-1, (child, deep+1))
            print("\t"*deep, node)

    def check(self, row: list) -> str:
        node = self._main_node
        value = None
        while True:
            node_value = node.get_value()
            index_of_label = self._df.get_labels().index(node_value)
            last_value = value
            value = row[index_of_label]
            if last_value == value:
                return "INNE"
            # print(value)
            for child in node.get_children():
                # print(child)
                if child.get_label() == value:
                    # print("v:", child.get_value())
                    if child.leaf():
                        # print("leaf")
                        return child.get_value()
                    else:
                        # print("node")
                        node = child
                        break # ? break, continue
            # print("True")
            # return print("!")
        


if __name__ == "__main__":
    data = [["A", 1, 0],
            ["B", 1, 1],
            ["B", 2, 1],
            ["B", 2, 0],
            ["B", 3, 1]]
    
    #        x1,  x2, x3, y
    data = [["A", "w", "t", 0],
            ["A", "w", "n", 1],
            ["B", "u", "t", 0],
            ["B", "i", "t", 1],
            ["A", "u", "n", 0],
            ["B", "w", "n", 1]]

    df = DataFrame(data, ["x1", "x2", "x3", "y"])
    df = get_data_frame()
    # print(df)
    tree = DecisionTree(df)
    print("Powinno być:", tree.get_data_frame()._rows[69][-1])
    tree.build_tree()
    # print(tree.get_data_frame()._rows[63])
    # input()
    # tree.print_tree()

    # print(tree.get_data_frame()._rows)
    # print(tree.check(["A", "i", "t"]))
    print("Jest:", tree.check(['usual', 'proper', 'complete', '2', 'convenient', 'inconv', 'problematic', 'recommended']))
