#pip install gym
#pip install tensorflow

import gym
import tensorflow as tf
from tf_agents.agents import tf_agent

class MinimalSubstrateEnvironment:
    def __init__(self):
        self.data=1


class MSAgent(tf_agent.TFAgent):
    def __init__(self):
        self.data=1
        #super(SignAgent, self).__init__(time_step_spec=time_step_spec,action_spec=action_spec,policy=policy,collect_policy=policy,train_sequence_length=None)