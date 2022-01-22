import pandas as pd

from bayes_math import gaussian_probability
from data_reader import open_file

data = pd.DataFrame(open_file())
for column in data:
    data[column] = pd.to_numeric(data[column])


class NaiveBayes:
    def __init__(self, data: pd.DataFrame, column_index: int = 0) -> None:
        self._data = data
        self._classes = self._devide_by_class(data, column_index)

    def _devide_by_class(self,
                         data: pd.DataFrame,
                         column_index: int) -> dict[str, pd.DataFrame]:
        """
        Devide pandas data frame by class.

        Input:
         * data: pd.DataFrame
         * column_index: int - index of column with classes

        Output:
         * dict[str, pd.DataFrame] - dict where key i the class
            and value is a data frame with the class
        """
        return dict([
                     (the_class, data[data[column_index] == the_class])
                     for the_class in set(data[column_index])
                     ])


if __name__ == "__main__":
    bayes = NaiveBayes(data, 0)
    print(bayes._classes.keys())
