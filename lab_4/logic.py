from math import log


def get_data_frame(file_name: str = "./nursery.data") -> list:
    """
    Open the file with the data and return it as a list.
    
    Input:
     * file_name: str - file name / location and name
    
    Output:
     * rows: list[list[str]]
    """
    data_frame = []
    with open(file_name, "r", -1, "utf-8") as file:
        for row in file:
            row = row.strip().split(",")
            if row != [""]:
                data_frame.append(row)
    return data_frame


def get_column(column_index: int, data_frame: list) -> list:
    """
    Extract a column with the given index from the data frame.
    
    Input:
     * column_index: int
     * data_frame: list[list[DATA]]
    
    Output:
     * data_frame: list[DATA]
    """
    return [row[column_index] for row in data_frame]


def del_column(column_index: int, data_frame: list) -> list:
    """
    Delete a column with the given index from the data frame.
    
    Input:
     * column_index: int
     * data_frame: list[list[DATA]]
    
    Output:
     * data_frame: list[DATA] - without the column
    """
    new_frame = []
    for row in data_frame:
        new_row = [element for index, element in enumerate(row) 
                   if index != column_index]
        new_frame.append(new_row)
    return new_frame


def devide_data_frame(column_index: int, data_frame: list) -> list:
    """
    Devide the data frame by a column with the given index.
    
    Input:
     * column_index: int
     * data_frame: list[list[DATA]]
    
    Output:
     * data_frames: list[ list[list[DATA]] ] - devided data frame
    """
    values = get_unique_values(column_index, data_frame)
    frames = [ [] for _ in range(len(values))]
    for row in data_frame:
        for index, value in enumerate(values):
            if row[column_index] == value:
                frames[index].append(row)

    for index, frame in enumerate(frames):
        frames[index] = del_column(column_index, frame)

    return frames
    


def get_unique_values(column_index: int, data_frame: list) -> set:
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
        


def i(column_index: int, data_frame: list) -> float:
    """
    Entropy of a column.
    
    Input:
     * column_index: int
     * data_frame: list[list[DATA]]
     
    Output:
     * entropy: float
    """
    column = get_column(column_index, data_frame)
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


def inf(column1_index: int, column2_index: int, data_frame: list) -> float:
    """
    Entropy of a data frame devided by column with index column1_index.
    Column with column2_index is a column with values.
    
    Input:
     * column1_index: int - A column that divides a data frame
     * column2_index: int - A column with values
     * data_frame: list[list[DATA]]
     
    Output:
     * Entropy: float
    """
    column1 = get_column(column1_index, data_frame)
    column2 = get_column(column2_index, data_frame)

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
             data_frame: list) -> float:
    """
    Information acquirement of data frame 
    devided by column with index column1_index.
    Column with column2_index is a column with values.
    
    Input:
     * column1_index: int - A column that divides a data frame
     * column2_index: int - A column with values
     * data_frame: list[list[DATA]]
     
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
    print("I:", i(-1, data))
    print("Inf:", inf(0, -1, data))
    print("InfGain:", inf_gain(0, -1, data))
    
    print()
    for row in data:
        print(row)
    print()
    for frame in devide_data_frame(0, data):
        for row in frame:
            print(row)
        print()
