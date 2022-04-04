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
max_value = 50
max_generations = 100
equation = 2
no_dims = 10
num_agents_B = 25

# env_B = Design_B.MinimalSubstrateEnvironment(num_agents_B, max_initial_number, max_value, max_generations, equation, no_dims)
# q_B = Design_B.qNetwork(env_B,hyperparameters)
# q_B.train(no_iterations)
# q_B.log.saveLogbook("logB2-10dims.txt")
# q_B.saveNetwork("netB2-10dims.txt")

num_agents_C = 50
popCutoff=50
env_C = Design_B.MinimalSubstrateEnvironment(num_agents_C, max_value, max_initial_number,max_generations, 1, 1)
q_C = Design_C.qNetwork(env_C,hyperparameters,popCutoff)
q_C.train(5)
q_C.log.saveLogbook("testing.txt")