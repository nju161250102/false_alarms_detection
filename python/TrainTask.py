import os
import numpy as np
import pandas as pd
from DataSet import *
from TrainModel import ModelFactory


class TrainTask:

    def __init__(self):
        self.data_set = None
        self.result_data = {}
        self.train_functions = {}

    def init_task(self):
        pass

    def run(self, num: int, rate: float):
        self.init_task()
        for i in range(num):
            for flag in [False, True]:
                if len(self.train_functions[flag]) == 0:
                    continue
                self.data_set.compress_flag = flag
                x_train, y_train, x_test, y_test = self.data_set.split_data(rate)
                for func in self.train_functions[flag]:
                    for k, l in func(x_train, y_train, x_test, y_test).items():
                        if k in self.result_data.keys():
                            self.result_data[k].append(l)
                        else:
                            self.result_data[k] = [l]

    def save_csv(self, output_dir: str):
        d = {}
        for func_name, func_data in self.result_data.items():
            a = np.array(func_data)
            d[func_name] = np.mean(a, axis=0)
        df = pd.DataFrame(list(d.values()), index=list(d.keys()))
        df.to_csv(os.path.join(output_dir, "result.csv"), header=False, index_label=True)

    @staticmethod
    def train(x_train, y_train, x_test, y_test):
        result = {}
        train_model = ModelFactory()
        for func in ["svm", "native_bayes", "random_forest", "decision_tree", "knn", "mlp"]:
            getattr(train_model, "build_" + func)()
            train_model.train(x_train, y_train)
            result[func] = train_model.evaluate(x_test, y_test, True)
        return result


class TaskA(TrainTask):

    def init_task(self):
        self.data_set = DocDataLoader("doc_vector", "/home/qian/Documents/Work/Data/SliceFeature/byte/")
        self.data_set.load_label("/home/qian/Documents/Work/Data/slice_label.csv")
        self.data_set.read_data()
        self.train_functions = {False: [TaskA.train], True: []}
        super().init_task()


class TaskB(TrainTask):

    def init_task(self):
        self.data_set = VectorDataLoader("ast_vector", "/home/qian/Documents/Work/Data/SliceFeature/astV/")
        self.data_set.load_label("/home/qian/Documents/Work/Data/label.csv")
        self.data_set.read_data(80)
        self.train_functions = {True: [TaskB.train], False: [TaskB.train_cnn, TaskB.train_lstm]}
        super().init_task()

    @staticmethod
    def train_cnn(x_train, y_train, x_test, y_test):
        train_model = ModelFactory()
        train_model.build_cnn((80, 16))
        train_model.train(x_train, y_train)
        return {"cnn": train_model.evaluate(x_test, y_test, True)}

    @staticmethod
    def train_lstm(x_train, y_train, x_test, y_test):
        train_model = ModelFactory()
        train_model.build_lstm()
        train_model.train(x_train, y_train)
        return {"lstm": train_model.evaluate(x_test, y_test, True)}


class TaskM(TrainTask):

    def init_task(self):
        self.data_set = ManualDataLoader("ast_vector", "/home/qian/Documents/Work/Data/ManualFeature/")
        self.data_set.load_label("/home/qian/Documents/Work/Data/label.csv")
        self.data_set.read_data()
        self.train_functions = {False: [TaskB.train], True: []}
        super().init_task()


class TaskW1(TrainTask):

    def init_task(self):
        self.data_set = WordDataLoader("ast_word", "/home/qian/Documents/Work/Data/SliceFeature/type")
        self.data_set.load_label("/home/qian/Documents/Work/Data/label.csv")
        self.data_set.read_data("Count")
        self.train_functions = {False: [TaskB.train], True: []}
        super().init_task()


class TaskW2(TrainTask):

    def init_task(self):
        self.data_set = WordDataLoader("ast_word", "/home/qian/Documents/Work/Data/SliceFeature/type")
        self.data_set.load_label("/home/qian/Documents/Work/Data/label.csv")
        self.data_set.read_data("Tf")
        self.train_functions = {False: [TaskB.train], True: []}
        super().init_task()
