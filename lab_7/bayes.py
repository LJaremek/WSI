from math import log

import pandas as pd

from bayes_math import mean, standard_deviation
from bayes_math import gaussian_probability


class BayesDataClass:
    """
    Class represents one class of the data.

    Init input:
     * class_name: str
     * class_col_index: int - index of the labels (class name)
     * class_data: pd.DataFrame
     * all_rows: int - number of rows in full data frame
    """
    def __init__(self,
                 class_name: str,
                 class_col_index: int,
                 class_data: pd.DataFrame,
                 all_rows: int) -> None:
        self._name = class_name
        self._data = class_data
        self._all_rows = all_rows
        self._class_index = class_col_index
        self._calc_probabilities()

    def _calc_probabilities(self) -> None:
        """
        Calculate porbabilities for every column.
        Function create self._class_prob and self._columns_prob.
        """
        self._class_prob = len(self._data.columns)/self._all_rows
        self._columns_prob = []
        for column in self._data:
            if column == self._class_index:  # label index
                self._columns_prob.append(None)
                continue
            self._columns_prob.append((mean(self._data[column]),
                                       standard_deviation(self._data[column])
                                       ))

    def get_column_mean(self, column_index: int) -> float:
        """
        Mean of the column with the given index.

        Input:
         * column_index: int

        Output:
         * float - mean
        """
        return self._columns_prob[column_index][0]

    def get_column_stdv(self, column_index: int) -> float:
        """
        Standard deviation of the column with the given index.

        Input:
         * column_index: int

        Output:
         * float - standard deviation
        """
        return self._columns_prob[column_index][1]

    def get_row_value(self, row: list[float]) -> float:
        """
        Value of the given row.
        It is sum of ln of gaussian_probability of the columns.

        Input:
         * row: list[float]

        Output:
         * float - value
        """
        values = []
        for index, cell in enumerate(row):
            index += 1
            if index == 0:  # prob of the class
                values.append(log(self._class_prob))
                continue
            # prob of the value from the row
            _mean = self.get_column_mean(index)
            _stdv = self.get_column_stdv(index)
            gauss = gaussian_probability(cell, _mean, _stdv)
            if gauss == 0.0:
                value = -(10**10)
            else:
                value = log(gauss)
            values.append(value)
        return sum(values)


class NaiveBayes:
    """
    Gaussian Naive Bayes Model.

    Init input:
     * data: pd.DataFrame - train data
     * label_index: int - index of column with class labels

    Predict function:
     * check_row(row)
    """
    def __init__(self,
                 data: pd.DataFrame,
                 class_col_index: int = 0) -> None:
        self._data = data
        self._label_index = class_col_index
        self._classes = self._devide_by_class()

    def _devide_by_class(self) -> dict[str, pd.DataFrame]:
        """
        Devide pandas data frame by class.

        Output:
         * dict[str, BayesDataClass] - dict where key i the class label
            and value is a BayesDataClass
        """
        return dict([
                     (the_class,
                      BayesDataClass(the_class,
                                     self._label_index,
                                     (self._data[self._data[self._label_index]
                                                 == the_class]),
                                     len(self._data))
                      )
                     for the_class in set(self._data[self._label_index])
                     ])

    def check_row(self, row: pd.DataFrame) -> str:
        """
        Check the class label of the given row.

        Input:
         * row: pd.DataFrame

        Output:
         * int - estimated class name
        """
        classes = list(self._classes.keys())
        values = []
        for the_class in classes:
            data_class = self._classes[the_class]
            class_value = data_class.get_row_value(row)
            values.append(class_value)
        index = values.index(max(values))
        return classes[index]
