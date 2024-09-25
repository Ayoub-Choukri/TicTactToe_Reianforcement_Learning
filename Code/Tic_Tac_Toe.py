import numpy as np
from time import sleep
import matplotlib.pyplot as plt
import tkinter as tk

class Tic_Tac_Toe :

    def __init__(self,Nb_Players = 2,Nb_Rows = 3,Nb_Cols = 3,Starter=1,Nb_Alignement=3):
        self.Nb_Players = Nb_Players
        self.Nb_Rows = Nb_Rows
        self.Nb_Cols = Nb_Cols
        self.Board = np.zeros((self.Nb_Rows,self.Nb_Cols))
        self.Markers = {1:'X',2:'O',0:' '}
        self.Current_Player = 0 # 0 means referee
        self.Winner = None
        self.Game_Over = False
        self.Game_Ongoing = False
        self.Draw = False
        self.Starter = Starter

        #Taille Minimale de la fenetre
        self.window = None
        self.Buttons = None
        self.window_size = 500,500

    # Fonction qui construit la première page d'accueil du jeu
    def Construct_First_Page(self): 
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.rowconfigure([0, 1, 2,3], minsize=50, weight=1)
        self.window.columnconfigure(0, minsize=50, weight=1)
        self.window.geometry("500x500")

        # Title
        self.Label_Title = tk.Label(master=self.window, text="Welcome to Tic Tac Toe !!!",bg='black',font=('Arial', 20),fg='white')
        self.Label_Title.grid(row=0, column=0, sticky="nsew")
        self.Button_Player_Vs_Player = tk.Button(master=self.window, text="Player Vs Player",bg='cyan',font=('Arial', 15),command=self.Game_Player_Vs_Player)
        self.Button_Player_Vs_Player.grid(row=1, column=0, sticky="nsew")

        self.Button_Player_Vs_Agent = tk.Button(master=self.window, text="Player Vs Agent",bg='cyan',font=('Arial', 15),command=self.Game_Player_Vs_Agent)
        self.Button_Player_Vs_Agent.grid(row=2, column=0, sticky="nsew")


        self.Button_Agent_vs_Player = tk.Button(master=self.window, text="Agent Vs Player",bg='cyan',font=('Arial', 15),command=self.Game_Agent_Vs_Player)
        self.Button_Agent_vs_Player.grid(row=3, column=0, sticky="nsew")


        self.window.mainloop()

            # Fonction qui construit la page de victoire
    def Construct_Winning_page(self):
        self.window.destroy()
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.rowconfigure([0, 1, 2], minsize=50, weight=1)
        self.window.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.window.geometry("500x500")

        self.Label_Title = tk.Label(master=self.window, text="Player {} wins".format(self.Winner),bg='black',font=('Arial', 20),fg='white')
        self.Label_Title.pack(fill='both',expand=True)

        #Button Replay
        self.Button_Replay = tk.Button(master=self.window, text="Replay",bg='cyan',font=('Arial', 15),command=self.Reset_Game_Tkinter)
        self.Button_Replay.pack(fill='both',expand=True)



        self.window.mainloop()

    def Construct_Draw_page(self):
        self.window.destroy()
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.rowconfigure([0, 1, 2], minsize=50, weight=1)
        self.window.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.window.geometry("500x500")

        self.Label_Title = tk.Label(master=self.window, text="Draw",bg='black',font=('Arial', 20),fg='white')
        self.Label_Title.pack(fill='both',expand=True)

        #Button Replay
        self.Button_Replay = tk.Button(master=self.window, text="Replay",bg='cyan',font=('Arial', 15),command=self.Reset_Game_Tkinter)
        self.Button_Replay.pack(fill='both',expand=True)

        

        self.window.mainloop()

    # Fonction qui construit la grille de jeu
    def Construct_Grille_Buttons_Tic_Tac_Toe(self):
        # Clear the window
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.rowconfigure([0, 1, 2], minsize=50, weight=1)
        self.window.columnconfigure([0, 1, 2], minsize=50, weight=1)
        self.window.geometry("500x500")

        self.Buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(master=self.window, text=" ",font=('Arial', 20),command=lambda i=i,j=j: self.On_Click(i,j),bg='cyan')
                button.grid(row=i, column=j, sticky="nsew")
                row.append(button)
            self.Buttons.append(row)




        
    def Put_Marker_Buttons(self,Row,Col,Player,color='black'):
        Marker_Put= False
        if self.Buttons[Row][Col]['text'] == ' ':
            self.Buttons[Row][Col]['text'] = 'X' if Player == 1 else 'O'
            self.Buttons[Row][Col]['fg'] = color
            self.Board[Row,Col] = self.Current_Player
            Marker_Put = True
        else:
            pass

        return Marker_Put
    



    def Agent_Play(self):
        Old_Player = self.Current_Player
        Action = self.Best_Policy[self.Board_State_To_Number(self.Board)]
        Row, Col = self.Number_To_Action(Action)
        self.Board[Row,Col] = self.Current_Player
        self.Put_Marker_Buttons(Row,Col,self.Current_Player,color='red')
        self.Scann_Referee()
        if self.Game_Over:
            if self.Winner == 1:
                print('Player 1 wins')
                self.Construct_Winning_page()
            elif self.Winner == 2:
                print('Player 2 wins')
                self.Construct_Winning_page()
            else:
                print('Draw')
                self.Construct_Draw_page()
        else:
            self.Current_Player = 3-Old_Player

    def On_Click(self,Row,Col):
        if self.Game_Ongoing:
            if self.Board[Row,Col] == 0:

                Old_Player = self.Current_Player
                self.Board[Row,Col] = self.Current_Player

                while not self.Put_Marker_Buttons(Row,Col,self.Current_Player):
                    pass


                self.Scann_Referee()
                if self.Game_Over:
                    if self.Winner == 1:
                        print('Player 1 wins')
                        self.Construct_Winning_page()
                    elif self.Winner == 2:
                        print('Player 2 wins')
                        self.Construct_Winning_page()
                    else:
                        print('Draw')
                        self.Construct_Draw_page()
                else:
                    self.Current_Player = 3-Old_Player


                if self.Agent_Plays and self.Game_Ongoing : 
                    self.Agent_Play()
            else:
                pass
        else:
            print('Game is over')
    

    def Load_Policy(self,Path):
        """
        This function loads the policy
        """
        self.Best_Policy = np.load(Path,allow_pickle=True)
        return self.Best_Policy
    

    def Game_Player_Vs_Player(self):
        self.Game_Ongoing = True
        self.Agent_Plays = False
        
        self.Current_Player = self.Starter  

        self.window.destroy()
        self.Construct_Grille_Buttons_Tic_Tac_Toe()


    def Game_Player_Vs_Agent(self):
        self.Agent_Starts = False
        self.Agent_Plays = True
        self.Load_Policy('./Policies/Policy_Iteration_Player_Starts.npy')

        self.Game_Ongoing = True
        self.Current_Player = self.Starter

        self.window.destroy()
        self.Construct_Grille_Buttons_Tic_Tac_Toe()


    def Game_Agent_Vs_Player(self):
        self.Agent_Starts = True
        self.Agent_Plays = True
        self.Load_Policy('./Policies/Policy_Iteration_Agent_Starts.npy')



        self.Current_Player = self.Starter
        self.Game_Ongoing = True

        self.window.destroy()
        self.Construct_Grille_Buttons_Tic_Tac_Toe()

        print('Agent Starts')
        self.Agent_Play()

        self.window.mainloop()














        


    def Display_board(self,Pause= True,Time=1):
        self.fig , self.ax = plt.subplots()
        self.ax.grid(True, linewidth=1, color='black')
        self.ax.set_xticks(np.arange(1, self.Nb_Cols, 1))
        self.ax.set_yticks(np.arange(1, self.Nb_Rows, 1))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        plt.xlim([0, self.Nb_Cols])
        plt.ylim([0, self.Nb_Rows])

        for i in range(self.Nb_Rows):
            for j in range(self.Nb_Cols):
                if self.Board[i,j] == 1:
                    Color = 'red'
                    self.ax.text(j+0.5, (2-i)+0.5, self.Markers[self.Board[i,j]], fontsize=20, ha='center', va='center', color=Color)
                elif self.Board[i,j] == 2:
                    Color = 'blue'
                    self.ax.text(j+0.5, (2-i)+0.5, self.Markers[self.Board[i,j]], fontsize=20, ha='center', va='center', color=Color)

        # show for 3 seconds

        if Pause:
            plt.pause(Time)
            plt.close()
        else:
            plt.show()

        return self.fig, self.ax



    def _Check_Winning_State_(self):
        if self.Current_Player !=0:
            assert False, "Referee cant check winning state"
        else:

            for i in range(1,3):
            # Vertical
                if np.all(self.Board[0,:] == i) or np.all(self.Board[1,:] == i) or np.all(self.Board[2,:] == i):
                    self.Winner = i
                    self.Game_Over = True
                    self.Game_Ongoing = False
                    break
                # Horizontal
                elif np.all(self.Board[:,0] == i) or np.all(self.Board[:,1] == i) or np.all(self.Board[:,2] == i):
                    self.Winner = i
                    self.Game_Over = True
                    self.Game_Ongoing = False
                    break
                # Diagonal
                elif np.all(np.diag(self.Board) == i) or np.all(np.diag(np.fliplr(self.Board)) == i):
                    self.Winner = i
                    self.Game_Over = True
                    break
                else:
                    self.Winner = None
                    self.Game_Over = False
                    self.Game_Ongoing = True

            return self.Winner!=None
    
            
    def _Check_Draw_(self):

        if self.Current_Player !=0:
            assert False, "Referee cant check draw"
        else:
            if np.all(self.Board != 0) and self.Winner == None:
                # Draw
                self.Game_Ongoing = False
                self.Game_Over = True
                self.Winner = None
                self.Draw = True
            return self.Draw



    def Scann_Referee(self):
        # this function will scan the board and check if there is a winner or a draw
        Current_Player = self.Current_Player
        self.Current_Player = 0

        self._Check_Winning_State_()

        self._Check_Draw_()


        # Giving back the turn to the player

        self.Current_Player = 3-Current_Player


        return self.Game_Over
    

    def Reset_Game_Tkinter(self):
        self.Board = np.zeros((self.Nb_Rows,self.Nb_Cols))
        self.Winner = None
        self.Game_Over = False
        self.Game_Ongoing = False
        self.Draw = False
        self.Current_Player = 0
        self.Start_Game()
        self.window.destroy()
        self.Construct_First_Page()

    def Reset_Game(self):
        self.Board = np.zeros((self.Nb_Rows,self.Nb_Cols))
        self.Winner = None
        self.Game_Over = False
        self.Game_Ongoing = False
        self.Draw = False
        self.Current_Player = 0
        self.Start_Game()



                            
    def Start_Game(self):
        self.Game_Ongoing = True
        self.Winner = None
        self.Game_Over = False
        self.Board = np.zeros((self.Nb_Rows,self.Nb_Cols))

    def Make_Move(self,Player,Row,Col):

        if self.Current_Player != Player:
            assert False, "Only referee can make a move"
        else:
            if self.Game_Ongoing:
                if self.Board[Row,Col] == 0:
                    self.Board[Row,Col] = Player
                else:
                    assert False, "Invalid move"
            else:
                print('Game is over')

    def Make_Move_KeyBoard(self,Player):
        if self.Current_Player != Player:
            assert False, "Only referee can make a move"
        else:
            if self.Game_Ongoing:
                Valid_Moove = False
                while not Valid_Moove:
                    print('Enter the row and column number like 1 1')
                    Row, Col = input().split()
                    Row = int(Row) - 1
                    Col = int(Col) - 1
                    if self.Board[Row,Col] == 0:
                        self.Board[Row,Col] = Player
                        Valid_Moove = True
                    else:
                        print('Invalid move')
            else:
                assert False, "Game is over"



    def Play_Game(self):
        self.Start_Game()
        while not self.Game_Over:
            # Starter
            self.Current_Player = self.Starter
            print('Player {} turn'.format(self.Current_Player))
            self.Make_Move_KeyBoard(self.Starter)
            self.Display_board()
            self.Scann_Referee()
            if self.Game_Over:
                print('Player {} wins'.format(self.Winner))
                break

            # Player 2
            self.Current_Player = 3-self.Starter
            print('Player {} turn'.format(self.Current_Player))
            self.Make_Move_KeyBoard(3-self.Starter)
            self.Display_board()
            self.Scann_Referee()
            if self.Game_Over:
                print('Player {} wins'.format(self.Winner))
                break


    
        print('Game Over')

    def Play_Game_Tkinter(self):
        self.Construct_First_Page()
        

    def Play_game_Player_Vs_Agent(self,Best_Policy,Starter="Agent"):
        self.Start_Game()

        while not self.Game_Over:
            # Starter
            self.Current_Player = self.Starter
            print('Player {} turn'.format(self.Current_Player))
            if Starter == "Agent":
                Action = Best_Policy[self.Board_State_To_Number(self.Board)]
                Row, Col = self.Number_To_Action(Action)
                self.Make_Move(self.Current_Player,Row,Col)
            else:
                self.Make_Move_KeyBoard(self.Starter)
            self.Display_board()
            self.Scann_Referee()
            if self.Game_Over:
                print('Player {} wins'.format(self.Winner))
                break

            # Player 2
            self.Current_Player = 3-self.Starter
            print('Player {} turn'.format(self.Current_Player))
            if Starter == "Agent":
                self.Make_Move_KeyBoard(3-self.Starter)
            else:
                Action = Best_Policy[self.Board_State_To_Number(self.Board)]
                Row, Col = self.Number_To_Action(Action)
                self.Make_Move(self.Current_Player,Row,Col)
            self.Display_board()
            self.Scann_Referee()
            if self.Game_Over:
                print('Player {} wins'.format(self.Winner))
                break


        print('Game Over')


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
    

    def Action_To_Number(self,Row,Col):
        return int(Row*3 + Col)
    
    def Number_To_Action(self,Number):
        Row = Number//3
        Col = Number%3
        return  int(Row), int(Col)






    























        
    





