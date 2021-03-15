from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
import os, json
import numpy as np

class SimpleMario():
    def __init__(self):

        self.BASE_DIR = os.getcwd()
        self.SAVE_DESTINALTION = os.path.join(self.BASE_DIR, "saved_model")
        
        self.env = gym_super_mario_bros.make('SuperMarioBros-v0') 
        self.env = JoypadSpace(self.env, SIMPLE_MOVEMENT)

        self.valid_move_indx = set(range(7))
        
        self.fresh_start()

    def get_action_set(self):
        # ['NOOP', 'right', 'right A', 'right B', 'right A B', 'A', 'left']
        return dict({
            0: "stay",
            1: "forward",
            2: "forward , A ,",
            3: "forward , B ",
            4: "forward , A , B",
            5: "jump",
            6: "backward"
        })

    def fresh_start(self):
        """Reset Every time we need to do a fresh start"""
        self.env.reset()
    
    def get_env_state(self):
        respTuple = self.env.step(0)
        respData = dict()
        respData['state'] = respTuple[0]
        respData['reward'] = respTuple[1]
        respData['isdead'] = respTuple[2]
        respData['info'] = respTuple[3]
        return respData
    
    def make_move(self, move):
        """Returns Null is invalid input
        valid input: self.get_action_set()

        Args:
            move (int): move index

        Returns:
            tuple: 
                - (numpy.ndarray) the state as a result of the action
                - (float) the reward achieved by taking the action
                - (bool) a flag denoting whether the episode has ended
                - (dict) a dictionary of extra information
        """
        if move in self.valid_move_indx:
            return self.env.step(move)
        return None
    
    def generate_random_file_name(self):
        if not os.path.isdir(self.SAVE_DESTINALTION):
            os.makedirs(self.SAVE_DESTINALTION)
        fileContentCount = len(os.listdir(self.SAVE_DESTINALTION))
        return f"MarioEnv{fileContentCount}.npy"

    
    def save_env(self, destination: str = ""):
        if destination == "":
            if not os.path.isdir(self.SAVE_DESTINALTION):
                os.makedirs(self.SAVE_DESTINALTION)
        else:
            self.SAVE_DESTINALTION = destination

        fileDestination = os.path.join(
            self.SAVE_DESTINALTION, self.generate_random_file_name()
        )

        with open( fileDestination , 'w') as savedModel:
            np.save(fileDestination, self.get_env_state())
    
    def load_env(self, fileLocation: str = ""):
        if (fileLocation == ""):
            raise Exception("File Location Not Provided")
        elif not os.path.isfile(fileLocation):
            raise Exception("Invalid File Location")
        
        fileContent = None

        with open(fileLocation, 'r') as fileObj:
            fileContent = np.load(fileObj)
            
        return fileContent



        
    def close_env(self):
        self.env.close()
    
