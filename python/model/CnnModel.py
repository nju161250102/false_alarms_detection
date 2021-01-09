from keras import Sequential
from keras.layers import Conv1D, MaxPool1D, GlobalAveragePooling1D, Dropout, Dense
from keras.utils import to_categorical
from .TrainModel import TrainModel


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
