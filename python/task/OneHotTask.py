import os
from dataset import WordDataLoader
from .TrainTask import TrainTask


class OneHotTask(TrainTask):
    """
    OneHot对文本编码的训练任务
    """

    def __init__(self, feature_root: str, feature_dir: str, label_file: str):
        self.data_dir = os.path.join(feature_root, feature_dir)
        self.label_file = label_file
        super().__init__(feature_dir, "OneHot")

    def init_task(self):
        self.data_set = WordDataLoader(self.data_dir)
        self.data_set.load_label(self.label_file)
        self.data_set.read_data("OneHot")
        self.train_functions = {True: [OneHotTask.train], False: []}
        super().init_task()
