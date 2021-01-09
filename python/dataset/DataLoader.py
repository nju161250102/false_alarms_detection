import os
import random
import pandas as pd


class DataLoader:
    """
    数据加载器，用于加载、划分训练数据集与测试数据集
    """

    # 过采样设置
    over_sample = False
    # 欠采样设置
    under_sample = False
    # 漏洞分类筛选列表（设置为None表示不筛选）
    category_list = None

    def __init__(self, data_dir: str):
        # 自定义设置
        self.compress_flag = False
        # 文件列表，格式：[(文件路径, 文件ID)...]
        self.file_list = []
        # 数据列表，格式：[单个数据]
        self.data_list = []
        self.data_dir = data_dir

    def split_data(self, rate: float) -> tuple:
        """
        将数据集划分为训练数据集和测试数据集
        :param rate: 设定训练数据集的比例
        :return:
        """
        random.shuffle(self.data_list)
        train_data = list(zip(*self.data_list[:int(len(self.data_list) * rate)]))
        test_data = list(zip(*self.data_list[int(len(self.data_list) * rate):]))
        if self.compress_flag:
            X_train, y_train, X_test, y_test = self.transform_x(list(train_data[0])), list(train_data[1]), self.transform_x(list(test_data[0])), list(test_data[1])
        else:
            X_train, y_train, X_test, y_test = list(train_data[0]), list(train_data[1]), list(test_data[0]), list(test_data[1])
        if (not DataLoader.over_sample) and (not DataLoader.under_sample):
            return X_train, y_train, X_test, y_test
        true_y = sum(y_train)
        false_y = len(y_train) - true_y
        less_y = 0 if true_y > false_y else 1
        more_y = 1 if true_y > false_y else 0
        less_X = [x[0] for x in filter(lambda m: m[1] == less_y, zip(X_train, y_train))]
        more_X = [x[0] for x in filter(lambda m: m[1] == more_y, zip(X_train, y_train))]
        if DataLoader.over_sample:
            X_train += random.choices(less_X, k=(len(more_X) - len(less_X)))
            y_train += [less_y] * (len(more_X) - len(less_X))
        if DataLoader.under_sample:
            X_train = less_X + more_X[:len(less_X)]
            y_train = [less_y] * len(less_X) + [more_y] * len(less_X)
        modified_data = list(zip(X_train, y_train))
        random.shuffle(modified_data)
        X_train, y_train = zip(*modified_data)
        return X_train, y_train, X_test, y_test

    def load_label(self, label_csv: str):
        """
        :param label_csv: 处理好的标记csv，每行格式[数据ID，标记]
        """
        df = pd.read_csv(label_csv, header=None)
        d = {}
        for row in df.itertuples():
            if DataLoader.category_list is None \
                    or (DataLoader.category_list is not None and row[3] in DataLoader.category_list):
                d[row[1]] = row[2]
        for f in os.listdir(self.data_dir):
            file_id = os.path.splitext(f)[0][:-7]
            if file_id not in d.keys():
                continue
            self.file_list.append((os.path.join(self.data_dir, f), d[file_id]))

    @staticmethod
    def transform_x(x_data):
        result = []
        for x in x_data:
            result.append([sum(batch) / len(batch) for batch in x])
        return result
