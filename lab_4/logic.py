from __future__ import annotations

from random import randint
from math import log

class DataFrame:
    def __init__(self,
                 rows: list = None,
                 labels: list = None, 
                 title: str = None) -> None:
        if rows is None:
            self._rows = []
        else:
            self._rows = rows
        if labels is None and rows is None:
            self._labels = []
        elif labels is None:
            self._labels = [ str(i) for i in range(len(self._rows[0])) ]
        else:
            self._labels = labels
        self._title = title
    
    def __getitem__(self, index: int) -> list:
        return self._rows[index]
    
    def __next__(self):
        for row in self._rows:
            return row

    def __str__(self) -> str:
        string = f"----== {self._title} ==----\n"
        for l in self._labels:
            string += str(l)
            string += "\t"
        string += "\n"
        string += "\n"
        for row in self._rows:
            for v in row:
                string += str(v)
                string += "\t"
            string += "\n"
        string += f"----== {self._title} ==----\n"
        return string
    
    def __repr__(self) -> str:
        return self.__str__()

    def get_row(self, index: int) -> list:
        return self._rows[index]

    def get_column(self, index: int) -> list:
        return [row[index] for row in self._rows]
    
    def columns(self) -> int:
        return len(self._rows[0])
    
    def rows(self) -> int:
        return len(self._rows)
    
    def get_title(self) -> str:
        return self._title
    
    def set_title(self, new_title: str) -> None:
        self._title = new_title
        
    def get_labels(self) -> list:
        return [label for label in self._labels]

    def get_label(self, index: int) -> str:
        return self._labels[index]

    def add_row(self, row: list, index: int = -1) -> None:
        self._rows.insert(index, row)

    def add_column(self, column: list, index: int = -1) -> None:
        for c_i, row in enumerate(self._rows):
            self._rows.insert(index, column[c_i])
            
    def del_column(self, column_index: int) -> None:
        for row in self._rows:
            del row[column_index]
        del self._labels[column_index]
            
    def devide_data_frame(self, column_index: int) -> DataFrame:
        values = get_unique_values(column_index, self)
        frames = {}
        for value in values:
            frames[value] = DataFrame(labels=self.get_labels(), title=value)

        for row in self._rows:
            for index, value in enumerate(values):
                if row[column_index] == value:
                    frames[value].add_row(row)

        for frame in frames:
            frames[frame].del_column(column_index)

        return list(frames.values())


def open_file(file_name: str = "./nursery.data") -> list:
    """
    Open the file with the data and return it as a list.
    
    Input:
     * file_name: str - file name / location and name
    
    Output:
     * rows: DataFrame
    """
    rows = []
    with open(file_name, "r", -1, "utf-8") as file:
        for row in file:
            row = row.strip().split(",")
            if row != [""]:
                rows.append(row)
    return rows


def split_data(rows: list, parts: int = 3) -> list:
    part_list = [ [] for _ in range(parts) ]
    p_index = 0
    while rows != []:
        index = randint(0, len(rows)-1)
        part_list[p_index].append(rows.pop(index))
        p_index += 1
        p_index = p_index%parts
    return part_list


def get_unique_values(column_index: int, data_frame: DataFrame) -> set:
    """
    Return unique values from the column with the given index.
    
    Input:
     * column_index: int
     * data_frame: list[list[DATA]]
    
    Output:
     * unique_values: set
    """
    values = [row[column_index] for row in data_frame]
    return set(values)


def i(column_index: int, data_frame: DataFrame) -> float:
    """
    Entropy of a column.
    
    Input:
     * column_index: int
     * data_frame: list[list[DATA]]
     
    Output:
     * entropy: float
    """
    column = data_frame.get_column(column_index)
    sum = 0
    length = len(column)
    elements = {}

    for element in column:
        if element in elements:
            elements[element] += 1
        else:
            elements[element] = 1

    for element in elements:
        prob = elements[element]/length
        # print(f"+{prob}*log({prob})")# = ({value*log(value)})")
        sum += prob*log(prob)

    return -sum


def inf(column1_index: int, column2_index: int, data_frame: DataFrame) -> float:
    """
    Entropy of a data frame devided by column with index column1_index.
    Column with column2_index is a column with values.
    
    Input:
     * column1_index: int - A column that divides a data frame
     * column2_index: int - A column with values
     * data_frame: DataFrame
     
    Output:
     * Entropy: float
    """
    column1 = data_frame.get_column(column1_index)
    column2 = data_frame.get_column(column2_index)

    elements1 = {}
    all_elements1 = 0
    for element in column1:
        if element in elements1:
            elements1[element] += 1
        else:
            elements1[element] = 1
        all_elements1 += 1

    elements2 = {}
    for index, element in enumerate(column1):
        all_elem = 0
        if element in elements2:
            element2 = column2[index]
            if element2 in elements2[element]:
                elements2[element][element2] += 1
            else:
                elements2[element][element2] = 1
        else:
            elements2[element] = {}
            element2 = column2[index]
            if element2 in elements2[element]:
                elements2[element][element2] += 1
            else:
                elements2[element][element2] = 1

    sum = 0
    for element in elements1:
        prob = elements1[element]/all_elements1
        # print(f"{elements1[element]}/{all_elements1}*[-(", end="")
        temp_sum = 0
        for element2 in elements2[element]:
            values = list(elements2[element].values())
            values_count  = 0
            for b in values:
                values_count += b
            prob_temp = elements2[element][element2]/values_count
            # print(f"{elements2[element][element2]}/{values_count}*log({elements2[element][element2]}/{values_count})", end="+")
            temp_sum += prob_temp*log(prob_temp)
        # print(")]")
        sum += -temp_sum*prob

    return sum


def inf_gain(column_index1: int, 
             column_index2: int, 
             data_frame: DataFrame) -> float:
    """
    Information acquirement of data frame 
    devided by column with index column1_index.
    Column with column2_index is a column with values.
    
    Input:
     * column1_index: int - A column that divides a data frame
     * column2_index: int - A column with values
     * data_frame: DataFrame
     
    Output:
     * Information acquirement: float
    """
    i_value = i(column_index2, data_frame)
    inf_value = inf(column_index1, column_index2, data_frame)
    return i_value - inf_value


if __name__ == "__main__":
    data = [["A", 1, 0],
            ["B", 1, 1],
            ["B", 2, 1],
            ["B", 2, 0],
            ["B", 3, 1]]
    df = DataFrame(data, ["x1", "x2", "y"])
    print(df)
    print("I:", i(-1, df))
    print("Inf:", inf(0, -1, df))
    print("InfGain:", inf_gain(0, -1, df))

    # the_list = DataFrame(open_file())
    # the_list = the_list.get_column(-1)
    # counter = {}
    # for el in the_list:
    #     if el in counter:
    #         counter[el] += 1
    #     else:
    #         counter[el] = 1
    # print(counter)
