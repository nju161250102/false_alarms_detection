from sklearn.neural_network import MLPClassifier
from .TrainModel import TrainModel


class MlpModel(TrainModel):
    def __init__(self):
        super().__init__()
        self.model = MLPClassifier(solver='lbfgs', alpha=1e-5, batch_size=8, hidden_layer_sizes=(30, 20),
                                   random_state=1)
