from Policy_Iteration import *
from Tic_Tac_Toe import *
from Value_Iteration import *
from  Gym_Tic_Tac_Toe import *
import numpy as np




#p = Gym_Tic_Tac_Toe_Object.Available_Actions_Matrix[16493]
#print(p)
#Board = Gym_Tic_Tac_Toe_Object.Number_To_Board_State(2)
#print(Board)
#print(Gym_Tic_Tac_Toe_Object.Transition_Probability_Matrix[2][1])
#Board = Gym_Tic_Tac_Toe_Object.Number_To_Board_State(59)
#print(Board)
#print(Gym_Tic_Tac_Toe_Object._Scann_Referee(Board))
#print(Gym_Tic_Tac_Toe_Object.String_To_Board('O        '))
#print(Gym_Tic_Tac_Toe_Object.Board_State_To_Number(Gym_Tic_Tac_Toe_Object.String_To_Board('OXOXOXXXO')))
#print(Gym_Tic_Tac_Toe_Object.Board_State_To_Number(Gym_Tic_Tac_Toe_Object.String_To_Board('XOXOXOXO ')))

#Gym_Tic_Tac_Toe_Object.reset()
#Gym_Tic_Tac_Toe_Object.step(0)
#Gym_Tic_Tac_Toe_Object.render()
#Gym_Tic_Tac_Toe_Object.step(1)
#Gym_Tic_Tac_Toe_Object.render()
    

Train = 1


if Train : 
    # Agent_Starts 
    Gym_Tic_Tac_Toe_Object = Gym_Tic_Tac_Toe(Agent_Starts = 1)

    Policy_Iteration_Object = Policy_Iteration(Env=Gym_Tic_Tac_Toe_Object,Gamma=1,Theta=0.00001)

    #Value_Iteration_Object = Value_Iteration(Env=Gym_Tic_Tac_Toe_Object,Gamma=1,Theta=0.00001)

    V1,Policy1 = Policy_Iteration_Object.Policy_Iteration_Train(Verbose=True)

    Policy_Iteration_Object.Save_Policy(Path='./Policies/Policy_Iteration_Agent_Starts.npy')

    #V2,Policy2 = Value_Iteration_Object.Value_Iteration_Train(Verbose=True)

    #Value_Iteration_Object.Save_Policy(Path='./Policies/Value_Iteration_Agent_Starts.npy')

    # Player_Starts
    Gym_Tic_Tac_Toe_Object = Gym_Tic_Tac_Toe(Agent_Starts = 0)

    Policy_Iteration_Object = Policy_Iteration(Env=Gym_Tic_Tac_Toe_Object,Gamma=1,Theta=0.00001)

    #Value_Iteration_Object = Value_Iteration(Env=Gym_Tic_Tac_Toe_Object,Gamma=1,Theta=0.00001)

    V1,Policy1 = Policy_Iteration_Object.Policy_Iteration_Train(Verbose=True)

    Policy_Iteration_Object.Save_Policy(Path='./Policies/Policy_Iteration_Player_Starts.npy')

    #V2,Policy2 = Value_Iteration_Object.Value_Iteration_Train(Verbose=True)

    #Value_Iteration_Object.Save_Policy(Path='./Policies/Value_Iteration_Player_Starts.npy')








else:
    Policy = np.load('./Policies/Policy_Iteration_Agent_Starts.npy')

    Tic_Tac_Toe_Object = Tic_Tac_Toe()

    Tic_Tac_Toe_Object.Play_game_Player_Vs_Agent(Policy,Starter="Agent")
    
    
    