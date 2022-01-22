import pandas as pd

from data_reader import open_file
from bayes import NaiveBayes

if __name__ == "__main__":
    # Read data
    data = pd.DataFrame(open_file())
    label_index = 0  # index of column with labels

    # changing strings to floats
    for column in data:
        if column == label_index:
            continue
        data[column] = pd.to_numeric(data[column])

    # shuffle data
    shuffle_data = data.sample(frac=1).reset_index(drop=True)

    # split data
    rows = len(shuffle_data)
    train = 0.8
    train_data = shuffle_data.iloc[int(rows*(1-train)):]

    test_data = shuffle_data.iloc[:int(rows*(1-train))]

    # train model
    bayes = NaiveBayes(train_data, label_index)

    # predict model
    class_list = list("123")

    results = [[0 for _ in class_list] for _ in class_list]
    for index, row in test_data.iterrows():
        desired_result = row[label_index]
        row = row.drop(label_index, 0)
        obtained_result = bayes.check_row(row)

        index_0 = class_list.index(desired_result)
        index_1 = class_list.index(obtained_result)
        results[index_0][index_1] += 1

    # calculate metrics
    metrics = {}
    for y in class_list:
        metrics[y] = {"tp": 0,
                      "tn": 0,
                      "fn": 0,
                      "fp": 0}

    # print results
    print("\n\t", "\t".join(class_list))
    for index, value in enumerate(class_list):
        print(value, "\t", "\t".join(list(map(str, results[index]))))

    # calculate
    for index, y in enumerate(class_list):
        metrics[y]["tp"] = results[index][index]
        metrics[y]["tn"] = sum([row[i]
                                for i, row in enumerate(results)
                                if i != index])
        metrics[y]["fp"] = sum([row[index]
                                for i, row in enumerate(results)
                                if i != index])
        metrics[y]["fn"] = sum(results[index][:index] +
                               results[index][index+1:])

    # print Matrix
    print("\nMatrix:")
    for key in metrics:
        print(key, metrics[key])

    # Get and print additional parameters
    tpr = sum([metrics[key]["tp"]]) / (sum([metrics[key]["tp"]]) +
                                       sum([metrics[key]["fn"]]))
    fpr = sum([metrics[key]["fp"]]) / (sum([metrics[key]["fp"]]) +
                                       sum([metrics[key]["tn"]]))
    ppv = sum([metrics[key]["tp"]]) / (sum([metrics[key]["tp"]]) +
                                       sum([metrics[key]["fp"]]))
    acc = ((sum([metrics[key]["tp"]]) + sum([metrics[key]["tn"]])) /
           (sum([metrics[key]["tp"]]) + sum([metrics[key]["fn"]]) +
            sum([metrics[key]["tn"]]) + sum([metrics[key]["fn"]])))
    print("\nTPR:", tpr)
    print("FPR:", fpr)
    print("PPV:", ppv)
    print("Acc:", acc)
