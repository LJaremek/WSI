from __future__ import annotations
from collections import Counter

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

    def _the_most_popular(self, the_list: list):
        counter = {}
        for el in the_list:
            if el in counter:
                counter[el] += 1
            else:
                counter[el] = 1
        max_ = -1
        max_el = None
        for el in counter:
            if counter[el] > max_:
                max_ = counter[el]
                max_el = el
        return max_el

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
                    parent: Node, 
                    data_frame: DataFrame) -> None:
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
                if node.leaf():
                    return self._the_most_popular(node.get_children())
                else:
                    # print(node.get_children())
                    # print("!2", self._the_most_popular(node.get_children()))
                    return self._the_most_popular(node.get_children())

            for child in node.get_children():
                if child.get_label() == value:
                    if child.leaf():
                        return child.get_value()
                    else:
                        node = child
                        break


if __name__ == "__main__":
    rows = open_file()
    print("Rows:", len(rows))
    
    parts = 5
    train_parts = split_data(rows, parts)
    print("Parts:", parts, "with:", len(train_parts[0]), "elemetns")
    test_part = train_parts.pop()
    trees = []

    for part in train_parts:
        tree = DecisionTree(DataFrame(part))
        tree.build_tree()
        trees.append(tree)

    results = {"ok": 0,
               "ni": 0}
    for row in test_part:
        result = row.pop()
        res = []
        for tree in trees:
            res.append(tree.check(row))
        c = Counter(res)
        res = c.most_common(1)[0][0]
        if result == res:
            results["ok"] += 1
        else:
            results["ni"] += 1
    
    print(results)
