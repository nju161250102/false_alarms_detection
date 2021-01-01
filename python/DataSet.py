import os
import random
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler


class DataLoader:

    over_sample = False
    under_sample = False

    """
    数据加载器，用于加载、划分训练数据集与测试数据集
    """
    def __init__(self, data_dir: str):
        # 自定义设置
        self.compress_flag = False
        # 文件列表，格式：[(文件路径, 文件ID)...]
        self.file_list = []
        # 标签Map，格式：{文件ID, 0/1标签}
        self.label_dict = {}
        # 数据列表，格式：[单个数据]
        self.data_list = []
        # 获取文件夹下文件路径与ID的对应关系
        for f in os.listdir(data_dir):
            self.file_list.append((os.path.join(data_dir, f), os.path.splitext(f)[0][:-7]))

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
        if DataLoader.over_sample:
            ros = RandomOverSampler(random_state=0)
            X_resampled, y_resampled = ros.fit_sample(X_train, y_train)
            print(len(X_resampled), len(X_train))
            return X_resampled, y_resampled, X_test, y_test
        if DataLoader.under_sample:
            rus = RandomUnderSampler(random_state=0)
            X_resampled, y_resampled = rus.fit_sample(X_train, y_train)
            return X_resampled, y_resampled, X_test, y_test
        return X_train, y_train, X_test, y_test

    def load_label(self, label_csv: str):
        """
        :param label_csv: 处理好的标记csv，每行格式[数据ID，标记]
        :return: 数据ID到标记的映射
        """
        df = pd.read_csv(label_csv, header=None)
        for row in df.itertuples():
            self.label_dict[row[1]] = row[2]

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
        for file_path, file_id in self.file_list:
            if file_id not in self.label_dict.keys():
                continue
            df = pd.read_csv(file_path, header=None)
            feature_len = df.shape[0]
            x_data = []
            for index, row in df.iterrows():
                if index < len_limit:
                    x_data.append(list(row))
            if feature_len < len_limit:
                for i in range(feature_len, len_limit):
                    x_data.append([0 for j in range(df.shape[1])])
            self.data_list.append((x_data, self.label_dict[file_id]))


class WordDataLoader(DataLoader):

    def __init__(self, data_dir: str):
        super().__init__(data_dir)

    def read_data(self, handler: str):
        text_data = []
        id_list = []
        vectorizer = CountVectorizer() if handler == "Count" else TfidfVectorizer()
        for file_path, file_id in self.file_list:
            if file_id not in self.label_dict.keys():
                continue
            df = pd.read_csv(file_path, header=None)
            text_data.append(" ".join([str(s) for s in df.values.tolist()[0]]))
            id_list.append(file_id)
        vector_array = vectorizer.fit_transform(text_data).toarray()
        for i in range(len(vector_array)):
            self.data_list.append((vector_array[i], self.label_dict[id_list[i]]))


class ManualDataLoader(DataLoader):

    def __init__(self, data_dir: str):
        super().__init__(data_dir)

    def read_data(self):
        for file_path, file_id in self.file_list:
            if file_id not in self.label_dict.keys():
                continue
            with open(file_path) as txt_file:
                self.data_list.append(([int(s) for s in txt_file.readline().split()[:5]], self.label_dict[file_id]))


class DocDataLoader(DataLoader):

    def __init__(self, data_dir: str):
        super().__init__(data_dir)

    def read_data(self):
        for file_path, file_id in self.file_list:
            if file_id not in self.label_dict.keys():
                continue
            df = pd.read_csv(file_path, header=None)
            self.data_list.append((df.values.tolist()[0], self.label_dict[file_id]))
