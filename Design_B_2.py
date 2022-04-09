
import gym
import random
import numpy as np
import logBook_B
import Design_B             

class MinimalSubstrateEnvironment(Design_B.MinimalSubstrateEnvironment):
    def __init__(self, num_agents, max_init_no, max_value, max_generations,equation,no_dims):
        
        self.num_agents = num_agents
        self.max_init_no = max_init_no
        self.max_value = max_value
        self.max_generations = max_generations
        self.possible_agents = ["agent_" + str(r) for r in range(num_agents)]
        self.equation = equation
        self.no_dims = no_dims
        # Action space size of 2 per dimension: increase/decrease dimension by 1

        self._action_spaces = [gym.spaces.Discrete(2*no_dims) for i in range(self.num_agents)]
        # Observation space is 3: 0 if it beat more opponents last round, 1 if it lost more
        
        self._observation_spaces = [gym.spaces.Discrete(2) for i in range(self.num_agents)]

        
        self.reset()

    def reset(self):
        '''
        Returns the observations for each agent
        '''
        self.state = 0
        self.current_gen = -1
        
        #this defines the initial integers for both dimensions for every agent
        self.agents = [Design_B.agent([random.randint(0,self.max_init_no) for z in range(self.no_dims)],self.max_value) for i in range(self.num_agents)]
        self.rewards =  [0 for i in range(self.num_agents)]
        if self.equation == 1:
            self.calculateRewards_eq1()
        elif self.equation == 2:
            self.calculateRewards_eq2()
        elif self.equation == 3:
            self.calculateRewards_eq3()
        observations = self.oberserveAgents()
        return observations

    def oberserveAgents(self):
        halfway = (len(self.agents)//2)
        output = []
        for i in range(0,self.num_agents):
            if self.rewards[i]>=halfway:
                output.append(0)
            else:
                output.append(1)
        return(output)
        