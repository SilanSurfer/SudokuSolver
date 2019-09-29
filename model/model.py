import tensorflow as tf


# TODO: save model weights in separate file

def load_data():
    mnist_dataset = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist_dataset.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    return x_train, y_train, x_test, y_test


def build_model():
    global model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=["accuracy"])


def train_model(x, y, epochs: int):
    model.fit(x, y, epochs=epochs)


def evaluate_model(x_test, y_test):
    loss, acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"loss: {loss}, accuracy: {acc}")


def main():
    epochs = 10
    x_train, y_train, x_test, y_test = load_data()
    build_model()
    train_model(x_train, y_train, epochs)
    evaluate_model(x_test, y_test)


if __name__ == "__main__":
    main()