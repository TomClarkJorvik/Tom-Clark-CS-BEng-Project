import logBook_B
import logBook_C
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




