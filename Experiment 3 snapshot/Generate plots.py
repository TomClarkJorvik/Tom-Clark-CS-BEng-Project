import logBook_B
import logBook_C
equation = 3

l1 = logBook_B.logbook(equation,scalarLabel="Scalar Value")
l1.loadLogbook("logB3.txt")
l1.plot_obj_fitness_and_rewards_one_iteration(49)

l2 = logBook_B.logbook(equation,scalarLabel="Scalar Value")
l2.loadLogbook("logB3_2.txt")
l2.plotLogbook()


