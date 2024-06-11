import tensorflow as tf
import numpy as np
import os

class Model:
    def __init__(self, input_shape=(10,), lr=0.001) -> None:
        self.lr= lr
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=lr)
        self.model = self.create_model(input_shape)


    def create_model(self, input_shape):
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Dense(activation='relu', units=40, input_shape=input_shape))
        #model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(units=128, activation='relu'))
        model.add(tf.keras.layers.Dropout(0.15))
        model.add(tf.keras.layers.Dense(units=3, activation='softmax'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.lr), metrics=['accuracy'])
        model.summary()
        return model

    # def load(self):
    #     if os.path.isfile('model.h5'):
    #         self.model.load_weights('model.h5')

    def predict(self, state):
        return self.model.predict(state)

    def train(self, input, output, epochs, verbose=True):
        self.model.fit(input, output, epochs=epochs, verbose=verbose)
        #self.model.save('model.h5')

    def save(self):
        self.model.save('model.h5')


class Trainer:
    def __init__(self, model, lr, gamma) -> None:
        self.model = model
        self.lr = lr
        self.gamma = gamma
    

    def train_step(self, states, actions, rewards, next_states, dones):

        states = np.array(states, dtype=np.float32)
        actions = np.array(actions, dtype=np.float32)
        rewards = np.array(rewards, dtype=np.float32)
        next_states = np.array(next_states, dtype=np.float32)
        dones = np.array(dones, dtype=np.int32)

        pred = self.model.predict(states)
        target = pred.copy()

        for ind in range(len(dones)):
            Q_new = rewards[ind]
            if not dones[ind]:
                Q_new = rewards[ind] + self.gamma * np.max(self.model.predict([next_states[ind]]))

            target[ind][np.argmax(actions[ind])] = Q_new
        
        


