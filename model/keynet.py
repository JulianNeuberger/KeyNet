from keras import Model
from keras.callbacks import TensorBoard
from keras.layers import Input, Conv2D, MaxPool2D, Flatten, Dense

from data.provider import get_all


def keynet_v1() -> Model:
    input_layer = Input(shape=(500, 500, 3))
    x = Conv2D(filters=32, kernel_size=(5, 5))(input_layer)
    x = MaxPool2D(pool_size=(3, 3))(x)
    x = Conv2D(filters=32, kernel_size=(5, 5))(x)
    x = MaxPool2D(pool_size=(3, 3))(x)
    x = Conv2D(filters=32, kernel_size=(5, 5))(x)
    x = MaxPool2D(pool_size=(3, 3))(x)
    x = Flatten()(x)
    x = Dense(units=100)(x)
    x = Dense(units=2, activation='softmax')(x)
    model = Model(inputs=input_layer, outputs=x)
    model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


def train():
    model = keynet_v1()
    x, y = get_all()
    tensorboard_callback = TensorBoard(log_dir='logs/keynetv1')
    model.fit(x=x, y=y, callbacks=[tensorboard_callback], batch_size=32, epochs=100, shuffle=True)


train()
