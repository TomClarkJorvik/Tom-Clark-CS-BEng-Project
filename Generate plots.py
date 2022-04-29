import logBook_B
import logBook_C

#Experiment 1
equation = 1

l1 = logBook_B.logbook(equation)
l1.loadLogbook("logB1.txt")
l1.plotLogbook("fig1.svg")
l1.plot_one_iteration("fig2.svg",49)

l2 = logBook_C.logbook(equation,25)
l2.loadLogbook("logC1.txt")
l2.plotLogbook("fig3.svg")

l3 = logBook_B.logbook(equation)
l3.loadLogbook("logB1_2inds.txt")
l3.plotLogbook_only2inds("fig4.svg")
l3.plotLogbook_2inds_one_iteration("fig5.svg",48)
l3.plotLogbook_2inds_one_iteration("fig6.svg",49)

#Experiment 2
equation = 2

l4 = logBook_B.logbook(equation)
l4.loadLogbook("logB2.txt")
l4.plot_obj_fitness_and_rewards("fig7.svg")

l5 = logBook_B.logbook(equation,scalarLabel="Scalar Value",maxScalarValue=50)
l5.loadLogbook("logB2-10dims.txt")
l5.plot_obj_fitness_and_rewards("fig8.svg")
l5.plot_one_iteration("fig9.svg",49)

#Experiment 3
equation = 3

l6 = logBook_B.logbook(equation,scalarLabel="Scalar Value")
l6.loadLogbook("logB3.txt")
l6.plot_obj_fitness_and_rewards_one_iteration("fig10.svg",49)

l7 = logBook_B.logbook(equation,scalarLabel="Scalar Value")
l7.loadLogbook("logB3_2.txt")
l7.plotLogbook("fig11.svg")

