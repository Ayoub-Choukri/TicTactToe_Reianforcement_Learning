import numpy as np


class Value_Iteration():

        
    def __init__(self,Env,Gamma = 0.9,Theta = 0.0001):
        self.Env = Env
        self.Gamma = Gamma
        self.Theta = Theta
        self.V = np.zeros(3**9)


    def Compute_Sum_Policy_Evalutation(self,Env,V,State,Action,Gamma):
        """
        This function computes the sum of the transition probabilities times the expected value of the next state
        """
        Sum = 0
        Liste_Transition_Probability = Env.Transition_Probability_Matrix[State][Action]
        for Prob,Next_State,Reward,Done in Liste_Transition_Probability:
            Sum += Prob*(Reward + Gamma*V[Next_State])

        return Sum
    

    def Value_Iteration_Train(self,Verbose = False):
        """
        This function trains the agent using the value iteration algorithm
        """
        while True:
            Delta = 0
            for State in range(3**9):
                if self.Env.Matrix_States_End[State] == 0:
                    V_old = self.V[State]
                    Actions_Available = self.Env.Available_Actions_Matrix[State]
                    self.V[State] = max([self.Compute_Sum_Policy_Evalutation(Env=self.Env,V=self.V,State=State,Action=Action,Gamma=self.Gamma) for Action in range(9) if Actions_Available[Action] == 1])
                    Delta = max(Delta,abs(V_old - self.V[State]))
                else:
                    self.V[State] = 0
            if Delta < self.Theta:
                break

        if Verbose:
            print('Value Iteration Done')

            self.Policy = np.zeros(3**9)

            for State in range(3**9):
                if self.Env.Matrix_States_End[State] == 0:
                    Actions_Available = self.Env.Available_Actions_Matrix[State]
                    Max= -np.inf
                    Best_Action = None
                    for i in range(len(Actions_Available)):
                        
                        if Actions_Available[i] == 1:

                            Sum = self.Compute_Sum_Policy_Evalutation(Env=self.Env,V=self.V,State=State,Action=i,Gamma=self.Gamma)
                            
                            if Sum > Max:
                                Max = Sum
                                Best_Action = i

                    self.Policy[State] = Best_Action
                else:
                    self.Policy[State] = 0

        return self.V,self.Policy
    


    def Save_Policy(self,Path):
        """
        This function saves the policy
        """
        
        np.save(Path,self.Policy)



    def Load_Policy(self,Path):
        """
        This function loads the policy
        """
        self.Policy = np.load(Path)

        return self.Policy

