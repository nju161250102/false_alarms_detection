import numpy as np
from .CnnModel import CnnModel
from .Cnn2dModel import Cnn2dModel
from .LstmModel import LstmModel
from .BayesModel import BayesModel
from .DecisionTreeModel import DecisionTreeModel
from .KnnModel import KnnModel
from .MlpModel import MlpModel
from .RandomForestModel import RandomForestModel
from .SvmModel import SvmModel


class ModelFactory:
    """
    创建训练模型的工厂，具体的模型继承TrainModel父类
    """

    def __init__(self):
        self.model = None

    def build_svm(self):
        self.model = SvmModel()

    def build_native_bayes(self):
        self.model = BayesModel()

    def build_random_forest(self):
        self.model = RandomForestModel()

    def build_decision_tree(self):
        self.model = DecisionTreeModel()

    def build_knn(self):
        self.model = KnnModel()

    def build_mlp(self):
        self.model = MlpModel()

    def build_cnn(self, input_shape=(80, 16)):
        self.model = CnnModel(input_shape)

    def build_cnn2(self):
        self.model = Cnn2dModel()

    def build_lstm(self, input_shape=(80, 16)):
        self.model = LstmModel(input_shape)

    def train(self, x_train, y_train, reshape=None):
        if self.model is not None:
            self.model.train(np.array(x_train) if reshape is None else np.array(x_train).reshape(reshape), y_train)

    def evaluate(self, x_test, y_test, output=False, reshape=None) -> list:
        if self.model is not None:
            return self.model.evaluate(np.array(x_test) if reshape is None
                                       else np.array(x_test).reshape(reshape), y_test, output)
