import numpy as np
class Policy_Iteration():
    
    def __init__(self,Env,Gamma = 0.9,Theta = 0.0001):
        self.Env = Env
        self.Gamma = Gamma
        self.Theta = Theta
        self.Policy = self.Init_Policy()
        self.V = np.zeros(3**9)

    
    def Init_Policy(self):
        '''
        This function initializes the policy by selecting a valid action randomly for each state
        '''
        self.Policy = np.zeros(3**9)
        for State in range(3**9):
            if self.Env.Matrix_States_End[State] == 0:
                Available_Actions = self.Env.Available_Actions_Matrix[State]
                self.Policy[State] = np.random.choice(np.where(Available_Actions == 1)[0])
            else:   
                pass
        
        return self.Policy
    def Compute_Sum_Policy_Evalutation(self,Env,V,State,Action,Gamma):
        """
        This function computes the sum of the transition probabilities times the expected value of the next state
        """
        Sum = 0
        Liste_Transition_Probability = Env.Transition_Probability_Matrix[State][Action]
        for Prob,Next_State,Reward,Done in Liste_Transition_Probability:
            Sum += Prob*(Reward + Gamma*V[Next_State])

        return Sum
    
    def Policy_Evalutation(self,Env,V,Policy,Gamma,Theta,Verbose = False):
        """
        This function evaluates the policy
        """

        while True:
            Delta = 0
            for State in range(3**9):
                if Env.Matrix_States_End[State] == 0:
                    V_old = V[State]
                    V[State] = self.Compute_Sum_Policy_Evalutation(Env=Env,V=V,State=State,Action=int(Policy[State]),Gamma=Gamma)
                    Delta = max(Delta,abs(V_old - V[State]))
                else:
                    V[State] = 0
            if Delta < Theta:
                break

        if Verbose:
            print('Policy Evaluation Done')

        return V,Policy

        
    def Policy_Improvement(self,Env,V,Policy,Gamma,Verbose = False):
        """
        This function improves the policy
        """
        Policy_Stable = True
        for State in range(3**9):
            if Env.Matrix_States_End[State] == 0:
                
                Old_Action = Policy[State]
                Available_Actions = Env.Available_Actions_Matrix[State]
                Max = -np.inf
                Best_Action = None
                for i in range(len(Available_Actions)):
                    Action = Available_Actions[i]
                    if Action == 1:
                        Sum = self.Compute_Sum_Policy_Evalutation(Env=Env,V=V,State=State,Action=i,Gamma=Gamma)
                        if Sum > Max:
                            Max = Sum
                            Best_Action = i
                Policy[State] = Best_Action
                if Old_Action != Policy[State]:
                    Policy_Stable = False
            else:
                Policy[State] = 0
            

        if Verbose:
            print('Policy Improvement Done')

        return V,Policy,Policy_Stable
    

    def Policy_Iteration_Train(self,Verbose = False):
        """
        This function performs the policy iteration
        """
        Policy_Stable = False
        print(self.Policy)
        while not Policy_Stable:
            self.V,self.Policy = self.Policy_Evalutation(Env=self.Env,V=self.V,Policy=self.Policy,Gamma=self.Gamma,Theta=self.Theta,Verbose=Verbose)
            self.V,self.Policy,Policy_Stable = self.Policy_Improvement(Env=self.Env,V=self.V,Policy=self.Policy,Gamma=self.Gamma,Verbose=Verbose)


        if Verbose:
            print('Policy Iteration Done')

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


