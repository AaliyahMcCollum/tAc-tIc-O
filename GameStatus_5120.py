# -*- coding: utf-8 -*-


class GameStatus:


        def __init__(self, board_state, turn_O):

                self.board_state = board_state
                self.turn_O = turn_O
                self.oldScores = 0

                self.winner = ""


        def is_terminal(self):
        
                #returns winner 
                for row in self.board_state:
                        if 0 in row:
                                return False
                return True
        
        def get_scores(self, terminal):
        
                rows = len(self.board_state)
                cols = len(self.board_state[0])
                scores = 0
                check_point = 3 if terminal else 2
                print(check_point)
                # Check horizontally
                for row in range(rows):
                        for col in range(cols - 2):
                            if sum(self.board_state[row][col:col + 3]) >= abs(check_point):
                                scores += 1
                            elif sum(self.board_state[row][col:col + 3]) <= -abs(check_point):
                                scores += -1
        
                # Check vertically
                for col in range(cols):
                    for row in range(rows - 2):
                        if sum(self.board_state[row][col] for row in range(row, row + 3)) >= abs(check_point):
                            scores += 1
                        elif sum(self.board_state[row][col] for row in range(row, row + 3)) <= -abs(check_point):
                            scores += -1
        
                # Check diagonally (top-left to bottom-right)
                for row in range(rows - 2):
                    for col in range(cols - 2):
                        if sum(self.board_state[row + i][col + i] for i in range(3)) >= abs(check_point):
                            scores += 1
                        elif sum(self.board_state[row + i][col + i] for i in range(3)) <= -abs(check_point):
                            scores += -1
        
                # Check diagonally (top-right to bottom-left)
                for row in range(rows - 2):
                    for col in range(2, cols):
                        if sum(self.board_state[row + i][col - i] for i in range(3)) >= abs(check_point):
                            scores += 1
                        elif sum(self.board_state[row + i][col - i] for i in range(3)) <= -abs(check_point):
                            scores += -1
        
                if not scores == self.oldScores:
                    self.oldScores = scores
                if not scores == 0:
                    return scores
                is_there_free_cell = False
                for x in range(len(self.board_state)):
                    for y in range(len(self.board_state[0])):
                        if self.board_state[x, y] == 0:
                            is_there_free_cell = True
                if (is_there_free_cell == False):
                    return scores
                else:
                    return 0
        

        def get_negamax_scores(self, terminal):
        
                
                winner= []
                rows= []
                cols=[]
                rows = len(self.board_state)
                cols = len(self.board_state[0])
                scores = 0
                check_point = 3 if terminal else 2
        
        
        
                for i in range(3): #adding up horizontal(rows)
                        winner.append(rows[i][0]+ rows[i][1]+ rows[i][2])
    
                for i in range(3): #adding up vertical(columns)
                        winner.append(cols[0][i]+ cols[1][i]+ cols[2][i])
        
                #adding up diagonals
                winner.append(self.board_state[0][0]+ self.board_state[1][1]+ self.board_state[2][2])
                winner.append(self.board_state[0][2]+ self.board_state[1][1]+ self.board_state[2][0])
            
                if check_point in winner:
                        terminal= True
                        return 1 #Human Wins
                elif -3 in winner:
                        terminal= True
                        return -1 #AI Wins
                else:
                        return scores # Both Tie
 
  
        def get_moves(self):
                moves = []
                #adding up the non empty cells 
                for i in range(len(self.board_state)):
                        for j in range(len(self.board_state[i])):
                                if self.board_state[i][j] == 0:
                                        moves.append((i,j))
                    
   
                return moves
    


        def get_new_state(self, move):
                new_board_state = self.board_state.copy()
                x, y = move[0], move[1]
                new_board_state[x,y] = 1 if self.turn_O else -1
                return GameStatus(new_board_state, not self.turn_O)
