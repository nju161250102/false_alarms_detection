from sklearn.ensemble import RandomForestClassifier
from .TrainModel import TrainModel


class RandomForestModel(TrainModel):

    def __init__(self):
        super().__init__()
        self.model = RandomForestClassifier()
