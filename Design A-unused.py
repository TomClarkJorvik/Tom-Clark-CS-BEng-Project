#pip install gym

import gym
import random
import numpy as np
import logBook



class agent:
    def __init__(self, firstDim, secondDim):
        self.first = firstDim
        self.second = secondDim
        self.mutpb = 0.05

    def __getitem__(self, key):
        #returns the unitation of a dimension
        if key == 0:
            return(sum(self.first))
        else:
            return(sum(self.second))
    def __str__(self):
        return(str(self.toList()))
    def toList(self):
        return([sum(self.first),sum(self.second)])
    def takeAction(self, action):
        #flips a random bit at a random index, or does nothing.
        if action == 0:
            for i in range(len(self.first)):
                if random.uniform(0,1) < 0.05:
                    self.first[i] = 1-self.first[i]
        elif action == 1:
            for i in range(len(self.second)):
                if random.uniform(0,1) < 0.05:
                    self.second[i] = 1-self.second[i]     
        #else, no change to either
    def takeActionOld(self, action):
        #flips a random bit at a random index, or does nothing.
        if action == 0:
            index = random.randint(0,len(self.first)-1)
            self.first[index] = 1 - self.first[index]
        elif action == 1:
            index = random.randint(0,len(self.second)-1)
            self.second[index] = 1 - self.second[index]      
        #else, no change to either
        
                    
class MinimalSubstrateEnvironment(gym.Env):
    def __init__(self, num_agents, max_scalar_no, max_generations,equation):
        '''
        The init method takes in environment arguments and
         should define the following attributes:
        - possible_agents
        - action_spaces
        - observation_spaces
        These attributes should not be changed after initialization.
        '''
        self.num_agents = num_agents
        self.max_scalar_no = max_scalar_no
        self.max_generations = max_generations
        self.possible_agents = ["agent_" + str(r) for r in range(num_agents)]
        self.equation = equation
        
        # Action space size of 5: increase/decrease dimension x by 1, increase/decrease dimension y by 1, or do nothing
        #self._action_spaces = {agent: gym.spaces.Discrete(5) for agent in self.possible_agents}
        self._action_spaces =[gym.spaces.Discrete(3) for agent in self.possible_agents]
        # Observation space is the number of agents greater than, equal to or less, than in both dimension     
        #self._observation_spaces = {agent:  gym.spaces.Discrete(2) for agent in self.possible_agents}
        self._observation_spaces = [gym.spaces.Discrete(6) for agent in self.possible_agents]
        self.reset()
    def render(self):
        pass
    def getNumberOfStates(self):
        gym.spaces.Discrete(6)
        return()


    def reset(self):
        '''
        Returns the observations for each agent
        '''
        self.state = 0
        self.current_gen = -1
        dimLength = 100 
        #this defines the initial scalar values for both dimensions for every agent
        self.agents = [agent([random.randint(0,1) for x in range(max_scalar_no)],[random.randint(0,1) for y in range(max_scalar_no)]) for i in range(self.num_agents)]
        observations = self.oberserveAgents()
        return observations

    def step(self, actions):
        
        #actions is a num_agents length list. action[i] is applied to agent[i]
        #every agent takes the action assigned to it.
        
        self.current_gen+=1

        for i in range(len(actions)):
            self.agents[i].takeAction(actions[i])

        self.rewards =  [0 for i in range(len(self.possible_agents))]

        if self.equation == 2:
            self.calculateRewards_eq2()
        elif self.equation == 3:
            self.calculateRewards_eq3()
        rewards=self.rewards
        observations = self.oberserveAgents()

        if self.current_gen == self.max_generations:
            done = True
        else:
            done = False

        #info placeholder
        info = {}

        return observations, rewards, done, info
    def returnAgents(self):
        output = []
        for agent in self.agents:
            output.append(agent.toList())
        return(output)
    
    def oberserveAgents(self):
        max = len(self.agents)
        latest = 1
        #calculates the observation for each agent
        # count = [number of other agents greater than itself in dimension x,equal in x,less than in x,
            #  greater than in dimension y,equal in y,less than in y]
        # output for agent i = 0 if count[i][0] is the largest, 1 if count[i][1] is the largest etc
        counter = np.array([[0,0,0,0,0,0] for _ in range(max)])
        output = []
        for i in range(max):
            for x in range(latest,max):
                if i!=x:
                    a=self.agents[i]
                    b=self.agents[x]
                    #dimension x
                    if a[0]>b[0]:
                        counter[i][2]+=1
                        counter[x][0]+=1
                    elif a[0]<b[0]:
                        counter[i][0]+=1
                        counter[x][2]+=1
                    else:
                        counter[i][1]+=1
                        counter[x][1]+=1
                    #dimension y
                    if a[1]>b[1]:
                        counter[i][5]+=1
                        counter[x][3]+=1
                    elif a[1]<b[1]:
                        counter[i][3]+=1
                        counter[x][5]+=1
                    else:
                        counter[i][4]+=1
                        counter[x][4]+=1  
            output.append(np.argmax(counter[i]))
            latest+=1

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
            
        elif a[dimension]<b[dimension]:
            self.rewards[indexB] = self.rewards[indexB] + 1
            
        #if they are equal, neither is rewarded.

