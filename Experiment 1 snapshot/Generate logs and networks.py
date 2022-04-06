import Design_B
import Design_C
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