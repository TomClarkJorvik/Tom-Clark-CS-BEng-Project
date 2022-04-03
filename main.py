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
max_iters = 50

max_initial_number = 10
max_generations = 100
equation = 1
num_agents_B = 25
env_B = Design_B.MinimalSubstrateEnvironment(num_agents_B, max_initial_number, max_generations, equation)
q_B = Design_B.qNetwork(env_B,hyperparameters)
q_B.train(max_iters)

q_B.log.saveLogbook("logB1_2inds.txt")
q_B.saveNetwork("netB1_2inds.txt")

# num_agents_C = 50
# popCutoff = 25
# env_C = Design_C.MinimalSubstrateEnvironment(num_agents_C, max_initial_number, max_generations, equation, popCutoff)
# q_C = Design_C.qNetwork(env_C,hyperparameters)
# q_C.train(max_iters)
# q_C.log.saveLogbook("logC1.txt")
# q_C.saveNetwork("netC1.txt")

q_B.log.plotLogbook()
# q_C.log.plotLogbook()