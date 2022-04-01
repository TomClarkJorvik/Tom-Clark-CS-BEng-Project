##pip install gym
##pip install matplotlib

import gym
import random
import numpy as np
import logBook_C
import Design_B
                    
class MinimalSubstrateEnvironment(Design_B.MinimalSubstrateEnvironment):
    def __init__(self, num_agents, max_init_no, max_generations,equation,popCutoff):
        
        self.num_agents = num_agents
        self.max_init_no = max_init_no
        self.max_generations = max_generations
        self.possible_agents = ["agent_" + str(r) for r in range(num_agents)]
        self.equation = equation
        self.popCutoff = popCutoff
        
        if equation ==1:
            # Action space size of 2: increase/decrease dimension by 1

            self._action_spaces =[gym.spaces.Discrete(2) for i in range(2)]
            # Observation space is the number of agents greater than, equal to or less than itself 
            
            self._observation_spaces = [gym.spaces.Discrete(3) for i in range(2)]

        else:

            # Action space size of 4: increase/decrease dimension x by 1, increase/decrease dimension y by 1

            self._action_spaces =[gym.spaces.Discrete(4) for i in range(2)]
            # Observation space is the number of agents greater than, equal to or less, than in both dimension     
            
            self._observation_spaces = [gym.spaces.Discrete(6) for i in range(2)]


        self.reset()

    def step(self, actions):
        
        #actions is a 2 length list. action[0] is applied to agents from population 0
        #action[1] is applied to agents from population 1
        #population is determined by the popCutoff
        
        self.current_gen+=1

        for i in range(self.num_agents):
            if i<self.popCutoff:
               self.agents[i].takeAction(actions[0])
            else:
                self.agents[i].takeAction(actions[1])

        self.rewards =  [0 for i in range(len(self.possible_agents))]

        if self.equation == 1:
            self.calculateRewards_eq2()
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

class qNetwork(Design_B.qNetwork):
    def __init__(self, env, hyperparameters):
        self.directory = "./nets/"      
        self.env = env
        self.no_agents = self.env.num_agents
        self.popCutoff = self.env.popCutoff
        #this qNetwork has 2 q tables, 1 for each population. At initialisation both q tables are full of 0s
        #init at 0
        self.q_table = [np.zeros((self.env._observation_spaces[i].n, self.env._action_spaces[i].n)) for i in range(2)]
        
        self.hyperparameters = hyperparameters

    def train(self, maxIter):
        self.log = logBook_C.logbook(self.env.equation,self.popCutoff)
        timesActionsTaken = [0 for i in range(self.env._action_spaces[0].n)]
        for iter in range(0,maxIter):
            state = self.env.reset()
            
            epochs = 0
            done = False
            while not done:
                actions = []
                for i in range(self.no_agents):
                    if i<self.popCutoff:
                        popNo=0
                    else:
                        popNo=1
                    if (random.uniform(0, 1) < self.hyperparameters[2]):
                        actions.append(self.env._action_spaces[popNo].sample()) # Explore action space
                    elif all(v == 0 for v in self.q_table[popNo][state[i]]):
                        # if the q table's entry for that state is an array of 0's: i.e. no actions tested for that state
                        actions.append(self.env._action_spaces[popNo].sample()) # Explore action space
                    else:
                        actions.append(np.argmax(self.q_table[popNo][state[i]])) # Exploit learned values
                    timesActionsTaken[actions[i]]+=1
                
                next_state, rewards, done, info = self.env.step(actions)
                
                
                for i in range(self.no_agents):
                    if i<self.popCutoff:
                        popNo=0
                    else:
                        popNo=1
                    old_value = self.q_table[popNo][state[i]][actions[i]]
                    next_max = np.max(self.q_table[popNo][next_state[i]])
                    new_value = old_value + self.hyperparameters[0] * (rewards[i] + self.hyperparameters[1] * next_max - old_value)
                    self.q_table[popNo][state[i]][actions[i]] = new_value
                    
                    
                self.log.addEntry([self.env.current_gen,self.env.returnAgents(),rewards])
                state = next_state
                epochs += 1
                if epochs%50==0:
                    print("Epoch:{}".format(epochs))
                   
                    
            print("Iteration:{}".format(iter))
            print("Times actions taken",timesActionsTaken)


