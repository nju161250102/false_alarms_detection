from keras import Sequential
from keras.layers import Conv1D, Conv2D, MaxPool1D, MaxPool2D, GlobalAveragePooling1D, Dropout, Dense, LSTM, Flatten
from keras.utils import to_categorical
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import *
import numpy as np


class ModelFactory:
    """
    创建训练模型的工厂，具体的模型继承TrainModel父类
    """

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

    class SvmModel(TrainModel):

        def __init__(self):
            super().__init__()
            self.model = SVC(kernel='rbf')

    class BayesModel(TrainModel):

        def __init__(self):
            super().__init__()
            self.model = GaussianNB()

    class RandomForestModel(TrainModel):

        def __init__(self):
            super().__init__()
            self.model = RandomForestClassifier()

    class DecisionTreeModel(TrainModel):

        def __init__(self):
            super().__init__()
            self.model = DecisionTreeClassifier()

    class KnnModel(TrainModel):

        def __init__(self):
            super().__init__()
            self.model = KNeighborsClassifier()

    class MlpModel(TrainModel):
        def __init__(self):
            super().__init__()
            self.model = MLPClassifier(solver='lbfgs', alpha=1e-5, batch_size=8, hidden_layer_sizes=(30, 20), random_state=1)

    class CnnModel(TrainModel):

        def __init__(self, input_shape):
            super().__init__()
            self.model = Sequential()
            self.model.add(Conv1D(32, kernel_size=5, activation='relu', input_shape=input_shape))
            self.model.add(MaxPool1D(3))
            self.model.add(Conv1D(16, kernel_size=3, activation='relu'))
            self.model.add(MaxPool1D(3))
            self.model.add(GlobalAveragePooling1D())
            self.model.add(Dropout(0.1))
            self.model.add(Dense(32, activation='relu'))
            self.model.add(Dense(8, activation='relu'))
            self.model.add(Dense(2, activation='softmax'))
            self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        def train(self, x_train, y_train):
            self.model.fit(x_train, to_categorical(y_train), epochs=20, verbose=0)

        def predict(self, x_data) -> list:
            return self.transform_predict(self.model.predict(x_data))

    class Cnn2dModel(TrainModel):

        def __init__(self):
            super().__init__()
            self.model = Sequential()
            self.model.add(Conv2D(32, kernel_size=5, input_shape=(80, 16, 1), activation='relu'))
            self.model.add(MaxPool2D(pool_size=(3, 3)))
            self.model.add(Conv2D(16, kernel_size=(3, 3), activation='relu'))
            self.model.add(MaxPool2D(pool_size=(2, 2)))
            self.model.add(Flatten())
            self.model.add(Dense(100, activation='relu'))
            self.model.add(Dense(10, activation='relu'))
            self.model.add(Dense(2, activation='softmax'))
            self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        def train(self, x_train, y_train):
            self.model.fit(x_train, to_categorical(y_train), epochs=20, verbose=0)

        def predict(self, x_data) -> list:
            return self.transform_predict(self.model.predict(x_data))

    class LstmModel(TrainModel):

        def __init__(self, input_shape):
            super().__init__()
            self.model = Sequential()
            self.model.add(LSTM(80, input_shape=input_shape))
            self.model.add(Dense(80, activation='relu'))
            self.model.add(Dense(32, activation='relu'))
            self.model.add(Dense(16, activation='relu'))
            self.model.add(Dense(2, activation='softmax'))
            self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        def train(self, x_train, y_train):
            self.model.fit(x_train, to_categorical(y_train), epochs=20, verbose=0)

        def predict(self, x_data) -> list:
            return self.transform_predict(self.model.predict(x_data))

    def __init__(self):
        self.model = None

    def build_svm(self):
        self.model = self.SvmModel()

    def build_native_bayes(self):
        self.model = self.BayesModel()

    def build_random_forest(self):
        self.model = self.RandomForestModel()

    def build_decision_tree(self):
        self.model = self.DecisionTreeModel()

    def build_knn(self):
        self.model = self.KnnModel()

    def build_mlp(self):
        self.model = self.MlpModel()

    def build_cnn(self, input_shape=(80, 16)):
        self.model = self.CnnModel(input_shape)

    def build_cnn2(self):
        self.model = self.Cnn2dModel()

    def build_lstm(self, input_shape=(80, 16)):
        self.model = self.LstmModel(input_shape)

    def train(self, x_train, y_train, reshape=None):
        if self.model is not None:
            self.model.train(np.array(x_train) if reshape is None else np.array(x_train).reshape(reshape), y_train)

    def evaluate(self, x_test, y_test, output=False, reshape=None) -> list:
        if self.model is not None:
            return self.model.evaluate(np.array(x_test) if reshape is None else np.array(x_test).reshape(reshape), y_test, output)
