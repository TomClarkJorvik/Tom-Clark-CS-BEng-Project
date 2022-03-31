import Design_B
# Hyperparameters
#learning rate
alpha = 0.1
#discount factor
gamma = 0.6
#epsilon allows for a greed/reward balance
epsilon = 0.2
hyperparameters = [alpha,gamma,epsilon]
max_iters = 15

num_agents = 25
max_initial_number = 10
max_generations = 100
env = Design_B.MinimalSubstrateEnvironment(num_agents, max_initial_number, max_generations, 3)
q = Design_B.qNetwork(env,hyperparameters)
q.train(max_iters)

q.log.saveLogbook("logB.txt")
q.saveNetwork("netB.txt")
