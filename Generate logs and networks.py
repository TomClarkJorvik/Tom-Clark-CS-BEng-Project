import Design_B
import Design_C
import numpy as np
import logBook_B

# Hyperparameters
#learning rate
alpha = 0.1
#discount factor
gamma = 0.6
#epsilon allows for a greed/reward balance
epsilon = 0.2
hyperparameters = [alpha,gamma,epsilon]

#Experiment 1

no_iterations = 50

max_initial_number = 10
max_value = 100
max_generations = 100
equation = 1
no_dims = 1
num_agents_B = 25
num_agents_C = 50
popCutoff=25

env_B = Design_B.MinimalSubstrateEnvironment(num_agents_B, max_initial_number, max_value, max_generations, equation, no_dims)
q_B = Design_B.qNetwork(env_B,hyperparameters)
q_B.train(no_iterations)
q_B.log.saveLogbook("logB1.txt")
q_B.saveNetwork("netB1.txt")

env_C = Design_B.MinimalSubstrateEnvironment(num_agents_C, max_value, max_initial_number,max_generations, 1, 1)
q_C = Design_C.qNetwork(env_C,hyperparameters,popCutoff)
q_C.train(no_iterations)
q_C.log.saveLogbook("logC1.txt")
q_C.saveNetwork("netC1.txt")

env_B_2inds = Design_B.MinimalSubstrateEnvironment(2, max_initial_number, max_value, max_generations, equation, no_dims)
q_B_2inds = Design_B.qNetwork(env_B_2inds,hyperparameters)
q_B_2inds.train(no_iterations)
q_B_2inds.log.saveLogbook("logB1_2inds.txt")
q_B_2inds.saveNetwork("netB1_2inds.txt")

#Experiment 2

no_iterations = 50

max_initial_number = 10
max_value = 100
max_generations = 100
equation = 2
num_agents_B = 25

env_B = Design_B.MinimalSubstrateEnvironment(num_agents_B, max_initial_number, max_value, max_generations, equation, 2)
q_B = Design_B.qNetwork(env_B,hyperparameters)
q_B.train(no_iterations)
q_B.log.saveLogbook("logB2.txt")
q_B.saveNetwork("netB2.txt")

env_B_2 = Design_B.MinimalSubstrateEnvironment(num_agents_B, max_initial_number, 50, max_generations, equation, 10)
q_B_2 = Design_B.qNetwork(env_B,hyperparameters)
q_B_2.train(no_iterations)
q_B.log.saveLogbook("logB2-10dims.txt")
q_B.saveNetwork("netB2-10dims.txt")


#Experiment 3

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