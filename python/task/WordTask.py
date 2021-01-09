import os
from dataset import WordDataLoader
from .TrainTask import TrainTask


class WordTask(TrainTask):
    """
    使用单词进行词频分析的训练任务
    """

    def __init__(self, feature_root: str, feature_dir: str, label_file: str, counter: str):
        self.data_dir = os.path.join(feature_root, feature_dir)
        self.label_file = label_file
        self.counter = counter
        super().__init__(feature_dir, counter)

    def init_task(self):
        self.data_set = WordDataLoader(self.data_dir)
        self.data_set.load_label(self.label_file)
        self.data_set.read_data(self.counter)
        self.train_functions = {False: [WordTask.train], True: []}
        super().init_task()
