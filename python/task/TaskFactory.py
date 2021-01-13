import os
import logging
import pandas as pd
from .MeasureTask import MeasureTask
from .WordTask import WordTask
from .VectorTask import VectorTask
from .OneHotTask import OneHotTask


class TaskFactory:

    def __init__(self, feature_root: str, label_file: str):
        self.task_list = []
        self.feature_root = feature_root
        self.label_file = label_file

    def add_tasks(self, feature_list: list):
        """
        向任务列表中增加一系列特征的训练任务
        :param feature_list 特征目录列表
        """
        for feature_dir in feature_list:
            # 检查目录是否存在，不存在返回[]
            if not os.path.isdir(os.path.join(self.feature_root, feature_dir)):
                continue
            # 特征类型：Word2Vec向量
            if "v" in feature_dir:
                self.task_list.append(VectorTask(self.feature_root, feature_dir, self.label_file))
            # 特征类型：度量特征
            elif "manual" in feature_dir:
                self.task_list.append(MeasureTask(self.feature_root, feature_dir, self.label_file))
            # 特征类型：单词特征
            else:
                for v in ["Count", "Tf"]:
                    self.task_list.append(WordTask(self.feature_root, feature_dir, self.label_file, v))
                self.task_list.append(OneHotTask(self.feature_root, feature_dir, self.label_file))

    def auto_add_tasks(self):
        """
        根据feature_root自动读取并训练所有特征
        """
        self.add_tasks(os.listdir(self.feature_root))

    def run_and_save(self, output_path: str, run_time: int, train_rate=0.7):
        """
        依次运行训练任务并保存结果
        """
        result = []
        # 合并训练结果
        for t in self.task_list:
            t.run(run_time, train_rate)
            result.extend(t.get_result_lines())
            logging.info("Task: %s_%s, Line_sum: %d" % (t.feature_name, t.vector_method, len(result)))
            df = pd.DataFrame(data=result,
                              columns=["feature", "to_vector", "model_name", "acc", "pre", "rec", "f1", "auc"])
            df.to_csv(output_path, header=True, index_label=False)
