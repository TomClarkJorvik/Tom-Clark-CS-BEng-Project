#pip install gym
#pip install tensorflow
#pip install pettingzoo

import gym
import tensorflow as tf
import pettingzoo
import random

def env():
    env = MinimalSubstrateEnvironment()
    # This wrapper is only for environments which print results to the terminal
    env = pettingzoo.wrappers.CaptureStdoutWrapper(env)
    # this wrapper helps error handling for discrete action spaces
    env = pettingzoo.wrappers.AssertOutOfBoundsWrapper(env)
    # Provides a wide vareity of helpful user errors
    # Strongly recommended
    env = pettingzoo.wrappers.OrderEnforcingWrapper(env)
    return env

def policy(obs, agent):
    action = 1
    return action

class agent:
    def __init__(self, firstDim, secondDim):
        self.first = firstDim
        self.second = secondDim
        self.reward = 0
    def incrementReward(self):
        self.reward+=1
    def resetReward(self):
        self.reward=0
    def __getitem__(self, key):
        if key == 0:
            return(self.first)
        else:
            return(self.second)
    def takeAction(self, action):
        if action==0:
            self.first+=1
        elif action == 1:
            self.second+=1
        #else, no increase to either
                    
class MinimalSubstrateEnvironment(gym.Env):
    def __init__(self, num_agents, max_init_no, max_generations):
        '''
        The init method takes in environment arguments and
         should define the following attributes:
        - possible_agents
        - action_spaces
        - observation_spaces
        These attributes should not be changed after initialization.
        '''
        self.num_agents = num_agents
        self.max_init_no = max_init_no
        self.max_generations = max_generations
        self.possible_agents = ["agent_" + str(r) for r in range(num_agents)]
        
        # Gym spaces are defined and documented here: https://gym.openai.com/docs/#spaces

        # Action space size of 3: increase dimension x by 1, increase dimension y by 1 or do nothing
        self._action_spaces = {agent: gym.spaces.Discrete(3) for agent in self.possible_agents}
        # Observation space is both dimensions for every agent (UNSURE; MIGHT BE ALL POSSIBLE VALUES IT CAN GO UP TO? USE BOX?)
        self._observation_spaces = {agent:  gym.spaces.Discrete(2) for agent in self.possible_agents}

    def render(self):
        pass

    def reset(self):
        '''
        Returns the observations for each agent
        '''
        self.state = 0
        self.num_gen = 0
        
        #this defines the initial integers for both dimensions for every agent
        self.agents = dict(zip(self.possible_agents[:], 
            [agent(random.randint(0,self.max_init_no),random.randint(0,self.max_init_no)) for i in range(self.num_agents)] ))
        observations = self.agents
        return observations

    def step(self, actions):
        
        self.rewards =  dict(zip(list(self.agents.keys())[:], [0 for i in range(len(self.possible_agents))] ))
        observations = self.agents
        for key in self.agents.keys():
            self.agents[key].resetReward()
        self.calculateRewards_eq2()
        rewards=self.rewards

        return observations, rewards #, dones, infos
    
    def calculateRewards_eq2(self):
        #calculates the score for every agent by comparing them against every other agent
        latest = 1
        keys = list(self.agents.keys())
        max = len(keys)
        for key in keys:
            for i in range(latest,max):
                if keys[i]!=key:
                    a = self.agents[key]
                    b = self.agents[keys[i]]
                    if abs(a[0]-b[0]) > abs(a[1]-b[1]):
                        dim=0
                    #IF BOTH DIMENSIONS EQUIDISTANT => DEFAULTS TO DIMENSION Y
                    else:
                        dim=1
                    self.compare(key,keys[i],a,b,dim)
            latest+=1

    def calculateRewards_eq3(self):
        latest = 1
        keys = list(self.agents.keys())
        max = len(keys)
        for key in keys:
            for i in range(latest,max):
                if keys[i]!=key:
                    a = self.agents[key]
                    b = self.agents[keys[i]]
                    if abs(a[0]-b[0]) < abs(a[1]-b[1]):
                        dim=0
                    #IF BOTH DIMENSIONS EQUIDISTANT => DEFAULTS TO DIMENSION Y
                    else:
                        dim=1
                    self.compare(key,keys[i],a,b,dim)
            latest+=1

    def compare(self,key1,key2,a,b,dimension):
        if a[dimension]>b[dimension]:
            self.rewards.update({key1:self.rewards[key1] + 1})
            a.incrementReward()
        elif a[dimension]<b[dimension]:
            self.rewards.update({key2:self.rewards[key2] + 1})
            b.incrementReward()
        #if they are equal, neither is rewarded.

    def test(self):
        self.reset()
        self.step([])
        for key in self.agents.keys():
            print(self.agents[key].reward)


a = MinimalSubstrateEnvironment(25, 10, 100)
a.test()
