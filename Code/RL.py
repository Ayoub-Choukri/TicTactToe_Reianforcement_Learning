

import Tic_Tac_Toe 
import numpy as np


def Board_State_To_Number(board):
    """
    This function takes the board state and converts it to a number
    """
    Filtre = np.array([3**i for i in range(9)]).reshape(3,3)
    number = np.sum(board*Filtre)
    return number


#Tic_Tac_Toe_Obj = Tic_Tac_Toe.Tic_Tac_Toe(Starter=2)
#Tic_Tac_Toe_Obj.Start_Game()
#Tic_Tac_Toe_Obj.Current_Player = 2
#Tic_Tac_Toe_Obj.Make_Move(2,0,0)
#Tic_Tac_Toe_Obj.Display_board()
#Tic_Tac_Toe_Obj.Current_Player = 2
#Tic_Tac_Toe_Obj.Make_Move(2,0,1)
#print(Tic_Tac_Toe_Obj.Board)
#print(Board_State_To_Number(Tic_Tac_Toe_Obj.Board))

def Number_To_Board_State(number):
    """
    This function takes the number and converts it to a board state
    """
    Filtre = np.array([3**i for i in range(9)]).reshape(3,3)
    board = np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            board[i,j] = number%3
            number = (number - number%3) // 3
    return board


def Available_Actions():
    """
    This function intializes a Matrix of Nb_States x Nb_Actions and sets true for the possible actions
    """

    Result = np.zeros((3**9,9))

    for Nb_State in range(3**9):
        board = Number_To_Board_State(Nb_State)
        for i in range(3):
            for j in range(3):
                if board[i,j] == 0:
                    Result[Nb_State,i*3+j] = 1


    return Result


print(Available_Actions())