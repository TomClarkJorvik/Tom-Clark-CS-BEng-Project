#pip install gym
#pip install tensorflow
#pip install pettingzoo

import gym
import tensorflow as tf
from tf_agents.agents import tf_agent
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




class MinimalSubstrateEnvironment(gym.Env):
    def __init__(self, num_agents, max_no):
        '''
        The init method takes in environment arguments and
         should define the following attributes:
        - possible_agents
        - action_spaces
        - observation_spaces

        These attributes should not be changed after initialization.
        '''
        self.possible_agents = ["agent_" + str(r) for r in range(num_agents)]
        #this defines the initial integers for both dimensions for every agent
        self.agent_name_mapping = dict(zip(self.possible_agents, [[random.randint(0,max_no),random.randint(0,max_no)] for i in range(num_agents)] ))

        # Gym spaces are defined and documented here: https://gym.openai.com/docs/#spaces

        # Action space size of 2: increase dimension x or increase dimension y
        self._action_spaces = {agent: gym.spaces.Discrete(2) for agent in self.possible_agents}
        # Observation space is both dimensions for every agent
        self._observation_spaces = {agent:  gym.spaces.Discrete(2) for agent in self.possible_agents}

    def render(self):
        pass

    def reset(self):
        '''
        Reset needs to initialize the `agents` attribute and must set up the
        environment so that render(), and step() can be called without issues.

        Here it initializes the `num_moves` variable which counts the number of
        hands that are played.

        Returns the observations for each agent
        '''
        self.agents = self.possible_agents[:]
        self.num_gen = 0
        observations = {agent: None for agent in self.agents}
        return observations

    def step(self, actions):
        '''
        step(action) takes in an action for each agent and should return the
        - observations
        - rewards
        - dones
        - infos
        dicts where each dict looks like {agent_1: item_1, agent_2: item_2}
        '''
        # If a user passes in actions with no agents, then just return empty observations, etc.
        if not actions:
            self.agents = []
            return {}, {}, {}, {}

        # rewards for all agents are placed in the rewards dictionary to be returned
        rewards = {}
        for agent in self.agents:
            agent

        rewards[self.agents[0]], rewards[self.agents[1]] = REWARD_MAP[(actions[self.agents[0]], actions[self.agents[1]])]

        self.num_gen += 1
        env_done = self.num_moves >= NUM_ITERS
        dones = {agent: env_done for agent in self.agents}

        # current observation is just the other player's most recent action
        observations = {self.agents[i]: int(actions[self.agents[1 - i]]) for i in range(len(self.agents))}

        # typically there won't be any information in the infos, but there must
        # still be an entry for each agent
        infos = {agent: {} for agent in self.agents}

        if env_done:
            self.agents = []

        return observations, rewards, dones, infos




class MSAgent(tf_agent.TFAgent):
    def __init__(self):
        self.data=1
        #super(SignAgent, self).__init__(time_step_spec=time_step_spec,action_spec=action_spec,policy=policy,collect_policy=policy,train_sequence_length=None)

a = MinimalSubstrateEnvironment(25, 10)
