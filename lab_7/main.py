import pandas as pd

from data_reader import open_file
from bayes import NaiveBayes

if __name__ == "__main__":
    data = pd.DataFrame(open_file())
    label_index = 0
    for column in data:
        if column == label_index:
            continue
        data[column] = pd.to_numeric(data[column])

    shuffle_data = data.sample(frac=1).reset_index(drop=True)

    rows = len(shuffle_data)
    train = 0.8
    train_data = shuffle_data.iloc[int(rows*(1-train)):]

    test_data = shuffle_data.iloc[:int(rows*(1-train))]

    bayes = NaiveBayes(train_data, label_index)

    ok = 0
    not_ok = 0
    for index, row in test_data.iterrows():
        drop_row = row.drop(label_index, 0)
        if row[0] != bayes.check_row(drop_row):
            print(row[0], bayes.check_row(drop_row))
            not_ok += 1
        else:
            ok += 1

    print("not ok", not_ok)
    print("ok", ok)
