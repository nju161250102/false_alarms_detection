from sklearn.naive_bayes import GaussianNB
from .TrainModel import TrainModel


class BayesModel(TrainModel):

    def __init__(self):
        super().__init__()
        self.model = GaussianNB()
