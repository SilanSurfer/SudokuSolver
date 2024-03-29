import tensorflow as tf
import numpy as np
import logging


class DigitRecognizer:
    def __init__(self, logging_level):
        self._model = self._build_model()
        self._is_model_trained = False
        self._logger = self._set_logger(logging_level)

    def _set_logger(self, logging_level):
        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging_level)
        streamHandler.setFormatter(
            logging.Formatter('%(name)s[%(levelname)s]: %(message)s'))
        logger = logging.getLogger(type(self).__name__)
        logger.setLevel(logging_level)
        logger.addHandler(streamHandler)
        return logger

    def _build_model(self):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10, activation='softmax')
        ])

        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=["accuracy"])

        model.summary()

        return model

    def _load_data(self):
        mnist_dataset = tf.keras.datasets.mnist
        (x_train, y_train), (x_test, y_test) = mnist_dataset.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0
        return x_train, y_train, x_test, y_test

    def train_model(self, epochs):
        x, y, _, _ = self._load_data()
        self._model.fit(x, y, epochs=epochs)
        self._is_model_trained = True

    def evaluate_model(self):
        if not self._is_model_trained:
            self._logger.error("Model wasn't trained!!! Either train model" +
                               " or load stored weights!!!")
            return

        _, _, x_test, y_test = self._load_data()
        loss, acc = self._model.evaluate(x_test, y_test, verbose=0)
        self._logger.info(f"loss: {loss}, accuracy: {acc}")

    def save_weights(self, filename='model/digit_recognizer_weights.hdf5'):
        if not self._is_model_trained:
            self._logger.error("I can't save model since it wasn't trained!")
            return
        self._model.save_weights(filename)
        self._logger.info(f"Model was saved in {filename}")

    def load_weights(self, filename='model/digit_recognizer_weights.hdf5'):
        self._model.load_weights(filename)
        self._is_model_trained = True
        self._logger.info(f"Weights for model were loaded from: {filename}")

    def predict(self, digit_image):
        return np.argmax(self._model.predict(digit_image))


if __name__ == "__main__":
    recognizer = DigitRecognizer(logging.DEBUG)
    recognizer.load_weights()
    recognizer.evaluate_model()
