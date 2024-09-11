
import pygame
import numpy as np

from GameStatus_5120 import GameStatus
from multiAgents import minimax, negamax
import sys, random
#BUTTON CLASS
class Button:
    def __init__(self, rect, color, text, text_color, font, action=None):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font
        self.action = action
        
        

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = self.font
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()
#RADIO BUTTONS
class Radio:
    def __init__(self, options, rect, color, text_color=(255, 255, 255), action=None):
        self.options = options
        self.rect = pygame.Rect(rect)
        self.color = color
        self.text_color = text_color
        self.action = action
        self.selected_option = None
        self.dropdown_open = False

        self.dropdown_rect = pygame.Rect(rect.left, rect.top, rect.width, rect.height * len(options))
        self.radio_buttons = []
        self.create_radio_buttons()

    def create_radio_buttons(self):
        y_offset = self.rect.top
        for option in self.options:
            button_rect = pygame.Rect(self.rect.left, y_offset, self.rect.width, self.rect.height)
            button = RadioButton(option, button_rect, self.text_color, self.set_selected_option)
            self.radio_buttons.append(button)
            y_offset += self.rect.height

    def set_selected_option(self, option):
        self.selected_option = option
        if self.action:
            self.action(option)

    def toggle_dropdown(self):
        self.dropdown_open = not self.dropdown_open

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)

        # Draw selected option
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.selected_option, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery))
        screen.blit(text_surface, text_rect)

        # Draw dropdown menu if open
        if self.dropdown_open:
            pygame.draw.rect(screen, self.color, self.dropdown_rect)
            for button in self.radio_buttons:
                button.draw(screen, self.selected_option)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.toggle_dropdown()
        if self.dropdown_open:
            for button in self.radio_buttons:
                button.handle_event(event)


class RadioButton:
    def __init__(self, text, rect, text_color, action=None):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.text_color = text_color
        self.action = action

    def draw(self, screen, selected_option):
        if selected_option == self.text:
            pygame.draw.rect(screen, (150, 150, 150), self.rect, 0)
        else:
            pygame.draw.rect(screen, (200, 200, 200), self.rect, 0)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)
        font = pygame.font.Font(None, 20)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action(self.text)





