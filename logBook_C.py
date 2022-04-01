import matplotlib.pyplot as plt
import numpy as np
import random
import logBook_B
#This construct is simply for saving and loading log entries, and displaying graphs
#Designed for Design C
class logbook(logBook_B.logbook):
    def __init__(self,equation,popCutoff):
        self.log = []
        self.gens = []
        self.inds = []
        self.equation = equation
        self.rewards = []
        self.no_gens = 0
        self.popCutoff = popCutoff
        self.directory = "./logs/"

    def addAverageRewards(self, mainArray, toAddArray,no_gens,no_iterations):
        totIndsRewards=[0 for z in range(no_gens)]
        for x in range(no_gens*no_iterations):
            index=x%no_gens
            totIndsRewards[index]+=toAddArray[x]
        for i in range(no_gens):
            mainArray[i] += totIndsRewards[i]/no_iterations
        return(mainArray)

    def calcAverageRewards(self,rewards,no_gens,no_iterations,no_individuals):
        popAverageReward = [[0 for i in range(no_gens)] for x in range(2)]
        
        for i in range(no_individuals):
            indsRewards=rewards[:,i]
            if i<self.popCutoff:
                popAverageReward[0] = self.addAverageRewards(popAverageReward[0],indsRewards,no_gens,no_iterations)
            else:
                popAverageReward[1] = self.addAverageRewards(popAverageReward[1],indsRewards,no_gens,no_iterations)
        
        for i in range(no_gens):
            popAverageReward[0][i] = popAverageReward[0][i]/(no_iterations)
            popAverageReward[1][i] = popAverageReward[1][i]/(no_iterations)
        return(popAverageReward)

    def addAverageScalars(self, mainArray, toAddArray,no_gens,no_iterations,no_dims):
        totInds=[[0,0] for z in range(no_gens)]
            
        for x in range(no_gens*no_iterations):
            index=x%no_gens
            for y in range(0,no_dims):
                totInds[index][y]+=toAddArray[x][y]
        for z in range(no_gens):
            for y in range(0,no_dims):
                mainArray[z][y] += totInds[z][y]/no_iterations
        return(mainArray)
    
    def calcAverageScalars(self,individuals,no_gens,no_iterations,no_individuals,no_dims):
        popAverageScalars = [[[0 for z in range(no_dims)] for i in range(no_gens)] for x in range(2)]
        
        for i in range(no_individuals):
            indsScalars=individuals[:,i]
            if i<self.popCutoff:
                popAverageScalars[0] = self.addAverageScalars(popAverageScalars[0],indsScalars,no_gens,no_iterations,no_dims)
            else:
                popAverageScalars[1] = self.addAverageScalars(popAverageScalars[1],indsScalars,no_gens,no_iterations,no_dims)
        
        for i in range(no_gens):
            for y in range(0,no_dims):
                popAverageScalars[0][i][y] = popAverageScalars[0][i][y]/(no_iterations)
                popAverageScalars[1][i][y] = popAverageScalars[1][i][y]/(no_iterations)
        return(popAverageScalars)


    def plotRewards(self):
        rewards = np.array(self.rewards)
        no_individuals = len(rewards[0])
        no_gens = self.no_gens+1
        no_iterations = int(len(rewards)/no_gens)
        gensToPlot = [i for i in range(no_gens)]
        colourMap = self.getColourMap()
        popAverageReward = self.calcAverageRewards(rewards,no_gens,no_iterations,no_individuals)
        fig, axes = plt.subplots(2, 1, constrained_layout=True)
        
        for i in range(2):
            axes[i].set_xlabel("Generation")
            axes[i].set_ylabel("Rewards")
            #axes[i].set_ylim([0, 1])
            axes[i].plot(gensToPlot, popAverageReward[i], color=colourMap[i*4])

        plt.show()

    def plotInds(self):
        individuals = np.array(self.inds)
        no_individuals = len(individuals[0])
        no_gens = self.no_gens+1
        no_iterations = int(len(individuals)/no_gens)
        no_dims = len(individuals[0][0])
        gensToPlot = [i for i in range(no_gens)]
        colourMap = self.getColourMap()
        popAverageScalars = self.calcAverageScalars(individuals,no_gens,no_iterations,no_individuals,no_dims)
        
        fig, axes = plt.subplots(1, 1, constrained_layout=True)
        axes.set_xlabel("Generation")
        axes.set_ylabel("Scalars")
        for i in range(no_dims):
            axes.plot(gensToPlot, popAverageScalars[i], color=colourMap[i*4])

        plt.show()

    def plotLogbook(self):
        rewards = np.array(self.rewards)
        individuals = np.array(self.inds)
        no_individuals = len(rewards[0])
        no_gens = self.no_gens+1
        no_iterations = int(len(rewards)/no_gens)
        colourMap = self.getColourMap()
        
        #Rewards
        fig, axes = plt.subplots(2, 1, constrained_layout=True)
        gensToPlot = [i for i in range(no_gens)]
        no_dims = len(individuals[0][0])

        popAverageReward = self.calcAverageRewards(rewards,no_gens,no_iterations,no_individuals)
        popAverageScalars = self.calcAverageScalars(individuals,no_gens,no_iterations,no_individuals,no_dims)
        
        
        #Plotting
        for i in range(2):
            axes[0].set_xlabel("Generation")
            axes[0].set_ylabel("Average Rewards")
            axes[0].plot(gensToPlot, popAverageReward[i], color=colourMap[i*4])
        for i in range(2):
            axes[1].set_xlabel("Generation")
            axes[1].set_ylabel("Average Scalar Value")
            axes[1].plot(gensToPlot, popAverageScalars[i], color=colourMap[i*4])


        plt.show()
    def getColourMap(self):
        n=10
        name='hsv'
        cmap=plt.cm.get_cmap(name, n)
        colourArray = []
        for i in range(n):
            colourArray.append(cmap(i))
        return(colourArray)