class qNetwork:
    def __init__(self, env, hyperparameters):
        
        self.env = env
        self.no_agents = self.env.num_agents
        #the qNetwork has no_agents many q tables, 1 for each agent. At initialisation every q table is full of 0s
        #init at 0
        self.q_table = [np.zeros((self.env._observation_spaces[i].n, self.env._action_spaces[i].n)) for i in range(self.no_agents)]
        
        
        self.hyperparameters = hyperparameters

    def train(self, maxIter):
        self.log = logBook.logbook()
        timesActionsTaken = [0 for i in range(self.env._action_spaces[0].n)]
        for iter in range(0,maxIter):
            state = self.env.reset()
            
            epochs = 0
            done = False
            while not done:
                actions = []
                for i in range(self.no_agents):
                    if (random.uniform(0, 1) < epsilon):
                        actions.append(self.env._action_spaces[i].sample()) # Explore action space
                    elif all(v == 0 for v in self.q_table[i][state[i]]):
                        # if the q table's entry for that state is an array of 0's: i.e. no actions tested for that state
                        actions.append(self.env._action_spaces[i].sample()) # Explore action space
                    else:
                        actions.append(np.argmax(self.q_table[i][state[i]])) # Exploit learned values
                    timesActionsTaken[actions[i]]+=1
                
                next_state, rewards, done, info = self.env.step(actions)
                
                
                for i in range(self.no_agents):
                    old_value = self.q_table[i][state[i]][actions[i]]
                    next_max = np.max(self.q_table[i][next_state[i]])
                    new_value = old_value + alpha * (rewards[i] + gamma * next_max - old_value)
                    self.q_table[i][state[i]][actions[i]] = new_value
                    
                    
                self.log.addEntry([env.current_gen,env.returnAgents(),rewards])
                state = next_state
                epochs += 1
                if epochs%50==0:
                    print("Epoch:{}".format(epochs))
                   
                    
            print("Iteration:{}".format(iter))
            print("Times actions taken",timesActionsTaken)
    def saveNetwork(self,fileName):
        f=open(fileName,"w")
        for line in self.q_table:
            f.write(str(line))
            f.write("\n")
        f.close()

# Hyperparameters
#learning rate
alpha = 0.1
#discount factor
gamma = 0.6
#epsilon allows for a greed/reward balance
epsilon = 0.2
hyperparameters = [alpha,gamma,epsilon]
max_iters = 15

num_agents = 25
max_scalar_no = 100
max_generations = 100
env = MinimalSubstrateEnvironment(num_agents, max_scalar_no, max_generations, 3)
q = qNetwork(env,hyperparameters)
q.train(max_iters)

q.log.saveLogbook("logA.txt")
q.saveNetwork("netA.txt")

#there is a natural bias to take the 0th action, irregardless of whether it improves reward or not
