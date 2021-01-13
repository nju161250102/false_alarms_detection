import gc
import logging
import numpy as np
from model import ModelFactory


class TrainTask:
    """
    Task：在某一类数据上训练不同的机器学习模型，评估效果并进行对比
    具体的训练任务继承此父类，配置合适的数据处理方法与使用的模型
    feature_name: 任务对应的特征分类名称
    vector_method: 任务对特征使用的向量处理方法名称
    data_set: 数据集，应当使用DataLoader的子类得到
    result_data: 评估结果，{模型名: [[acc, pre, rec, f1, auc],...]}
    train_functions: 训练方法，{False: [], True: []}，表明数据是否需要被降维处理，以便于列表中的模型使用
        每个训练方法使用self, x_train, y_train, x_test, y_test五个参数，返回和result_data格式一致的dict
    以上成员变量在子类的 init_task 方法中初始化
    """

    def __init__(self, feature_name: str, vector_method: str):
        self.feature_name = feature_name
        self.vector_method = vector_method
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
        logging.info("Feature Name: %s, vector: %s" % (self.feature_name, self.vector_method))
        self.init_task()
        logging.info("Init success")
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

    def get_result_lines(self):
        """
        先进行平均值计算，然后生成一个字典列表，用于构建Dataframe
        :return list[dict]
        """
        lines = []
        for func_name, func_data in self.result_data.items():
            arr = []
            for data in func_data:
                if min(data) > 0.01:
                    arr.append(data)
            measure_result = np.mean(np.array(arr), axis=0)
            lines.append({
                "feature": self.feature_name,
                "to_vector": self.vector_method,
                "model_name": func_name,
                "acc": measure_result[0],
                "pre": measure_result[1],
                "rec": measure_result[2],
                "f1": measure_result[3],
                "auc": measure_result[4],
            })
        return lines

    def clear(self):
        """

        """
        del self.data_set
        self.data_set = None
        gc.collect()


    def train(self, x_train, y_train, x_test, y_test):
        """
        传统机器学习模型训练方法的整合
        """
        result = {}
        train_model = ModelFactory()
        for func in ["svm", "native_bayes", "random_forest", "decision_tree", "knn", "mlp"]:
            getattr(train_model, "build_" + func)()
            train_model.train(x_train, y_train)
            result[func] = train_model.evaluate(x_test, y_test)
        return result
