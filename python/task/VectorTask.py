import os
import re
from dataset import VectorDataLoader
from model import ModelFactory
from .TrainTask import TrainTask


class VectorTask(TrainTask):
    """
    训练样本由向量序列组成（也就是矩阵），特征命名方式为[特征名_v_向量大小]
    """

    def __init__(self, feature_root: str, feature_dir: str, label_file: str, seq_len=80):
        """
        :param feature_root 特征数据根目录
        :param feature_dir 特征目录名 [特征名_v_向量大小]
        :param label_file 标签文件
        :param seq_len 截取/补齐的序列长度
        """
        feature_name, vector_size = re.findall(r"(.*?)_v_(.*)", feature_dir)[0]
        self.data_dir = os.path.join(feature_root, feature_dir)
        self.label_file = label_file
        self.feature_size = int(vector_size)
        self.seq_len = seq_len
        super().__init__(feature_name, "wv_" + vector_size)

    def init_task(self):
        self.data_set = VectorDataLoader(self.data_dir)
        self.data_set.load_label(self.label_file)
        self.data_set.read_data(self.seq_len)
        self.train_functions = {True: [VectorTask.train], False: [VectorTask.train_cnn, VectorTask.train_lstm]}
        super().init_task()

    def train_cnn(self, x_train, y_train, x_test, y_test):
        train_model = ModelFactory()
        train_model.build_cnn((self.seq_len, self.feature_size))
        train_model.train(x_train, y_train)
        return {"cnn": train_model.evaluate(x_test, y_test)}

    def train_lstm(self, x_train, y_train, x_test, y_test):
        train_model = ModelFactory()
        train_model.build_lstm((self.seq_len, self.feature_size))
        train_model.train(x_train, y_train)
        return {"lstm": train_model.evaluate(x_test, y_test)}
