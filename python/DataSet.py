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
            return self.transform_x(list(train_data[0])), list(train_data[1]), self.transform_x(list(test_data[0])), list(test_data[1])
        return list(train_data[0]), list(train_data[1]), list(test_data[0]), list(test_data[1])

    def load_label(self, label_csv: str):
        """
        :param label_csv: 处理好的标记csv，每行格式[数据ID，标记]
        """
        df = pd.read_csv(label_csv, header=None)
        d = {}
        for row in df.itertuples():
            d[row[1]] = row[2]
        for f in os.listdir(self.data_dir):
            file_id = os.path.splitext(f)[0][:-7]
            if file_id not in d.keys():
                continue
            self.file_list.append((os.path.join(self.data_dir, f), d[file_id]))
        X, y = zip(* self.file_list)
        if DataLoader.over_sample:
            ros = RandomOverSampler(random_state=0)
            X_resampled, y_resampled = ros.fit_sample(list(X), list(y))
            self.file_list = list(zip(X_resampled, y_resampled))
        if DataLoader.under_sample:
            rus = RandomUnderSampler(random_state=0)
            X_resampled, y_resampled = rus.fit_sample(list(X), list(y))
            self.file_list = list(zip(X_resampled, y_resampled))

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
        vectorizer = CountVectorizer() if handler == "Count" else TfidfVectorizer()
        for file_path, file_label in self.file_list:
            df = pd.read_csv(file_path, header=None)
            text_data.append(" ".join([str(s) for s in df.values.tolist()[0]]))
            id_list.append(file_label)
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
