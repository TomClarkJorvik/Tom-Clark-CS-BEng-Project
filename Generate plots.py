import logBook_B
import logBook_C
equation = 2

l1 = logBook_B.logbook(equation)
l1.loadLogbook("logB2.txt")
l1.plot_obj_fitness_and_rewards()

l2 = logBook_B.logbook(equation,scalarLabel="Scalar Value",maxScalarValue=50)
l2.loadLogbook("logB2-10dims.txt")
l2.plot_obj_fitness_and_rewards()
l2.plot_one_iteration(49)




