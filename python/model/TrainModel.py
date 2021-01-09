from sklearn.metrics import *


class TrainModel:
    """
    训练模型的父类，新增模型时增加一个子类的实现
    train方法与predict方法提供默认实现
    """

    @staticmethod
    def transform_predict(y_predict):
        """
        将预测概率转换为0/1标记
        :param y_predict 预测概率
        """
        return [1 if row[0] > 0.5 else 0 for row in y_predict]

    def __init__(self):
        self.model = None

    def train(self, x_train, y_train):
        """
        调用model的train方法训练模型
        :param x_train 训练数据
        :param y_train 数据标签
        """
        self.model.fit(x_train, y_train)

    def predict(self, x_data) -> list:
        """
        调用model的predict方法预测数据标签
        :param x_data 预测数据
        """
        return self.model.predict(x_data)

    def evaluate(self, x_test, y_test, output=False) -> list:
        """
        评估模型效果
        :param x_test 测试数据
        :param y_test 测试数据的实际标签
        :param output 是否输出
        """
        y_predict = self.predict(x_test)
        acc = accuracy_score(y_test, y_predict)
        pre = precision_score(y_test, y_predict)
        rec = recall_score(y_test, y_predict)
        f1 = f1_score(y_test, y_predict)
        auc = roc_auc_score(y_test, y_predict)
        if output:
            print(acc, pre, rec, f1, auc)
        return [acc, pre, rec, f1, auc]