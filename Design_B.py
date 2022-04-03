##pip install gym
##pip install matplotlib

import gym
import random
import numpy as np
import logBook_B
import os
class agent:
    def __init__(self, firstDim, secondDim):
        self.first = firstDim
        self.second = secondDim
        self.zMax = 3
        self.maxVal = 100

    def __getitem__(self, key):
        if key == 0:
            return(self.first)
        else:
            return(self.second)
    def __str__(self):
        return(str(self.toList()))
    def toList(self):
        return([self.first,self.second])
    def takeAction(self, action):
        
        z = random.randint(1,self.zMax)
        if action==0:
            if self.first+z > self.maxVal:
                self.first = self.maxVal
            else:
                self.first+=z
        elif action ==1:
            if self.first-z < 0:
                self.first = 0
            else:
                self.first-=z
        elif action == 2:
            if self.second+z > self.maxVal:
                self.second = self.maxVal
            else:
                self.second+=z
        elif action == 3:
            if self.second-z < 0:
                self.second = 0
            else:
                self.second-=z

class agent_single_dimension:
    def __init__(self, firstDim):
        self.first = firstDim
        self.zMax = 3
        self.maxVal = 100
    def getValue(self):
        return(self.first)

    def __str__(self):
        return(str(self.toList()))
    def toList(self):
        return([self.first])
    def takeAction(self, action):
        
        z = random.randint(1,self.zMax)
        if action==0:
            if self.first+z > self.maxVal:
                self.first = self.maxVal
            else:
                self.first+=z
        elif action ==1:
            if self.first-z < 0:
                self.first = 0
            else:
                self.first-=z
                
        
                    
class MinimalSubstrateEnvironment:
    def __init__(self, num_agents, max_init_no, max_generations,equation):
        
        self.num_agents = num_agents
        self.max_init_no = max_init_no
        self.max_generations = max_generations
        self.possible_agents = ["agent_" + str(r) for r in range(num_agents)]
        self.equation = equation
         
        if self.equation ==1:
            # Action space size of 2: increase/decrease dimension by 1

            self._action_spaces = [gym.spaces.Discrete(2) for i in range(self.num_agents)]
            # Observation space is the number of agents greater than, equal to or less than itself 
            
            self._observation_spaces = [gym.spaces.Discrete(3) for i in range(self.num_agents)]

        else:

            # Action space size of 4: increase/decrease dimension x by 1, increase/decrease dimension y by 1

            self._action_spaces =[gym.spaces.Discrete(4) for i in range(self.num_agents)]
            # Observation space is the number of agents greater than, equal to or less, than in both dimension     
            
            self._observation_spaces = [gym.spaces.Discrete(6) for i in range(self.num_agents)]

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
        if self.equation ==1:
            self.agents = [agent_single_dimension(random.randint(0,self.max_init_no)) for i in range(self.num_agents)]
        else:
            self.agents = [agent(random.randint(0,self.max_init_no),random.randint(0,self.max_init_no)) for i in range(self.num_agents)]
        observations = self.oberserveAgents()
        return observations

    def step(self, actions):
        
        #actions is a num_agents length list. action[i] is applied to agent[i]
        #every agent takes the action assigned to it.
        
        self.current_gen+=1

        for i in range(self.num_agents):
            self.agents[i].takeAction(actions[i])

        self.rewards =  [0 for i in range(self.num_agents)]
        if self.equation == 1:
            self.calculateRewards_eq1()
        elif self.equation == 2:
            self.calculateRewards_eq2()
        elif self.equation == 3:
            self.calculateRewards_eq3()
        rewards=self.rewards
        observations = self.oberserveAgents()

        if self.current_gen == self.max_generations-1:
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
        if self.equation == 1:
            counter = np.array([[0,0,0] for _ in range(max)])
            output = []
            for i in range(max):
                for x in range(latest,max):
                    if i!=x:
                        a=self.agents[i]
                        b=self.agents[x]
                        #dimension x
                        if a.getValue()>b.getValue():
                            counter[i][2]+=1
                            counter[x][0]+=1
                        elif  a.getValue()<b.getValue():
                            counter[i][0]+=1
                            counter[x][2]+=1
                        else:
                            counter[i][1]+=1
                            counter[x][1]+=1
                output.append(np.argmax(counter[i]))
                latest+=1

        else:
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
    def calculateRewards_eq1(self):
        #calculates the score for every agent by comparing them against every other agent
        latest = 1
        max = len(self.agents)
        for i in range(max):
            for x in range(latest,max):
                if i!=x:
                    a = self.agents[i]
                    b = self.agents[x]
                    if a.getValue()>b.getValue():
                        self.rewards[i] = self.rewards[i] + 1
                        
                    elif a.getValue()<b.getValue():
                        self.rewards[x] = self.rewards[x] + 1
            latest+=1
            
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
        self.directory = "./nets/"
        self.env = env
        self.no_agents = self.env.num_agents
        #the qNetwork has no_agents many q tables, 1 for each agent. At initialisation every q table is full of 0s
        #init at 0
        self.q_table = [np.zeros((self.env._observation_spaces[i].n, self.env._action_spaces[i].n)) for i in range(self.no_agents)]
        
        
        self.hyperparameters = hyperparameters

    def train(self, maxIter):
        self.log = logBook_B.logbook(self.env.equation)
        timesActionsTaken = [0 for i in range(self.env._action_spaces[0].n)]
        for iter in range(0,maxIter):
            state = self.env.reset()
            
            epochs = 0
            done = False
            while not done:
                actions = []
                for i in range(self.no_agents):
                    if (random.uniform(0, 1) < self.hyperparameters[2]):
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
                    new_value = old_value + self.hyperparameters[0] * (rewards[i] + self.hyperparameters[1] * next_max - old_value)
                    self.q_table[i][state[i]][actions[i]] = new_value
                    
                    
                self.log.addEntry([self.env.current_gen,self.env.returnAgents(),rewards])
                state = next_state
                epochs += 1
                if epochs%50==0:
                    print("Epoch:{}".format(epochs))
                   
                    
            print("Iteration:{}".format(iter))
            print("Times actions taken",timesActionsTaken)

    def saveNetwork(self,fileName):
        file_path = os.path.join(self.directory, fileName)
        f=open(file_path,"w")
        for line in self.q_table:
            f.write(str(line))
            f.write("\n")
        f.close()