#GAME CLASS
class RandomBoardTicTacToe:
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pygame Buttons")
        # Define some colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (35,58,72)
        self.FOREST = (67,110,103)
        self.TEAL = (108,149,133)
        self.MINT = (190,208,143)
        self.BEIGE = (229,227,206)
        self.LineWidth = (5)
        self.board = np.zeros((3,3))
        #temporary placement of options
        self.bt = "3 x 3"
        self.human = "x"
        self.mode = "Human v AI"
       
        self.game_state = GameStatus(self.board,True)
        #Define Fonts
        self.font = pygame.font.Font('freesansbold.ttf', 25)
        self.font2 = pygame.font.Font('freesansbold.ttf', 50)
        self.font3 = pygame.font.Font('freesansbold.ttf', 20)
        self.font4 = pygame.font.Font('freesansbold.ttf', 15)

        #BUTTONS
        self.start = Button((180, 150, 100, 40), self.TEAL, "START", self.WHITE, self. font3, self.button1_action)
        self.restart = Button((480,520,90,40), self.TEAL, "RESET", self.WHITE, self.font3, self.button2_action)
        self.buttons = [self.start,self.restart]

        #RADIO BUTTONS
        # Initialize Radio objects with different options and actions
        self.radio_options_1 = ["Human v AI", "Human v Human"]
        self.radio_rect_1 = pygame.Rect(160, 17, 140, 30)
        self.radio_color = self.BEIGE
        self.radio_text_color = self.TEAL
        self.radio_action_1 = self.radio_action_callback_1
        self.radio_1 = Radio(self.radio_options_1, self.radio_rect_1, self.radio_color, self.radio_text_color, self.radio_action_1)

        self.radio_options_2 = ["3 x 3", "4 x 4", "5 x 5"]
        self.radio_rect_2 = pygame.Rect(450, 17, 90, 30)
        self.radio_action_2 = self.radio_action_callback_2
        self.radio_2 = Radio(self.radio_options_2, self.radio_rect_2, self.radio_color, self.radio_text_color, self.radio_action_2)
        
        self.radio_options_3 = ["x", "o"]
        self.radio_rect_3 = pygame.Rect(550, 96, 50, 30)
        self.radio_action_3 = self.radio_action_callback_3
        self.radio_3 = Radio(self.radio_options_3, self.radio_rect_3, self.radio_color, self.radio_text_color, self.radio_action_3)

        pygame.init()
        self.game_reset
        

    #FXNS FOR BOARD SIZE
    def draw3x3(self):
        #3X3
        #Horizontal
        pygame.draw.line(self.screen, self.BEIGE, (0,200+(400/3)), (450,200+(400/3)), self.LineWidth)
        pygame.draw.line(self.screen, self.BEIGE, (0,200 +(2*(400/3))), (450,200+(2*(400/3))), self.LineWidth)
                
        #Vertical Lines
        pygame.draw.line(self.screen, self.BEIGE, ((450/3),200), ((450/3),600), self.LineWidth)
        pygame.draw.line(self.screen, self.BEIGE, ((2*(450/3)),200), ((2*(450/3)),600), self.LineWidth)
        
        #initialize board array
        self.rows,self.cols = (3,3)
        
        
        
    
    def draw4x4(self):
        #4X4 Board
        #Horizontal 
        pygame.draw.line(self.screen, self.BEIGE, (0,200+(400/4)), (450,200+(400/4)), self.LineWidth)
        pygame.draw.line(self.screen, self.BEIGE, (0,200 +(2*(400/4))), (450,200+(2*(400/4))), self.LineWidth)
        pygame.draw.line(self.screen, self.BEIGE, (0,200 +(3*(400/4))), (450,200+(3*(400/4))), self.LineWidth)
        
        #Vertical
        pygame.draw.line(self.screen, self.BEIGE, ((450/4),200), ((450/4),600), self.LineWidth)
        pygame.draw.line(self.screen, self.BEIGE, ((2*(450/4)),200), ((2*(450/4)),600), self.LineWidth)
        pygame.draw.line(self.screen, self.BEIGE, ((3*(450/4)),200), ((3*(450/4)),600), self.LineWidth)
        #initialize board array
        self.rows,self.cols = (4,4)
        
        
         
    def draw5x5(self):
        #5x5 BOARD
        #Horizontal
        pygame.draw.line(self.screen, self.BEIGE, (0,200+(400/5)), (450,200+(400/5)), self.LineWidth)
        pygame.draw.line(self.screen, self.BEIGE, (0,200 +(2*(400/5))), (450,200+(2*(400/5))), self.LineWidth)
        pygame.draw.line(self.screen, self.BEIGE, (0,200 +(3*(400/5))), (450,200+(3*(400/5))), self.LineWidth)
        pygame.draw.line(self.screen, self.BEIGE, (0,200 +(4*(400/5))), (450,200+(4*(400/5))), self.LineWidth)
        
        #Vertical
        pygame.draw.line(self.screen, self.BEIGE, ((450/5),200), ((450/5),600), self.LineWidth)
        pygame.draw.line(self.screen, self.BEIGE, ((2*(450/5)),200), ((2*(450/5)),600), self.LineWidth)
        pygame.draw.line(self.screen, self.BEIGE, ((3*(450/5)),200), ((3*(450/5)),600), self.LineWidth)
        pygame.draw.line(self.screen, self.BEIGE, ((4*(450/5)),200), ((4*(450/5)),600), self.LineWidth)
        
        #initialize board array
        self.rows,self.cols = (5,5)
        
    
    def draw_board(self):
        if self.bt == "3 x 3":
            self.draw3x3()
        elif self.bt == "4 x 4":
            self.draw4x4()
        elif self.bt == "5 x 5":
            self.draw5x5()
        self.board = np.zeros((self.rows,self.cols))
        self.game_state = GameStatus(self.board, True)
		

    def draw_game(self):
        #DRAW GRID
        # Draw the boarder of grid
        pygame.draw.rect(self.screen, self.FOREST, pygame.Rect(0, 200, 450, 400))
        pygame.draw.rect(self.screen, self.BEIGE, pygame.Rect(0, 200, 450, 400), 7)

        #call draw grid fxns based on selected board size from button
        if self.bt == "3 x 3":
            self.draw3x3()
        elif self.bt == "4 x 4":
            self.draw4x4()
        elif self.bt == "5 x 5":
            self.draw5x5()

        #GUI ELEMENTS
        title = self.font2.render("Tic-Tac-Toe ", True, self.TEAL)
        self.screen.blit(title, (100, 100))

        gt = self.font3.render("Game Type: ", True, self.MINT)
        bt = self.font3.render("Board Type: ", True, self.MINT)
        pt = self.font3.render("Player Type: ", True, self.MINT)
        score = self.font3.render("Scores", True, self.BLUE)
        sent1 = self.font4.render("1. Select Options",True, self.BLUE)
        sent2 = self.font4.render("2. Press 'Start'",True, self.BLUE)
        pygame.draw.line(self.screen, self.BLUE, (485, 178), (560, 178), width=2)
    
        self.screen.blit(gt, (30, 20))
        self.screen.blit(bt, (320, 20))
        self.screen.blit(pt, (420, 100))
        self.screen.blit(score, (490, 160))
        self.screen.blit(sent1, (460,400))
        self.screen.blit(sent2, (460,420))
        
        if self.mode == "Human v AI":
            human = self.font3.render("Human: ", True, self.BLUE)
            ai = self.font3.render("AI: ", True, self.BLUE)
            self.screen.blit(human, (460, 200))
            self.screen.blit(ai, (508, 240))
        elif self.mode == "Human v Human":
            p1 = self.font3.render("Player 1: ", True, self.BLUE)
            p2 = self.font3.render("Player 2: ", True, self.BLUE)
            self.screen.blit(p1, (460, 200))
            self.screen.blit(p2, (460, 240))
        
        self.draw_figures()
        


    #Mark numpy board w player #
    def mark_square(self, x, y , player):
        self.board[x][y] = player 
        #draw the figure on the board
        if player == 0:
            return
        return self.board
        

    #Check if numpy board space is empty
    def available_square(self,x,y):
        if self.board[x][y] == 0:
            return True
        else:
            return False
    
    def is_board_full(self):
        for i in self.board[self.rows]:
            for j in self.board[self.cols]:
                if self.board[i][j] == 0:
                    return False
                
    #Change turn of player
    def change_turn(self):
        
        if(self.game_state.turn_O):
            pygame.display.set_caption("Tic Tac Toe - O's turn")
        else:
            pygame.display.set_caption("Tic Tac Toe - X's turn")

    #BUTTON ACTIONS
    def button1_action(self):
        """ call play game (play game should dictate which game mode bassed off of mode chosen)"""
        print("Initiating Game...")
        #takes options and change board & gt

    def button2_action(self):
        print("Reseting Game...")
        self.game_reset()

    #RADIO ACTIONS

    #Set game mode
    def radio_action_callback_1(self, selected_option):

        self.mode = str(selected_option)
        self.draw_game()
        
    #Set board Type
    def radio_action_callback_2(self, selected_option):
        self.bt = str(selected_option)
        self.draw_board()
        
        

    def radio_action_callback_3(self, selected_option):
        if selected_option == 'x':
            self.human = 1
            self.ai = 2
        elif selected_option == 'o':
            self.human = 2
            self.ai = 1
        self.draw_game()

    #FXNS TO DRAW FIGURES
    def draw_circle(self, x, y): 

        #scale circle to 3x3 board
        if self.bt == "3 x 3":
            pygame.draw.circle(self.screen, self.BLUE, (int((2*y+1)*450/6),int((2*x+1)*(400/6)+200)),50, width = 10)
            
        #scale to 4x4
        elif self.bt == "4 x 4":
            pygame.draw.circle(self.screen, self.BLUE, (int((2*y+1)*450/8),int((2*x+1)*(400/8)+200)),40, width = 8)
        
        #scale to 5x5   
        elif self.bt == "5 x 5":
            pygame.draw.circle(self.screen, self.BLUE, (int((2*y+1)*450/10),int((2*x+1)*(400/10)+200)),30, width = 7)

    def draw_cross(self, x, y):

        if self.bt == "3 x 3":
            pygame.draw.line(self.screen, self.MINT,(int(((2*y+1)*(450/6))-(450/6)/2),int((((2*x+1)*(400/6)+200)-(450/6)/2))), 
                             (int(((2*y+1)*(450/6))+(450/6)/2),int((((2*x+1)*(400/6)+200)+(450/6)/2))), 
                             width = 10)
            pygame.draw.line(self.screen, self.MINT,(int(((2*y+1)*(450/6))+(450/6)/2),int((((2*x+1)*(400/6)+200)-(450/6)/2))), 
                             (int(((2*y+1)*(450/6))-(450/6)/2),int((((2*x+1)*(400/6)+200)+(450/6)/2))), 
                             width = 10)
        
        elif self.bt == "4 x 4":
            pygame.draw.line(self.screen, self.MINT,(int(((2*y+1)*(450/8))-(450/8)/2),int((((2*x+1)*(400/8)+200)-(450/8)/2))), 
                             (int(((2*y+1)*(450/8))+(450/8)/2),int((((2*x+1)*(400/8)+200)+(450/8)/2))), 
                             width = 10)
            pygame.draw.line(self.screen, self.MINT,(int(((2*y+1)*(450/8))+(450/8)/2),int((((2*x+1)*(400/8)+200)-(450/8)/2))), 
                             (int(((2*y+1)*(450/8))-(450/8)/2),int((((2*x+1)*(400/8)+200)+(450/8)/2))), 
                             width = 10)
        
        elif self.bt == "5 x 5":
            pygame.draw.line(self.screen, self.MINT,(int(((2*y+1)*(450/10))-(450/10)/2),int((((2*x+1)*(400/10)+200)-(450/10)/2))), 
                             (int(((2*y+1)*(450/10))+(450/10)/2),int((((2*x+1)*(400/10)+200)+(450/10)/2))), 
                             width = 10)
            pygame.draw.line(self.screen, self.MINT,(int(((2*y+1)*(450/10))+(450/10)/2),int((((2*x+1)*(400/10)+200)-(450/10)/2))), 
                             (int(((2*y+1)*(450/10))-(450/10)/2),int((((2*x+1)*(400/10)+200)+(450/10)/2))), 
                             width = 10)   
            
    #Transfer console board to screen 
    def draw_figures(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 1: #If player 1, draw cross
                    self.draw_cross(row,col)
                elif self.board[row][col] == 2: #if player 2, draw circle
                    self.draw_circle(row,col)



    def is_game_over(self):

        if self.game_state.is_terminal == True:
            return True
        else:
            return False
    
    def move(self, move):
        self.game_state = self.game_state.get_new_state(move)

    def play_ai(self):
        minimax_score, move = minimax(self.game_state, 5, False)
      
        if not move == None:
            x = move[0] #row
            y = move[1] #col
            self.move((x, y))
            self.mark_square(x, y,self.ai)
            
        if self.is_game_over():
            self.game_reset()
                
        self.change_turn()
        pygame.display.update()
        terminal = self.is_game_over
        print(self.game_state.get_scores(terminal))
        

    def game_reset(self):
        self.draw_game()
        self.draw_board()
        pygame.display.update()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def play_game(self, mode= "player_vs_ai"):
        running = True
        clock=pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for button in self.buttons:
                    button.handle_event(event)

                self.radio_1.handle_event(event)
                self.radio_2.handle_event(event)
                self.radio_3.handle_event(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    pos= pygame.mouse.get_pos
                    self.mouse_x = event.pos[0] #x
                    self.mouse_y = event.pos[1] #y
                    #if user clicked inside grid space
                    if 0 <= self.mouse_x <= 450 and 200 <= self.mouse_y <= 600:
                        
                        if self.bt == "3 x 3":
                            clicked_col = int((self.mouse_x - 10)// 148)
                            clicked_row = int((self.mouse_y -200 )// 131)
                            print(clicked_row,clicked_col) #CONSISTENCY: Always RowxColumn
                            #Mark the board
                            if self.available_square(clicked_row,clicked_col):
                                self.mark_square(clicked_row,clicked_col,self.human)
                                
                                
                                
                        elif self.bt == "4 x 4":
                            clicked_col = int((self.mouse_x - 10)// 108)
                            clicked_row = int((self.mouse_y -200 )// 98)
                            print(clicked_row,clicked_col)
                            if self.available_square(clicked_row,clicked_col):
                                self.mark_square(clicked_row,clicked_col,self.human)
                                
                        elif self.bt == "5 x 5":
                            clicked_col = int((self.mouse_x - 10)// 88)
                            clicked_row = int((self.mouse_y - 200 )// 78)
                            print(clicked_row,clicked_col)
                            if self.available_square(clicked_row,clicked_col):
                                self.mark_square(clicked_row,clicked_col,self.human)
                                
                             
                        if self.human:
                            self.move((clicked_row,clicked_col))
                            if self.mode == "Human v AI":  
                                if not self.is_game_over():
                                    self.play_ai()
                                else: 
                                    print(self.game_state.get_scores(self.is_game_over))
                                    self.game_reset()
                            elif self.mode == "Human v Human":
                                if not self.is_game_over():
                                    if self.human == 1:
                                        self.human = 2      #change turn 'o'
                                        #pygame.display.set_caption("Tic Tac Toe - O's turn")
                                    else:
                                        self.human = 1      #change turn 'x'
                                            #pygame.display.set_caption("Tic Tac Toe - X's turn")
                                else: 
                                    self.game_state.get_scores(True)
                            
                    

            self.screen.fill((255, 255, 255))
            self.draw_game()
            
            
            for button in self.buttons:
                button.draw(self.screen)
            self.radio_1.draw(self.screen)
            self.radio_2.draw(self.screen)
            self.radio_3.draw(self.screen)
            

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game = RandomBoardTicTacToe()
    game.play_game(game.mode)

