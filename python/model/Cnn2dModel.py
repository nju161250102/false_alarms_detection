from keras import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten
from keras.utils import to_categorical
from .TrainModel import TrainModel


class Cnn2dModel(TrainModel):

    def __init__(self):
        super().__init__()
        self.model = Sequential()
        self.model.add(Conv2D(32, kernel_size=5, input_shape=(80, 16, 1), activation='relu'))
        self.model.add(MaxPool2D(pool_size=(3, 3)))
        self.model.add(Conv2D(16, kernel_size=(3, 3), activation='relu'))
        self.model.add(MaxPool2D(pool_size=(2, 2)))
        self.model.add(Flatten())
        self.model.add(Dense(100, activation='relu'))
        self.model.add(Dense(10, activation='relu'))
        self.model.add(Dense(2, activation='softmax'))
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    def train(self, x_train, y_train):
        self.model.fit(x_train, to_categorical(y_train), epochs=20, verbose=0)

    def predict(self, x_data) -> list:
        return self.transform_predict(self.model.predict(x_data))
