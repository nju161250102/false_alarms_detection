import os
import random
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class DataLoader:

    # 过采样设置
    over_sample = False
    # 欠采样设置
    under_sample = False
    # 用于训练的漏洞分类列表
    category_list = None

    """
    数据加载器，用于加载、划分训练数据集与测试数据集
    """
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


class VectorDataLoader(DataLoader):

    def __init__(self, data_dir: str):
        super().__init__(data_dir)

    def read_data(self, len_limit: int):
        for file_path, file_label in self.file_list:
            df = pd.read_csv(file_path, header=None)
            feature_len = df.shape[0]
            x_data = []
            for index, row in df.iterrows():
                if index < len_limit:
                    x_data.append(list(row))
            if feature_len < len_limit:
                for i in range(feature_len, len_limit):
                    x_data.append([0 for j in range(df.shape[1])])
            self.data_list.append((x_data, file_label))


class WordDataLoader(DataLoader):

    def __init__(self, data_dir: str):
        super().__init__(data_dir)

    def read_data(self, handler: str):
        text_data = []
        id_list = []
        for file_path, file_label in self.file_list:
            df = pd.read_csv(file_path, header=None)
            text_data.append(" ".join([str(s) for s in df.values.tolist()[0]]))
            id_list.append(file_label)
        # One-Hot 编码
        if handler == "OneHot":
            encoder = OneHotEncoder()
            all_text = " ".join(text_data).split(" ")
            encoder.fit(np.array(all_text).reshape(len(all_text), -1))
            for i in range(len(text_data)):
                text_list = text_data[i].split(" ")
                self.data_list.append((encoder.transform(np.array(text_list).reshape(len(text_list) - 1)), id_list[i]))
            return
        # 词频编码或TD-IDF编码
        else:
            vectorizer = CountVectorizer() if handler == "Count" else TfidfVectorizer()
            vector_array = vectorizer.fit_transform(text_data).toarray()
            for i in range(len(vector_array)):
                self.data_list.append((vector_array[i], id_list[i]))


class ManualDataLoader(DataLoader):

    def __init__(self, data_dir: str):
        super().__init__(data_dir)

    def read_data(self):
        for file_path, file_label in self.file_list:
            with open(file_path) as txt_file:
                self.data_list.append(([int(s) for s in txt_file.readline().split()[:5]], file_label))


class DocDataLoader(DataLoader):

    def __init__(self, data_dir: str):
        super().__init__(data_dir)

    def read_data(self):
        for file_path, file_label in self.file_list:
            df = pd.read_csv(file_path, header=None)
            self.data_list.append((df.values.tolist()[0], file_label))
