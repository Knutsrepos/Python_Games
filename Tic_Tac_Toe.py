"""
Tic tac toe. Up to now only two player version. I am currently working on a one player version
using Monte Carlo.
"""

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import numpy as np

#Define some constants
GRID_NUMBER=4
GRID_CELL_SIZE=500/GRID_NUMBER

#Define some global varaiables that are changed during the programm
blue_score_G=0
brown_score_G=0

class Draw:
    """
    Contains methods to draw pieces, the board during a game and the canvas if somebody won
    """
    def draw_piece(self,canvas,position,team,radius):
        """
        Draws piece on a given position. The color depends on the team.
        """
        break_cond=0
        #Set the color of the circle depending on the team
        if team==1:
            team_color="Brown"
        elif team==-1:
            team_color="Blue"
        #Set piece in the center of a grid cell
        circle_position=((position[0]+0.5)*GRID_CELL_SIZE+50,(position[1]+0.5)*GRID_CELL_SIZE+50)
        canvas.draw_circle([circle_position[0],circle_position[1]],radius,5,"White",
                            fill_color=team_color)
    
    def draw_board(self,canvas):
        """
        Draws the board containing the background and the grid
        """
        canvas.draw_polygon([[50,50],[550,50],[550,550],[50,550]], 12, 'Grey','Grey')
        for i in range(0,(GRID_NUMBER-1)):
            canvas.draw_line([50,(i+1)*GRID_CELL_SIZE+50],[550,(i+1)*GRID_CELL_SIZE+50],6,"White")
            canvas.draw_line([(i+1)*GRID_CELL_SIZE+50,50],[(i+1)*GRID_CELL_SIZE+50,550],6,"White")

    def draw_winner(self,canvas,winner):
        """
        Draws the canvas if somebody won
        """
        global brown_score_G,blue_score_G    
        #Set the radii depending on the winner
        if winner is 'Brown':
            radius_brown=10*(-1)**tick_counter_G
            radius_blue=-30
        elif winner is 'Blue':
            radius_brown=-30
            radius_blue=10*(-1)**tick_counter_G
        
        timer.start()
        #Leave board as is. Reduce size of the loser pieces (Brown), let the winner pieces blink
        if tick_counter_G<10:
            boardDraw=Draw()
            boardDraw.draw_board(canvas)
            set_pieces(canvas,radius_brown,radius_blue)
        #Write down the winner    
        elif tick_counter_G>10 and tick_counter_G<20:    
            canvas.draw_polygon([[0,0],[600,0],[600,600],[0,600]],10, 'Grey')
            canvas.draw_text(winner+' wins ',[220,300],40,winner)
        #Start new game
        elif tick_counter_G>20:    
            new_game()
            timer.stop()
            #Increment points for the winner
            if winner is 'Brown':
                brown_score_G+=1
            elif winner is 'Blue':
                blue_score_G+=1        
 

def get_winner():
    """
    Checks if somebody won the game
    """
    #Sum over diagonal, counter diagonal, rows (max and min values), columns (max and min values)
    diag_sum=np.sum(np.diag(coord_array_G))
    counter_diag_sum=np.sum(np.diag(np.fliplr(coord_array_G)))
    row_max=np.max(np.dot(coord_array_G,np.ones(GRID_NUMBER)))
    row_min=np.min(np.dot(coord_array_G,np.ones(GRID_NUMBER)))
    col_max=np.max(np.dot(np.ones(GRID_NUMBER),coord_array_G))
    col_min=np.min(np.dot(np.ones(GRID_NUMBER),coord_array_G))    
    #Summerarize everything into one tuple
    win_cond=(diag_sum,counter_diag_sum,row_max,row_min,col_max,col_min)
    #Check if win_cond contains +-GRID_NUMBER (+ Brown wins,- Blue wins)
    if GRID_NUMBER in win_cond:
        return 1
    if -GRID_NUMBER in win_cond:
        return -1
    else:
        return 0    

    
def compose(canvas):
    """
    Draws board depending on the state of the game
    """
    #Write the score for each player
    canvas.draw_text('Blue '+str(blue_score_G),[60,585],30,'Blue')
    canvas.draw_text('Brown '+str(brown_score_G),[430,585],30,'Brown')
    #Draw the grid unless there is no winner
    if get_winner()==0:
        boardDraw=Draw()
        boardDraw.draw_board(canvas)
        set_pieces(canvas,0,0)
    #Draw winner box
    #Brown is the winner
    elif get_winner()==1:
        brownWinsDraw=Draw()
        brownWinsDraw.draw_winner(canvas,'Brown')    
    #Blue is the winner        
    elif get_winner()==-1:
        blueWinsDraw=Draw()
        blueWinsDraw.draw_winner(canvas,'Blue')            
        
  
def click(position):
    """
    Handler for mouse clicks. If player clicks on a grid field the value of the grid matrix is
    changed accordingly (-1:Blue,0:Empty,1:Brown).
    """
    global player_index_G
    break_cond=0
    for i in range(0,GRID_NUMBER):
        for j in range(0,GRID_NUMBER):
            if position[0]<(i+1)*GRID_CELL_SIZE+50 and position[1]<(j+1)*GRID_CELL_SIZE+50:
                if coord_array_G[j,i]==0:
                    coord_array_G[j,i]=(-1)**player_index_G
                else:
                    player_index_G-=1
                break_cond=1
                break
        if break_cond==1:
            break
    player_index_G+=1

def set_pieces(canvas,radius_brown,radius_blue):
    """
    Sets pieces depending on the value in grid matrix (-1:Blue,0:Empty,1:Brown).
    """
    for i in range(0,len(coord_array_G)):
        for j in range(0,len(coord_array_G)):
            if coord_array_G[i,j]>0:
                pieceDraw=Draw()
                pieceDraw.draw_piece(canvas,(j,i),1,GRID_CELL_SIZE/3+radius_brown)
            elif coord_array_G[i,j]<0:
                pieceDraw=Draw()
                pieceDraw.draw_piece(canvas,(j,i),-1,GRID_CELL_SIZE/3+radius_blue)
                
def tick():
    """
    Incement time
    """
    global tick_counter_G
    tick_counter_G += 1
    
def new_game():
    """
    If a new game starts, initialize global variables that are changed during the programm
    """
    global coord_array_G,player_index_G,tick_counter_G
    tick_counter_G=0
    coord_array_G=np.zeros((GRID_NUMBER,GRID_NUMBER))
    player_index_G=0

"""
Main
"""
#Create Frame and get everything into rolling
frame = simplegui.create_frame("Tic Tac Toe", 600, 600,100)
frame.set_canvas_background("Lightgrey")

frame.add_button("Restart",new_game,100)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(compose)

timer=simplegui.create_timer(200,tick)

#Start the game
new_game()
frame.start()
