from DataSet import *
from TrainModel import ModelFactory
from TrainTask import *

if __name__ == "__main__":
    # data_set = VectorDataLoader("word_vector", "/home/qian/Documents/Work/Data/MethodFeature/wordV/")
    # data_set.load_label("/home/qian/Documents/Work/Data/label.csv")
    # data_set.read_data(80)
    # X_train, y_train, X_test, y_test = data_set.split_data(0.7)
    # train_model = ModelFactory()
    # train_model.build_cnn2()
    # train_model.train(X_train, y_train, reshape=(-1, 80, 16, 1))
    # train_model.evaluate(X_test, y_test, True, reshape=(-1, 80, 16, 1))
    t = TaskA()
    t.run(5, 0.7)
    t.save_csv("/home/qian")
