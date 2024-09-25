import numpy as np


class Gym_Tic_Tac_Toe():
    # Selon que l'agent commence ou non, il faut initialiser une classe ou l'autre pour entrainer l'agent
    def __init__(self,Agent_Starts=True):

        # Available Actions créer une matrice de 3**9 x 9 pour indiquer les actions possibles de chaque état
        #self.Available_Actions()

        self.Agent_Starts = Agent_Starts

        # self.player représente le symbole avec lequel l'agent joue
        if self.Agent_Starts:
            self.Player = 1
        else:
            self.Player = 2

        self.Random_Player = Random_player()

        # Récompenses
        self.Reward_Win = 10000
        self.Reward_Lose = -1000000
        self.Reward_Draw = -500
        self.Reward_Normal_Moove = -30

        # Cardinal de l'espace d'état et d'action
        self.Action_Space = 9
        self.Observation_Space = 3**9

        # Nombre de lignes, colonnes et alignements (Alignements = 3 pour le Tic Tac Toe normal)
        self.Nb_Rows = 3
        self.Nb_Cols = 3
        self.Nb_Alignement = 3

        # self.Available_Ations renvoie une matrice de 3**9 x 9 pour indiquer les actions possibles de chaque état
        self.Available_Actions_Matrix = self.Available_Actions()

        # self.Transition_Probability_Matrix renvoie la matrice de transition de l'environnement
        self.Transition_Probability_Matrix = self.Construct_Transition_probability_Matrix()

        # self.Matrix_Comming_From_Agent_Beginning renvoie une matrice de 3**9 x 1 pour indiquer les états terminaux 
        self.Matrix_States_End = self.Construct_Matrix_States_End()

    # Fonction pour convertir l'état du plateau en un nombre
    def Board_State_To_Number(self,board):
        """
        This function takes the board state and converts it to a number
        """
        Filtre = np.array([3**i for i in range(9)]).reshape(3,3)
        number = np.sum(board*Filtre)
        return int(number)
    

    # Fonction pour convertir un nombre en un état du plateau
    def Number_To_Board_State(self,number):
        """
        This function takes the number and converts it to a board state
        """
        board = np.zeros((3,3))
        for i in range(3):
            for j in range(3):
                board[i,j] = number%3
                number = (number - number%3) // 3
        return board     
    

    # Fonction pour convertir une action en un nombre
    def Action_To_Number(self,Row,Col):
        return Row*3 + Col
    
    def Number_To_Action(self,Number):
        Row = Number//3
        Col = Number%3
        return  Row, Col


    # Fonction pour construire la matrice des états terminaux
    def Construct_Matrix_States_End(self):
        """
        This function constructs the matrix of the end states
        """
        self.Matrix_States_End = np.zeros(3**9)
        for State in range(3**9):
            Board = self.Number_To_Board_State(State)
            Winner, Game_Over, Draw = self._Scann_Referee(Board)
            if Game_Over:
                self.Matrix_States_End[State] = 1
            else:
                self.Matrix_States_End[State] = 0

        return self.Matrix_States_End
    
    def reset(self):
        self.Board = np.zeros((self.Nb_Rows,self.Nb_Cols))
        self.Game_Over = False
        self.Draw = False
        self.Winner = None
        return self.Actual_State()



    def step(self,Action_Number):
        """
        This function takes the action number and returns the next state, reward, done, info
        """

        # Convert the action number to row and column
        Row , Col = self.Number_To_Action(Action_Number)

        #Check if the action is valid
        if self.Available_Actions_Matrix[self.Actual_State(),Action_Number] == 0:
            assert False, "Invalid action"
        else:

            # Make the move
            self.Make_Action(Row,Col,self.Player)



            #Make the Moove of the Opponent randomly
            Row , Col = self.Random_Player.Random_Move(self.Actual_State(),self.Available_Actions_Matrix)

            self.Make_Action(Row,Col,3-self.Player)

            # Check if the game is over
            self.Scann_Referee()

            # Check if the game is over

            if self.Game_Over:
                if self.Draw:
                    reward = self.Reward_Draw + self.Reward_Normal_Moove
                    done = True
                    info = 'Draw'
                elif self.Winner == self.Player:
                    reward = self.Reward_Win + self.Reward_Normal_Moove
                    done = True
                    info = 'Player 1 wins'
                elif self.Winner == 3-self.Player:
                    reward = self.Reward_Lose + self.Reward_Normal_Moove
                    done = True
                    info = 'Player 2 wins'
            else:
                reward = self.Reward_Normal_Moove
                done = False
                info = 'Game is ongoing'

            return self.Actual_State(), reward, done, info
        
    def render(self):
        self.Display_board(Pause=False,Time=0.1)

    
    def Display_board(self,Pause= True,Time=1):
        fig , ax = plt.subplots()
        ax.grid(True, linewidth=1, color='black')
        ax.set_xticks(np.arange(1, self.Nb_Cols, 1))
        ax.set_yticks(np.arange(1, self.Nb_Rows, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        plt.xlim([0, self.Nb_Cols])
        plt.ylim([0, self.Nb_Rows])

        for i in range(self.Nb_Rows):
            for j in range(self.Nb_Cols):
                if self.Board[i,j] == 1:
                    Color = 'red'
                    ax.text(j+0.5, (2-i)+0.5, 'X', fontsize=20, ha='center', va='center', color=Color)
                elif self.Board[i,j] == 2:
                    Color = 'blue'
                    ax.text(j+0.5, (2-i)+0.5, 'O', fontsize=20, ha='center', va='center', color=Color)

        # show for 3 seconds

        if Pause:
            plt.pause(Time)
            plt.close()
        else:
            plt.show()

        return fig, ax
    



    # Fonction pour préciser les actions possibles d'un état
    def Available_Actions(self):
        """
        This function intializes a Matrix of Nb_States x Nb_Actions and sets true for the possible actions
        """

        Result = np.zeros((3**9,9))

        for Nb_State in range(3**9):
            board = self.Number_To_Board_State(Nb_State)
            for i in range(3):
                for j in range(3):
                    if board[i,j] == 0:
                        Result[Nb_State,i*3+j] = 1


        self.Available_Actions_Matrix = Result

        return Result

    
        
    def Actual_State(self):
        return self.Board_State_To_Number(self.Board)
    

    def Make_Action(self, Row, Col, Player):
        self.Board[Row, Col] = Player

    def _Check_Winning_State(self,Board):

        for i in range(1,3):
        # Vertical
            if np.all(Board[0,:] == i) or np.all(Board[1,:] == i) or np.all(Board[2,:] == i):
                self.Winner = i
                self.Game_Over = True
                break
            # Horizontal
            elif np.all(Board[:,0] == i) or np.all(Board[:,1] == i) or np.all(Board[:,2] == i):
                self.Winner = i
                self.Game_Over = True
                break
            # Diagonal
            elif np.all(np.diag(Board) == i) or np.all(np.diag(np.fliplr(Board)) == i):
                self.Winner = i
                self.Game_Over = True
                break
            else:
                self.Winner = None
                self.Game_Over = False

        return self.Winner, self.Game_Over

    
    def _Check_Draw(self, Board, Winner):
        if np.all(Board != 0) and Winner == None:
            # Draw
            Game_Over = True
            Winner = None
            Draw = True
        else:
            Draw = False
            Game_Over = False
        return Draw, Game_Over
    
    def _Scann_Referee(self,Board):
        Winner , Game_Over = self._Check_Winning_State(Board)
        if not Game_Over:
            Draw ,Game_Over= self._Check_Draw(Board,Winner)
        else:
            Draw = False
        return Winner, Game_Over, Draw

    def Check_Winning_State(self):

        for i in range(1,3):
        # Vertical
            if np.all(self.Board[0,:] == i) or np.all(self.Board[1,:] == i) or np.all(self.Board[2,:] == i):
                self.Winner = i
                self.Game_Over = True
                break
            # Horizontal
            elif np.all(self.Board[:,0] == i) or np.all(self.Board[:,1] == i) or np.all(self.Board[:,2] == i):
                self.Winner = i
                self.Game_Over = True
                break
            # Diagonal
            elif np.all(np.diag(self.Board) == i) or np.all(np.diag(np.fliplr(self.Board)) == i):
                self.Winner = i
                self.Game_Over = True
                break
            else:
                self.Winner = None
                self.Game_Over = False




        return self.Winner, self.Game_Over

    def Check_Draw(self):
        if np.all(self.Board != 0) and self.Winner == None:
            # Draw
            self.Game_Over = True
            self.Winner = None
            self.Draw = True
        return self.Draw
    
    def Scann_Referee(self):
        self.Check_Winning_State()
        self.Check_Draw()
        return self.Game_Over
    
    def String_To_Board(self,String):
        Board = np.zeros((3,3))
        for i in range(3):
            for j in range(3):
                if String[i*3+j] == 'X':
                    Board[i,j] = 1
                elif String[i*3+j] == 'O':
                    Board[i,j] = 2
                else:
                    Board[i,j] = 0
        return Board

        
    def Transition_Probability(self,State_Number,Action_Number):
        """
        This function takes the state number and the action number and returns a list of tuples (Probabilty,Next_State,Reward,Done)
        """

        # Convert the action number to row and column
        Row , Col = self.Number_To_Action(Action_Number)
        
        Result= []
        #Check if the action is valid
        if self.Available_Actions_Matrix[State_Number,Action_Number] == 0:
            assert False, "Invalid action"
        else:
            Actual_Board = self.Number_To_Board_State(State_Number)

            Next_Board = Actual_Board.copy()

            # Make the move
            Next_Board[Row,Col] = self.Player

            # Determine the Current State
            Current_State = self.Board_State_To_Number(Next_Board)

            Winner, Game_Over, Draw = self._Scann_Referee(Next_Board)

            Actions_Available_Opponent = self.Available_Actions_Matrix[Current_State]
            N = len(Actions_Available_Opponent[Actions_Available_Opponent == 1])


            if N>0 and not Game_Over:
                for i in range(len(Actions_Available_Opponent)):
                    Action = Actions_Available_Opponent[i]

                    if Action == 1 :
                        New_Next_Bord = Next_Board.copy()
                        Row , Col = self.Number_To_Action(i)
                        New_Next_Bord[Row,Col] = 3-self.Player
                        Winner, Game_Over, Draw = self._Scann_Referee(New_Next_Bord)

                        if Game_Over:
                            if Draw:
                                Reward = self.Reward_Draw + self.Reward_Normal_Moove
                                Done = True
                            elif Winner == self.Player:
                                Reward = self.Reward_Win + self.Reward_Normal_Moove
                                Done = True
                            elif Winner == 3-self.Player:
                                Reward = self.Reward_Lose + self.Reward_Normal_Moove
                                Done = True

                        else:
                            Reward = self.Reward_Normal_Moove
                            Done = False

                        Next_State = self.Board_State_To_Number(New_Next_Bord)

                        Result.append((1/N,Next_State,Reward,Done))

                return Result
            else:
                if Draw:
                    return [(1,Current_State,self.Reward_Draw + self.Reward_Normal_Moove,True)]
                elif Winner == self.Player:
                    return [(1,Current_State,self.Reward_Win + self.Reward_Normal_Moove,True)]
                elif Winner == 3-self.Player:
                    return [(1,Current_State, self.Reward_Lose + self.Reward_Normal_Moove,True)]

        

    def Construct_Transition_probability_Matrix(self):
        """
        This function returns the transition probability matrix
        """

        Result = {}

        for State in range(3**9):
            Result[State] = {}
            Available_Actions = self.Available_Actions_Matrix[State]
            for i in range(len(Available_Actions)):
                Action = Available_Actions[i]
                if Action == 1:
                    Result[State][i] = self.Transition_Probability(int(State),int(i))
                else:
                    Result[State][i] = []
        
        self.Transition_Probability_Matrix = Result

        return Result


    def Display_board(self,Pause= True,Time=1):
        fig , ax = plt.subplots()
        ax.grid(True, linewidth=1, color='black')
        ax.set_xticks(np.arange(1, self.Nb_Cols, 1))
        ax.set_yticks(np.arange(1, self.Nb_Rows, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        plt.xlim([0, self.Nb_Cols])
        plt.ylim([0, self.Nb_Rows])

        for i in range(self.Nb_Rows):
            for j in range(self.Nb_Cols):
                if self.Board[i,j] == 1:
                    Color = 'red'
                    ax.text(j+0.5, (2-i)+0.5, 'X', fontsize=20, ha='center', va='center', color=Color)
                elif self.Board[i,j] == 2:
                    Color = 'blue'
                    ax.text(j+0.5, (2-i)+0.5, 'O', fontsize=20, ha='center', va='center', color=Color)

        # show for 3 seconds

        if Pause:
            plt.pause(Time)
            plt.close()
        else:
            plt.show()

        return fig, ax
    












class Random_player():

    def __init__(self):
        pass

    def Action_To_Number(self,Row,Col):
        return Row*3 + Col
    
    def Number_To_Action(self,Number):
        Row = Number//3
        Col = Number%3
        return  Row, Col


    def Board_State_To_Number(self,board):
        """
        This function takes the board state and converts it to a number
        """
        Filtre = np.array([3**i for i in range(9)]).reshape(3,3)
        number = np.sum(board*Filtre)
        return int(number)
    

    def Number_To_Board_State(self,number):
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
    
    def Random_Move(self,Number_State,Matrix_Available_Actions):
        """
        This function takes the number state and the available actions and returns a random action
        """
        print(Number_State)
        Action_Number = np.random.choice(np.where(Matrix_Available_Actions[Number_State] == 1)[0])
        Row , Col = self.Number_To_Action(Action_Number)
        return Row, Col
    


