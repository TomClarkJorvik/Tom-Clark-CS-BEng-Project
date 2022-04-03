import Design_B
import Design_C
import numpy as np
import matplotlib.pyplot as plt
import logBook_B
import logBook_C
equation = 1

logger = logBook_B.logbook(equation)
logger.loadLogbook("logB1_2inds.txt")
logger.plotLogbook_only2inds()

# logger = logBook_C.logbook(equation,25)
# logger.loadLogbook("logC1.txt")
# logger.plotLogbook()




