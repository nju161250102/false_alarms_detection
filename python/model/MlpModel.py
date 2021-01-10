from sklearn.neural_network import MLPClassifier
from .TrainModel import TrainModel


class MlpModel(TrainModel):
    def __init__(self):
        super().__init__()
        self.model = MLPClassifier(solver='lbfgs',
                                   activation='logistic',
                                   batch_size=8,
                                   hidden_layer_sizes=(50, 10),
                                   max_iter=500,
                                   random_state=1)
