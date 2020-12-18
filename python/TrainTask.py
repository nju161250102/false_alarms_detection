import numpy as np
from DataSet import *
from TrainModel import ModelFactory


class TrainTask:
    """
    Task：在某一类数据上训练不同的机器学习模型，评估效果并进行对比
    具体的训练任务继承此父类，配置合适的数据处理方法与使用的模型
    data_set: 数据集，应当使用DataLoader的子类得到
    result_data: 评估结果，{模型名: [acc, pre, rec, f1, auc]}
    train_functions: 训练方法，{False: [], True: []}，表明数据是否需要被降维处理，以便于列表中的模型使用
        每个训练方法使用x_train, y_train, x_test, y_test四个参数，返回和result_data格式一致的dict
    以上成员变量在子类的 init_task 方法中初始化
    """

    def __init__(self):
        self.data_set = None
        self.result_data = {}
        self.train_functions = {False: [], True: []}

    def init_task(self):
        pass

    def run(self, num: int, rate: float):
        """
        运行当前的训练任务
        :param num 数据集划分-训练-评估的循环次数
        :param rate 训练集划分比率
        """
        self.init_task()
        for i in range(num):
            for flag in [False, True]:
                if len(self.train_functions[flag]) == 0:
                    continue
                # 在划分前设置数据集属性
                self.data_set.compress_flag = flag
                # 根据划分比率得到一个划分结果
                x_train, y_train, x_test, y_test = self.data_set.split_data(rate)
                for func in self.train_functions[flag]:
                    # 将训练评估结果整合到result_data中
                    for k, l in func(self, x_train, y_train, x_test, y_test).items():
                        if k in self.result_data.keys():
                            self.result_data[k].append(l)
                        else:
                            self.result_data[k] = [l]

    def get_result(self):
        """
        获取平均值计算后的结果
        """
        d = {}
        for func_name, func_data in self.result_data.items():
            a = np.array(func_data)
            d[func_name] = np.mean(a, axis=0)
        return d

    def train(self, x_train, y_train, x_test, y_test):
        """
        传统机器学习模型训练方法的整合
        """
        result = {}
        train_model = ModelFactory()
        for func in ["svm", "native_bayes", "random_forest", "decision_tree", "knn", "mlp"]:
            getattr(train_model, "build_" + func)()
            train_model.train(x_train, y_train)
            result[func] = train_model.evaluate(x_test, y_test, True)
        return result


class VectorTask(TrainTask):
    """
    使用向量数据的训练任务
    """

    def __init__(self, data_dir: str, label_file: str, feature_size: int, seq_len=80):
        self.data_dir = data_dir
        self.label_file = label_file
        self.feature_size = feature_size
        self.seq_len = seq_len
        super().__init__()

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
        return {"cnn": train_model.evaluate(x_test, y_test, True)}

    def train_lstm(self, x_train, y_train, x_test, y_test):
        train_model = ModelFactory()
        train_model.build_lstm((self.seq_len, self.feature_size))
        train_model.train(x_train, y_train)
        return {"lstm": train_model.evaluate(x_test, y_test, True)}


class ManualTask(TrainTask):

    def __init__(self, data_dir: str, label_file: str):
        self.data_dir = data_dir
        self.label_file = label_file
        super().__init__()

    def init_task(self):
        self.data_set = ManualDataLoader(self.data_dir)
        self.data_set.load_label(self.label_file)
        self.data_set.read_data()
        self.train_functions = {False: [ManualTask.train], True: []}
        super().init_task()


class WordTask(TrainTask):

    def __init__(self, data_dir: str, label_file: str, counter: str):
        self.data_dir = data_dir
        self.label_file = label_file
        self.counter = counter
        super().__init__()

    def init_task(self):
        self.data_set = WordDataLoader(self.data_dir)
        self.data_set.load_label(self.label_file)
        self.data_set.read_data(self.counter)
        self.train_functions = {False: [WordTask.train], True: []}
        super().init_task()
