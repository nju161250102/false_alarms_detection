from keras import Sequential
from keras.layers import Dense, LSTM
from keras.utils import to_categorical
from .TrainModel import TrainModel


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
