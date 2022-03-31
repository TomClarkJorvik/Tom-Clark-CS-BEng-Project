from idna import InvalidCodepointContext
import matplotlib.pyplot as plt
import numpy as np

class logbook:
    def __init__(self):
        self.log = []
        self.gens = []
        self.inds = []
        self.rewards = []
        self.no_gens = 0
    def addEntry(self,entry):
        self.log.append(entry)
        self.gens.append(entry[0])
        if entry[0]>self.no_gens:
            self.no_gens=entry[0]
        self.inds.append(entry[1])
        self.rewards.append(entry[2])
    def printLogbook(self):
        for entry in self.log:
            print("Generation :",entry[0],"\n")
            print("Observation:{} Rewards:{}".format(entry[1],entry[2]))
    def saveLogbook(self,fileName):
        f=open(fileName,"w")
        for entry in self.log:
            toEnter=""
            toEnter+=str(entry[0])+";"
            for item in entry[1]:
                toEnter+="["+str(item[0])+","+str(item[1])+"]"
            toEnter+=";"
            for item in entry[2]:
                toEnter+=str(item)+","
            toEnter+=";\n"
            f.write(toEnter)

        f.close()
    def loadLogbook(self,fileName):
        f=open(fileName,"r")
        self.log = []
        for line in f.readlines():
            entry = []
            start = 0
            count = 0
            flag = True
            while flag:
                if line[count] == ";":
                    flag = False
                    toAppend=int(line[start:count])
                    entry.append(toAppend)
                    self.gens.append(toAppend)
                    if toAppend>self.no_gens:
                        self.no_gens = toAppend
                count+=1
            flag=True
            inds=[]
            while flag:
                if line[count] == "[":
                    indxStart=count+1
                elif line[count]==",":
                    indxEnd=count
                elif line[count]=="]":
                    indx=line[indxStart:indxEnd]
                    indy=line[indxEnd+1:count]
                    inds.append([int(indx),int(indy)])
                elif line[count]==";":
                    flag=False
                    entry.append(inds)
                    self.inds.append(inds)
                count+=1
            flag = True
            rewards=[]
            start = count
            while flag:
                if line[count] == ",":
                    rewards.append(int(line[start:count]))
                    start = count+1
                elif line[count]==";":
                    flag=False
                    entry.append(rewards)
                    self.rewards.append(rewards)
                    
                count+=1
                            
            self.log.append(entry)
        f.close()
    def plotRewards(self):
        
        # I want to plot generation vs rewards
        # and generation vs inds
        rewards = np.array(self.rewards)
        no_individuals = len(rewards[0])
        no_gens = self.no_gens+1
        no_iterations = int(len(rewards)/no_gens)

        fig, ax1 = plt.subplots()
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Rewards")
        gensToPlot = [i for i in range(no_gens)]

        for i in range(no_individuals):
            indsRewards=rewards[:,i]
            self.plotIndividualRewards(indsRewards,no_gens,no_iterations,ax1,gensToPlot,i)

        plt.show()

    def plotInds(self):
        
        # I want to plot generation vs rewards
        # and generation vs inds
        individuals = np.array(self.inds)
        no_individuals = len(individuals[0])
        no_gens = self.no_gens+1
        no_iterations = int(len(individuals)/no_gens)

        fig, ax1 = plt.subplots()
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Rewards")
        gensToPlot = [i for i in range(no_gens)]

        for i in range(no_individuals):
            indsDims=individuals[:,i]
            self.plotIndividualDimensions(indsDims,no_gens,no_iterations,ax1,gensToPlot,i)

        plt.show()

    def plotIndividualRewards(self,indsRewards,no_gens,no_iterations,ax1,gensToPlot,individual):
        totIndsRewards=[0 for z in range(no_gens)]

        for x in range(no_gens*no_iterations):
            index=x%no_gens
            totIndsRewards[index]+=indsRewards[x]
        for z in range(no_gens):
            totIndsRewards[z] = totIndsRewards[z]/no_iterations
        label = "Rewards:Ind {}".format(individual)
        ax1.plot(gensToPlot, totIndsRewards, label=label)
    
    def plotIndividualDimensions(self,inds,no_gens,no_iterations,ax1,gensToPlot,individual):
        totInds=[[0,0] for z in range(no_gens)]
            
        for x in range(no_gens*no_iterations):
            index=x%no_gens
            for y in range(0,2):
                
                totInds[index][y]+=inds[x][y]
        for z in range(no_gens):
            for y in range(0,2):
                totInds[z][y] = totInds[z][y]/no_iterations
        label = "Dimensions:Ind {}".format(individual)
        ax1.plot(gensToPlot, totInds, label = label)
    def plotIndividual(self,individual):
        individuals = np.array(self.inds)
        rewards = np.array(self.rewards)
        no_gens = self.no_gens+1
        no_iterations = int(len(individuals)/no_gens)

        fig, ax1 = plt.subplots()
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Rewards")
        gensToPlot = [i for i in range(no_gens)]
        
        indsDims=individuals[:,individual]
        indsRewards=rewards[:,individual]
        self.plotIndividualRewards(indsRewards,no_gens,no_iterations,ax1,gensToPlot,individual)
        self.plotIndividualDimensions(indsDims,no_gens,no_iterations,ax1,gensToPlot,individual)
        plt.show()


    def plotLogbook(self):
        self.plotInds()
        self.plotRewards()
        