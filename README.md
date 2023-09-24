# Tom-Clark-CS-BEng-Project

This project is the repository for my 3rd year University project - "Exploring Problems with Competitive Multi-Agent Self-Play Reinforcement Learning through a Minimal Substrate".
The project dissertation can be provided upon request.

This project takes a decentralised reinforcement learning approach to solve the competitive multi-agent Minimal Substrate environment.
3 experiments are made to see whether the issues of Loss of gradient, Focussing and Relativism appear when using Reinforcement Learning to solve this problem.

Here is a brief description of some of the files and folders in this repository:

-"Design_B.py" and "Design_C.py" is where the machine learning code is written. This contains a Reinforcement Learning representation of the Minimal Substrate problem, along with an Agent that learns within it. Design_A doesn't exist in this repository as I had already ruled it out during the design stage. All the machine learning code is hand written by myself with the exception of gym, which provided a useful discrete space class, and numpy for making an array of zeroes.

-"Generate Logs and Networks.py" sets up the environment and hyperparameters and initiates the learning. It also saves the networks and log files, these can be found in the "logs" and "nets" folder.

-"Generate Plots.py" loads the logs into the custom Logbook class that I've written, and represents the findings in graphs. You can see these in the "edited_plots" folder. These plots unfortunately lack the annotations that I made for them in my project dissertation.

-The "Experiment X snapshot" folders are snapshots of the code repository at the times when I performed the 3 different experiments. Experiment 1 for testing Loss of gradient, Experiment 2 for Focussing, and Experiment 3 for Relativism.
