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

    def get_action_set(self) -> dict:
        """Dict of all possible actions
        - key[int]: input for the action
        - value: action

        Returns:
            dict: dict of all action
        """
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
    
    def close_env(self):
        """
        Cleans inmemory data for the enviroment
        - CLEAN AFTER YOU ARE DONE
        """
        self.env.close()

    def fresh_start(self):
        """
        Reset Every time you need to do a fresh start
        - like when you die
        - want to restart from begining
        """
        self.env.reset()
    
    def get_env_state(self) -> dict:
        """Get Environment Details
        
        {
            'state': env.state,
            'reward': env.reward,
            'isdead': env.isdead,
            'info': env.info,
        }

        Returns:
            dict: environment Details
        """
        respTuple = self.env.step(0)
        respData = dict()
        respData['state'] = respTuple[0]
        respData['reward'] = respTuple[1]
        respData['isdead'] = respTuple[2]
        respData['info'] = respTuple[3]
        return respData
    
    # TODO: make it happen
    def get_miv_env(self):
        """ Still in progress """
        envConfig = self.get_env_state()
        envState = envConfig['state']
        envState = [np.argmax(pixel) for pixel in envState]
        return envState
    
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
        return [None, None, True, None]
    
    def play_game(self, moveCount: int = 0):
        """Play game using interface

        - After playing make sure to restart
        
        Key input [int] :
            Enter your move: range(0,7)
            Do you want to restart: {
                -1: Do Nothing
                 0: ShutDown preview
                else: Reset and Restart
            }


        Args:
            moveCount (int, optional): 
                key for action to take from self.get_action_set. 
                Defaults to 0.
        """
        self.fresh_start()
        self.env.render()
        for cou in range(moveCount):
            move_indx = int(input("Enter your move: "))
            for _ in range(30):
                state, reward, done, info = self.make_move(move_indx)
                self.env.render()

            if done:
                self.fresh_start()
                restart = int(input("Do you want to restart: "))
                if (restart == -1):
                    pass
                elif (restart == 0):
                    break
                                


    
    def generate_random_file_name(self):
        if not os.path.isdir(self.SAVE_DESTINALTION):
            os.makedirs(self.SAVE_DESTINALTION)
        fileContentCount = len(os.listdir(self.SAVE_DESTINALTION))
        return f"MarioEnv{fileContentCount}.npy"

    
    def save_env(self, destination: str = ""):
        """ Dont Really need it """
        if destination == "":
            if not os.path.isdir(self.SAVE_DESTINALTION):
                os.makedirs(self.SAVE_DESTINALTION)
        else:
            self.SAVE_DESTINALTION = destination

        fileDestination = os.path.join(
            self.SAVE_DESTINALTION, self.generate_random_file_name()
        )

        fileContent = self.get_env_state()

        with open( fileDestination , 'w') as savedModel:
            np.save(
                fileDestination,
                np.array(list(fileContent.items()), dtype=object)
            )
    
    def load_env(self, fileLocation: str = ""):
        """ Dont really need it """
        if (fileLocation == ""):
            raise Exception("File Location Not Provided")
        elif not os.path.isfile(fileLocation):
            raise Exception("Invalid File Location")
        
        fileContent = dict()

        with open(fileLocation, 'rb') as fileObj:
            fileListContent = np.load(fileObj, allow_pickle=True)
        
        for item in fileListContent:
            fileContent[item[0]] = item[1]
            
        return fileContent
    
