import os
from dataset import MeasureDataLoader
from .TrainTask import TrainTask


class MeasureTask(TrainTask):
    """
    训练样本是度量数据（向量）
    """

    def __init__(self, feature_root: str, feature_dir: str, label_file: str):
        """
        :param feature_root 特征数据根目录
        :param feature_dir 特征目录名
        :param label_file 标签文件
        """
        self.data_dir = os.path.join(feature_root, feature_dir)
        self.label_file = label_file
        super().__init__(feature_dir, "")

    def init_task(self):
        self.data_set = MeasureDataLoader(self.data_dir)
        self.data_set.load_label(self.label_file)
        self.data_set.read_data()
        self.train_functions = {False: [MeasureTask.train], True: []}
        super().init_task()
