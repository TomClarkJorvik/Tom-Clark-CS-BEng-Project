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
