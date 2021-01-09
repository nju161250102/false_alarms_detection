from sklearn.neighbors import KNeighborsClassifier
from .TrainModel import TrainModel


class KnnModel(TrainModel):

    def __init__(self):
        super().__init__()
        self.model = KNeighborsClassifier()
