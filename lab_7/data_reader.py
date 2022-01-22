def open_file(file_name: str = "wine.data") -> list:
    """
    Open file into list of lists.

    Input:
     * file_name: str - file path

    Output:
     * list[list[str]] - data
    """
    data = []

    with open(file_name, "r", -1, "utf-8") as file:
        for row in file:
            data.append(row.strip().split(","))

    return data
