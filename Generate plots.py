import logBook_B
import logBook_C

#Experiment 1
equation = 1

l1 = logBook_B.logbook(equation)
l1.loadLogbook("logB1.txt")
l1.plotLogbook()
l1.plot_one_iteration(49)
l2 = logBook_C.logbook(equation,25)
l2.loadLogbook("logC1.txt")
l2.plotLogbook()
l3 = logBook_B.logbook(equation)
l3.loadLogbook("logB1_2inds.txt")
l3.plotLogbook_only2inds()
l3.plotLogbook_2inds_one_iteration(48)
l3.plotLogbook_2inds_one_iteration(49)

#Experiment 2
equation = 2

l1 = logBook_B.logbook(equation)
l1.loadLogbook("logB2.txt")
l1.plot_obj_fitness_and_rewards()

l2 = logBook_B.logbook(equation,scalarLabel="Scalar Value",maxScalarValue=50)
l2.loadLogbook("logB2-10dims.txt")
l2.plot_obj_fitness_and_rewards()
l2.plot_one_iteration(49)

#Experiment 3
equation = 3

l1 = logBook_B.logbook(equation,scalarLabel="Scalar Value")
l1.loadLogbook("logB3.txt")
l1.plot_obj_fitness_and_rewards_one_iteration(49)

l2 = logBook_B.logbook(equation,scalarLabel="Scalar Value")
l2.loadLogbook("logB3_2.txt")
l2.plotLogbook()


