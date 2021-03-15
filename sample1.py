from mario_agent import SimpleMario
import os
import numpy as np

mario_env = SimpleMario()

mario_env.play_game(1000)

# mario_env.save_env()

mario_env.close_env()


# loadedData = mario_env.load_env(os.path.join(
#     mario_env.SAVE_DESTINALTION, "MarioEnv1.npy"
# ))
# print(loadedData)





# from nes_py.wrappers import JoypadSpace
# import gym_super_mario_bros
# from gym_super_mario_bros.actions import SIMPLE_MOVEMENT

# env = gym_super_mario_bros.make('SuperMarioBros-v0')
# env = JoypadSpace(env, SIMPLE_MOVEMENT)

# done = True
# for step in range(300):
#     if done:
#         state = env.reset()
#     state, reward, done, info = env.step(5)
#     env.render()

# env.close()


