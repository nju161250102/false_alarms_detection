from sklearn.svm import SVC
from .TrainModel import TrainModel


class SvmModel(TrainModel):

    def __init__(self):
        super().__init__()
        self.model = SVC(kernel='rbf')
