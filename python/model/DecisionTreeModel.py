from sklearn.tree import DecisionTreeClassifier
from .TrainModel import TrainModel


class DecisionTreeModel(TrainModel):

    def __init__(self):
        super().__init__()
        self.model = DecisionTreeClassifier()
