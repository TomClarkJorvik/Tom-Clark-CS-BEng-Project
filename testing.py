import Design_B
import Design_C
import numpy as np
import matplotlib.pyplot as plt
import logBook_B
import logBook_C
equation = 1

# logger = logBook_B.logbook()
# logger.loadLogbook("logB1.txt")
logger = logBook_C.logbook(equation,25)
logger.loadLogbook("logC2.txt")
#logger.plotRewards()
logger.plotLogbook()
#logger.plotInds()
#logger.plotLogbook()
#logger.plotTwoInds()
#logger.plotIndividual(0)



