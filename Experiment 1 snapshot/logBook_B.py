import matplotlib.pyplot as plt
import numpy as np
import os
#This construct is simply for saving and loading log entries, and displaying graphs
class logbook:
    def __init__(self,equation,maxScalarValue=100):
        self.log = []
        self.gens = []
        self.inds = []
        self.equation = equation
        self.rewards = []
        self.no_gens = 0
        self.no_plots_per_graph = 3
        self.directory = "./logs/"
        self.rewardLabel = "Subjective Fit."
        #self.scalarLabel = "Scalar Values"
        self.scalarLabel = "Objective Fit."
        self.maxScalarValue = maxScalarValue
    def addEntry(self,entry):
        
        self.log.append(entry)
        self.gens.append(entry[0])
        if entry[0]>self.no_gens:
            self.no_gens=entry[0]
        self.inds.append(entry[1])
        self.rewards.append(entry[2])
        self.no_dims = len(entry[1][0])

    def printLogbook(self):
        for entry in self.log:
            print("Generation :",entry[0],"\n")
            print("Observation:{} Rewards:{}".format(entry[1],entry[2]))
            
    def saveLogbook(self,fileName):
        file_path = os.path.join(self.directory, fileName)
        f=open(file_path,"w")
        f.write(str(self.equation)+"\n")
        f.write(str(self.no_dims)+"\n")
        for entry in self.log:
            toEnter=""
            toEnter+=str(entry[0])+";"
            if self.no_dims == 1:
                for item in entry[1]:
                    toEnter+="["+str(item[0])+"]"
            else:
                
                for item in entry[1]:
                    toEnter+="["
                    for dim in range(self.no_dims):
                        toEnter+=str(item[dim])+","
                    toEnter = toEnter[:-1]
                    toEnter+="]"
            toEnter+=";"
            for item in entry[2]:
                toEnter+=str(item)+","
            toEnter+=";\n"
            f.write(toEnter)
        f.close()
    def loadLogbook(self,fileName):
        file_path = os.path.join(self.directory, fileName)
        f=open(file_path,"r")
        self.log = []
        lines = f.readlines()
        self.equation = int(lines[0].rstrip('\n'))
        self.no_dims = int(lines[1].rstrip('\n'))
        for i in range(2,len(lines)):
            line = lines[i]
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
            if self.no_dims == 1:
                while flag:
                    if line[count] == "[":
                        indxStart=count+1
                    elif line[count]=="]":
                        indx=line[indxStart:count]
                        inds.append([int(indx)])
                    elif line[count]==";":
                        flag=False
                        entry.append(inds)
                        self.inds.append(inds)
                    count+=1
            else:
                while flag:
                    if line[count] == "[":
                        dims = []
                        indStart=count+1
                    elif line[count]==",":
                        dims.append(int(line[indStart:count]))
                        indStart = count+1
                        
                    elif line[count]=="]":
                        dims.append(int(line[indStart:count]))
                        inds.append(dims)
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

    def plotIndividualRewards(self,indsRewards,no_gens,no_iterations,ax1,gensToPlot,individual,colour):
        totIndsRewards=[0 for z in range(no_gens)]

        for x in range(no_gens*no_iterations):
            index=x%no_gens
            totIndsRewards[index]+=indsRewards[x]
        for z in range(no_gens):
            totIndsRewards[z] = totIndsRewards[z]/no_iterations
        label = "Rewards:Ind {}".format(individual)
        ax1.plot(gensToPlot, totIndsRewards, label=label,color=colour)
    
    def plotIndividualDimensions(self,inds,no_gens,no_iterations,ax1,gensToPlot,individual,colour):
        
        totInds=[[0 for i in range(self.no_dims)] for z in range(no_gens)]
        for x in range(no_gens*no_iterations):
            index=x%no_gens
            for y in range(0,self.no_dims):
                totInds[index][y]+=inds[x][y]
                
        for z in range(no_gens):
            for y in range(0,self.no_dims):
                totInds[z][y] = totInds[z][y]/no_iterations
        label = "Dimensions:Ind {}".format(individual)
        ax1.plot(gensToPlot, totInds, label = label,color=colour)

    def plotIndividual(self,individual):
        individuals = np.array(self.inds)
        rewards = np.array(self.rewards)
        no_gens = self.no_gens+1
        no_iterations = int(len(individuals)/no_gens)

        fig, ax1 = plt.subplots()
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Rewards/Scalar Value")
        gensToPlot = [i for i in range(no_gens)]
        colourMap = self.getColourMap(10)
        indsDims=individuals[:,individual]
        indsRewards=rewards[:,individual]
        self.plotIndividualRewards(indsRewards,no_gens,no_iterations,ax1,gensToPlot,individual,colourMap[0])
        self.plotIndividualDimensions(indsDims,no_gens,no_iterations,ax1,gensToPlot,individual,colourMap[9])
        leg = plt.legend(loc="upper left")
        plt.show()


    def plotLogbook(self):
        rewards = np.array(self.rewards)
        no_individuals = len(rewards[0])
        no_gens = self.no_gens+1
        no_iterations = int(len(rewards)/no_gens)
        colourMap = self.getColourMap(no_individuals)
        
        
        #Rewards
        fig, axes = plt.subplots(4, 5, constrained_layout=True)
        currentAxRow=0
        currentAxCol=0
        axes[currentAxRow][currentAxCol].set_xlabel("Generation")
        axes[currentAxRow][currentAxCol].set_ylabel(self.rewardLabel)
        gensToPlot = [i for i in range(no_gens)]
        for i in range(no_individuals):
            indsRewards=rewards[:,i]
            self.plotIndividualRewards(indsRewards,no_gens,no_iterations,axes[currentAxRow][currentAxCol],gensToPlot,i,colourMap[i])

            if i%self.no_plots_per_graph==self.no_plots_per_graph-1 and i!=no_individuals-1:
                if currentAxCol == 4:
                    currentAxCol = 0
                    currentAxRow = 2
                else:
                    currentAxCol+=1
                axes[currentAxRow][currentAxCol].set_xlabel("Generation")
                axes[currentAxRow][currentAxCol].set_ylabel(self.rewardLabel)

        #Dimensions
        individuals = np.array(self.inds)
        currentAxCol=0
        currentAxRow=1

        axes[currentAxRow][currentAxCol].set_xlabel("Generation")
        axes[currentAxRow][currentAxCol].set_ylabel(self.scalarLabel)
        axes[currentAxRow][currentAxCol].set_ylim([0, self.maxScalarValue])

        for i in range(no_individuals):
            indsDims=individuals[:,i]
            self.plotIndividualDimensions(indsDims,no_gens,no_iterations,axes[currentAxRow][currentAxCol],gensToPlot,i,colourMap[i])
            if i%self.no_plots_per_graph==self.no_plots_per_graph-1 and i!=no_individuals-1:
                if currentAxCol == 4:
                    currentAxCol = 0
                    currentAxRow = 3
                else:
                    currentAxCol+=1           
                axes[currentAxRow][currentAxCol].set_xlabel("Generation")
                axes[currentAxRow][currentAxCol].set_ylabel(self.scalarLabel)
                axes[currentAxRow][currentAxCol].set_ylim([0, self.maxScalarValue])

        plt.show()
    
    def plotLogbook_only2inds(self):
        #only difference is that the colours are set to be different.
        rewards = np.array(self.rewards)
        no_individuals = len(rewards[0])
        no_gens = self.no_gens+1
        no_iterations = int(len(rewards)/no_gens)
        colourMap = self.getColourMap_2_inds()
        
        #Rewards
        fig, axes = plt.subplots(2, 1, constrained_layout=True)
        currentAxRow=0
        axes[currentAxRow].set_xlabel("Generation")
        axes[currentAxRow].set_ylabel(self.rewardLabel)
        gensToPlot = [i for i in range(no_gens)]
        for i in range(no_individuals):
            indsRewards=rewards[:,i]
            self.plotIndividualRewards(indsRewards,no_gens,no_iterations,axes[currentAxRow],gensToPlot,i,colourMap[i*4])

            if i%self.no_plots_per_graph==self.no_plots_per_graph-1 and i!=no_individuals-1:
                axes[currentAxRow].set_xlabel("Generation")
                axes[currentAxRow].set_ylabel(self.rewardLabel)

        #Dimensions
        individuals = np.array(self.inds)
        currentAxRow+=1

        axes[currentAxRow].set_xlabel("Generation")
        axes[currentAxRow].set_ylabel(self.scalarLabel)
        axes[currentAxRow].set_ylim([0, self.maxScalarValue])
        for i in range(no_individuals):
            indsDims=individuals[:,i]
            self.plotIndividualDimensions(indsDims,no_gens,no_iterations,axes[currentAxRow],gensToPlot,i,colourMap[i*4])
            if i%self.no_plots_per_graph==self.no_plots_per_graph-1 and i!=no_individuals-1:          
                axes[currentAxRow].set_xlabel("Generation")
                axes[currentAxRow].set_ylabel(self.scalarLabel)
                axes[currentAxRow].set_ylim([0, self.maxScalarValue])

        plt.show()
    def plotLogbook_2inds_one_iteration(self,iteration):
        
        rewards = np.array(self.rewards)
        no_individuals = len(rewards[0])
        no_gens = self.no_gens+1
        no_iterations = int(len(rewards)/no_gens)
        colourMap = self.getColourMap_2_inds()
        
        #Rewards
        fig, axes = plt.subplots(2, 1, constrained_layout=True)
        currentAxRow=0
        axes[currentAxRow].set_xlabel("Generation")
        axes[currentAxRow].set_ylabel(self.rewardLabel)
        gensToPlot = [i for i in range(no_gens)]
        for i in range(no_individuals):
            indsRewards=rewards[:,i]
            self.plotIndividualRewards_one_iteration(indsRewards,no_gens,no_iterations,axes[currentAxRow],gensToPlot,i,colourMap[i*4],iteration)

            if i%self.no_plots_per_graph==self.no_plots_per_graph-1 and i!=no_individuals-1:
                axes[currentAxRow].set_xlabel("Generation")
                axes[currentAxRow].set_ylabel(self.rewardLabel)

        #Dimensions
        individuals = np.array(self.inds)
        currentAxRow+=1

        axes[currentAxRow].set_xlabel("Generation")
        axes[currentAxRow].set_ylabel(self.scalarLabel)
        axes[currentAxRow].set_ylim([0, self.maxScalarValue])
        for i in range(no_individuals):
            indsDims=individuals[:,i]
            self.plotIndividualDimensions_one_iteration(indsDims,no_gens,no_iterations,axes[currentAxRow],gensToPlot,i,colourMap[i*4],iteration)
            if i%self.no_plots_per_graph==self.no_plots_per_graph-1 and i!=no_individuals-1:          
                axes[currentAxRow].set_xlabel("Generation")
                axes[currentAxRow].set_ylabel(self.scalarLabel)
                axes[currentAxRow].set_ylim([0, self.maxScalarValue])

        plt.show()
    def plotIndividualRewards_one_iteration(self,indsRewards,no_gens,no_iterations,ax1,gensToPlot,individual,colour,iteration_to_plot):
        totIndsRewards=[0 for z in range(no_gens)]
        for x in range(no_gens*no_iterations):
            if x>= iteration_to_plot*no_gens and x<=(iteration_to_plot*no_gens+99):
                index=x%no_gens
                totIndsRewards[index]+=indsRewards[x]
            
        label = "Rewards:Ind {}".format(individual)
        ax1.plot(gensToPlot, totIndsRewards, label=label,color=colour)
    
    def plotIndividualDimensions_one_iteration(self,inds,no_gens,no_iterations,ax1,gensToPlot,individual,colour,iteration_to_plot):
        
        totInds=[[0 for i in range(self.no_dims)] for z in range(no_gens)]
        for x in range(no_gens*no_iterations):
            
            if x>= iteration_to_plot*no_gens and x<=(iteration_to_plot*no_gens+99):
                index=x%no_gens
                for y in range(0,self.no_dims):
                    totInds[index][y]+=inds[x][y]
        label = "Dimensions:Ind {}".format(individual)
        ax1.plot(gensToPlot, totInds, label = label,color=colour)

    def plot_one_iteration(self,iteration):
        rewards = np.array(self.rewards)
        no_individuals = len(rewards[0])
        no_gens = self.no_gens+1
        no_iterations = int(len(rewards)/no_gens)
        colourMap = self.getColourMap(no_individuals)
        
        #Rewards
        fig, axes = plt.subplots(4, 5, constrained_layout=True)
        currentAxRow=0
        currentAxCol=0
        axes[currentAxRow][currentAxCol].set_xlabel("Generation")
        axes[currentAxRow][currentAxCol].set_ylabel(self.rewardLabel)
        gensToPlot = [i for i in range(no_gens)]
        for i in range(no_individuals):
            indsRewards=rewards[:,i]
            self.plotIndividualRewards_one_iteration(indsRewards,no_gens,no_iterations,axes[currentAxRow][currentAxCol],gensToPlot,i,colourMap[i],iteration)

            if i%self.no_plots_per_graph==self.no_plots_per_graph-1 and i!=no_individuals-1:
                if currentAxCol == 4:
                    currentAxCol = 0
                    currentAxRow = 2
                else:
                    currentAxCol+=1
                axes[currentAxRow][currentAxCol].set_xlabel("Generation")
                axes[currentAxRow][currentAxCol].set_ylabel(self.rewardLabel)

        #Dimensions
        individuals = np.array(self.inds)
        currentAxCol=0
        currentAxRow=1

        axes[currentAxRow][currentAxCol].set_xlabel("Generation")
        axes[currentAxRow][currentAxCol].set_ylabel(self.scalarLabel)
        axes[currentAxRow][currentAxCol].set_ylim([0, self.maxScalarValue])

        for i in range(no_individuals):
            indsDims=individuals[:,i]
            self.plotIndividualDimensions_one_iteration(indsDims,no_gens,no_iterations,axes[currentAxRow][currentAxCol],gensToPlot,i,colourMap[i],iteration)
            if i%self.no_plots_per_graph==self.no_plots_per_graph-1 and i!=no_individuals-1:
                if currentAxCol == 4:
                    currentAxCol = 0
                    currentAxRow = 3
                else:
                    currentAxCol+=1           
                axes[currentAxRow][currentAxCol].set_xlabel("Generation")
                axes[currentAxRow][currentAxCol].set_ylabel(self.scalarLabel)
                axes[currentAxRow][currentAxCol].set_ylim([0, self.maxScalarValue])

        plt.show()

    def plotIndividualObjFitness(self,inds,no_gens,no_iterations,ax1,gensToPlot,individual,colour):
        
        totInds=[0 for z in range(no_gens)]
        
        for x in range(no_gens*no_iterations):
            index=x%no_gens
            for y in range(0,self.no_dims):
                totInds[index]+=inds[x][y]
        for i in range(no_gens):
            totInds[i] = totInds[i]/no_iterations
            
        label = "Dimensions:Ind {}".format(individual)
        ax1.plot(gensToPlot, totInds, label = label,color=colour)

    def plot_obj_fitness_and_rewards(self):
        rewards = np.array(self.rewards)
        no_individuals = len(rewards[0])
        no_gens = self.no_gens+1
        no_iterations = int(len(rewards)/no_gens)
        colourMap = self.getColourMap(no_individuals)
        
        #Rewards
        fig, axes = plt.subplots(4, 5, constrained_layout=True)
        currentAxRow=0
        currentAxCol=0
        axes[currentAxRow][currentAxCol].set_xlabel("Generation")
        axes[currentAxRow][currentAxCol].set_ylabel(self.rewardLabel)
        gensToPlot = [i for i in range(no_gens)]

        
        for i in range(no_individuals):
            indsRewards=rewards[:,i]
            self.plotIndividualRewards(indsRewards,no_gens,no_iterations,axes[currentAxRow][currentAxCol],gensToPlot,i,colourMap[i])

            if i%self.no_plots_per_graph==self.no_plots_per_graph-1 and i!=no_individuals-1:
                if currentAxCol == 4:
                    currentAxCol = 0
                    currentAxRow = 2
                else:
                    currentAxCol+=1
                axes[currentAxRow][currentAxCol].set_xlabel("Generation")
                axes[currentAxRow][currentAxCol].set_ylabel(self.rewardLabel)

        #Dimensions
        individuals = np.array(self.inds)
        currentAxCol=0
        currentAxRow=1

        maxObjValue = self.maxScalarValue*self.no_dims
        axes[currentAxRow][currentAxCol].set_xlabel("Generation")
        axes[currentAxRow][currentAxCol].set_ylabel("Objective Fit.")
        axes[currentAxRow][currentAxCol].set_ylim([0, maxObjValue])

        for i in range(no_individuals):
            indsDims=individuals[:,i]
            
            self.plotIndividualObjFitness(indsDims,no_gens,no_iterations,axes[currentAxRow][currentAxCol],gensToPlot,i,colourMap[i])
            if i%self.no_plots_per_graph==self.no_plots_per_graph-1 and i!=no_individuals-1:
                if currentAxCol == 4:
                    currentAxCol = 0
                    currentAxRow = 3
                else:
                    currentAxCol+=1           
                axes[currentAxRow][currentAxCol].set_xlabel("Generation")
                axes[currentAxRow][currentAxCol].set_ylabel("Objective Fit.")
                axes[currentAxRow][currentAxCol].set_ylim([0, maxObjValue])

        plt.show()
    

    def getColourMap(self, n):
        n=25 # only works for 25 indiviudals at the moment
        name='hsv'
        cmap=plt.cm.get_cmap(name, n)
        colourArray = []
        tempArray = [[] for i in range(5)]
        

        for i in range(n):
            tempArray[i%5].append(cmap(i))
        for col in tempArray:
            for colour in col:
                colourArray.append(colour)
        return(colourArray)
    def getColourMap_2_inds(self):
        name='hsv'
        cmap=plt.cm.get_cmap(name, 10)
        colourArray = []
        for i in range(10):
            colourArray.append(cmap(i))
        return(colourArray)

