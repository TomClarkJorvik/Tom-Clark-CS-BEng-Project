import Design_B
import Design_C
import random
import numpy as np
import logBook_B
import Design_B_2
# Hyperparameters
#learning rate
alpha = 0.1
#discount factor
gamma = 0.6
#epsilon allows for a greed/reward balance
epsilon = 0.2
hyperparameters = [alpha,gamma,epsilon]
no_iterations = 50

max_initial_number = 10
max_value = 100
max_generations = 100
equation = 3
num_agents_B = 25

env_B = Design_B.MinimalSubstrateEnvironment(num_agents_B, max_initial_number, max_value, max_generations, equation, 2)
q_B = Design_B.qNetwork(env_B,hyperparameters)
q_B.train(no_iterations)
q_B.log.saveLogbook("logB3.txt")
q_B.saveNetwork("netB3.txt")

env_B_2 = Design_B.MinimalSubstrateEnvironment(num_agents_B, max_initial_number, max_value, 300, equation, 2)
q_B_2 = Design_B.qNetwork(env_B_2,hyperparameters)
q_B_2.loadNetwork("netB3.txt")
state = env_B_2.reset()
done = False
logbook = logBook_B.logbook(3)
while not done:
    actions = []
    for i in range(num_agents_B):
        actions.append(np.argmax(q_B_2.q_table[i][state[i]]))
    state, rewards, done, info = env_B_2.step(actions)

    logbook.addEntry([env_B_2.current_gen,env_B_2.returnAgents(),rewards])
logbook.saveLogbook("logB3_2.txt")