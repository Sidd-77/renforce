import tensorflow as tf
import numpy as np
import random
import pygame
from deep_q import GameAI, Player, Stones, ALLOW_INPUT, CREATE_STONE, X_POSITIONS
from collections import deque
from model import Model, Trainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self) -> None:
        self.n_game = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        # TODO: Implement the model
        self.model = Model(input_shape=(10, ), lr=LR)
        self.trainer = Trainer(model=self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        state = list()
        for stone in game.stones_list[:4]:
            state.append(stone.x/120)
            state.append(720-stone.y)
        state.append(game.player.x/120)
        state.append(720-game.player.y)
        state = np.array(state)
        print("Deguggging=================================================")
        print(state)
        return state

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory > BATCH_SIZE):
            mini_sample = random.sample(self.memory.BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)


    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step([state], [action], [reward], [next_state], [done])

    def get_action(self, state):
        # Random moves : Exploration/Exploitation Tradeoff
        self.epsilon = 100 - self.n_game
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon : 
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = np.array(state, dtype=np.float32)
            state0 = np.reshape(state0, (1, 10))
            prediction = self.model.predict(state0)
            move = np.argmax(prediction[0])
            final_move[move] = 1

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = GameAI()

    while True:
        old_state = agent.get_state(game)
        final_move = agent.get_action(old_state)
        reward, game_over, score = game.play_step(action=final_move)
        new_state = agent.get_state(game)
        agent.train_short_memory(old_state, final_move, reward, new_state, game_over)
        agent.remember(old_state, final_move, reward, new_state, game_over)

        if game_over:
            # train long memory
            game.reset()
            agent.n_game += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game:', agent.n_game, 'Score:', score, 'Record:', record)
            # TODO: Ploting


if __name__=="__main__":
    train()
