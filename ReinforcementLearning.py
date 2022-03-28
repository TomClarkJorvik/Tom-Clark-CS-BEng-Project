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

class logbook:
    def __init__(self):
        self.log = []
    def addEntry(self,entry):
        self.log.append(entry)
    def printLogbook(self):
        for entry in self.log:
            print("Generation :",entry[0],"\n")
            print("Observation :",entry[1],"\n")
            print("Rewards :",entry[2],"\n")

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
    def __str__(self):
        return(str(self.toList))
    def toList(self):
        return([self.first,self.second])
    def takeAction(self, action):
        if action==0:
            self.first+=1
        elif action ==1:
            if self.first!=0:
                self.first-=1
        elif action == 2:
            self.second+=1
        elif action == 3:
            if self.second!=0:
                self.second-=1
        #else, no increase to either
    def decideAction(self):
        return(random.randint(0,4))
                    
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

        # Action space size of 5: increase/decrease dimension x by 1, increase/decrease dimension y by 1, or do nothing
        self._action_spaces = {agent: gym.spaces.Discrete(5) for agent in self.possible_agents}
        # Observation space is both dimensions for every agent (UNSURE; MIGHT BE ALL POSSIBLE VALUES IT CAN GO UP TO? USE BOX?)
        self._observation_spaces = {agent:  gym.spaces.Discrete(2) for agent in self.possible_agents}
        self.reset()
    def render(self):
        pass

    def reset(self):
        '''
        Returns the observations for each agent
        '''
        self.state = 0
        self.current_gen = -1
        
        #this defines the initial integers for both dimensions for every agent
        self.agents = [agent(random.randint(0,self.max_init_no),random.randint(0,self.max_init_no)) for i in range(self.num_agents)]
        observations = self.agents
        return observations

    def step(self, actions):
        
        #actions is a num_agents length list. action[i] is applied to agent[i]
        #every agent takes the action assigned to it.
        
        self.current_gen+=1

        for i in range(len(actions)):
            self.agents[i].takeAction(actions[i])

        self.rewards =  [0 for i in range(len(self.possible_agents))]
        observations = self.oberserveAgents()
        for agent in self.agents:
            agent.resetReward()
        self.calculateRewards_eq2()
        rewards=self.rewards

        if self.current_gen == self.max_generations:
            done = True
        else:
            done = False

        #info placeholder
        info = {}

        return observations, rewards, done, info
    
    def oberserveAgents(self):
        output = []
        for agent in self.agents:
            output.append(agent.toList())
        return(output)

    def calculateRewards_eq2(self):
        #calculates the score for every agent by comparing them against every other agent
        latest = 1
        max = len(self.agents)
        for i in range(max):
            for x in range(latest,max):
                if i!=x:
                    a = self.agents[i]
                    b = self.agents[x]
                    if abs(a[0]-b[0]) > abs(a[1]-b[1]):
                        dim=0
                    #IF BOTH DIMENSIONS EQUIDISTANT => DEFAULTS TO DIMENSION Y
                    else:
                        dim=1
                    self.compare(i,x,a,b,dim)
            latest+=1

    def calculateRewards_eq3(self):
        latest = 1
        max = len(self.agents)
        for i in range(max):
            for x in range(latest,max):
                if i!=x:
                    a = self.agents[i]
                    b = self.agents[x]
                    if abs(a[0]-b[0]) < abs(a[1]-b[1]):
                        dim=0
                    #IF BOTH DIMENSIONS EQUIDISTANT => DEFAULTS TO DIMENSION Y
                    else:
                        dim=1
                    self.compare(i,x,a,b,dim)
            latest+=1
        
    def compare(self,indexA,indexB,a,b,dimension):
        if a[dimension]>b[dimension]:
            self.rewards[indexA] = self.rewards[indexA] + 1
            a.incrementReward()
        elif a[dimension]<b[dimension]:
            self.rewards[indexB] = self.rewards[indexB] + 1
            b.incrementReward()
        #if they are equal, neither is rewarded.

    def decideActions(self):
        actions = []
        for agent in self.agents:
            actions.append(agent.decideAction())
        return(actions)

num_agents = 25
max_initial_number = 10
max_generations = 100
a = MinimalSubstrateEnvironment(num_agents, max_initial_number, max_generations)
flag = True
log = logbook()
while flag:
    actions = a.decideActions()
    obs, rewards, done, info = a.step(actions)
    log.addEntry([a.current_gen,obs,rewards])
    if done:
        flag = False

log.printLogbook()


