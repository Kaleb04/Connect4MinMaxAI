import tkinter as tk
import random
import math

root = tk.Tk()
root.title("Connect4")
canvas = tk.Canvas(root, width=750, height=750, bg='#2167b8')
canvas.pack()
rows, cols = (6, 7)
row=-1
gameRunning=False
xTurn='X'
end=False
availableSlots=0
prev_col=-1
firstMove=True

if gameRunning:
    canvas.bind("<Button-1>", )
    canvas.bind("<Motion>",)
else:
    canvas.create_text(400, 350, text="Choose Game Mode", font=('Arial', 40, 'bold'), fill="black")
    twoplayer_button = tk.Button(root, text="2 Players", command=lambda:restart_game(False))
    ai_button = tk.Button(root, text="AI vs Player", command=lambda:restart_game(True))
    canvas.create_window(300, 450, window=twoplayer_button) 
    canvas.create_window(500, 450, window=ai_button) 

def initialize_board():
    return [[None for i in range(cols)] for j in range(rows)]

def canPlace(input):
    global row
    for y in range(cols):
        if(board[5-y][input-1]==None):
            row=5-y
            if(xTurn=='X'):
                board[5-y][input-1]='X'
                canvas.create_oval(input*100-65, (6-y)*100+60 , input*100+15 , (6-y)*100+140 , width=2,fill="red")
                canvas.create_oval(input*100-65, 45,input*100+15,125, fill="#fff982")
                return True
            else:
                board[5-y][input-1]='O'
                canvas.create_oval(input*100-65, (6-y)*100+60 , input*100+15 , (6-y)*100+140 , width=2,fill="yellow")
                canvas.create_oval(input*100-65, 45,input*100+15,125, fill="#f7827c")
                return True
    return False

def count_consecutive(r, c, dr, dc,sign):
        count = 0
        for step in range(1, 4):  # Check next three positions
            nr, nc = r + step * dr, c + step * dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == sign:
                count += 1
            else:
                break
        return count

def winCheck(input, row, sign):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Left, Up, Up-Left, Up-Right
    col = input - 1
    for dr, dc in directions:
        count = 1  
        count += count_consecutive(row, col, dr, dc,sign)  # Check one direction
        count += count_consecutive(row, col, -dr, -dc,sign)  # Check opposite direction
        if count >= 4:
            return True
    return False

def check_game_status(col, player):
    global xTurn,row
    if winCheck(col, row, player):
        display_winner(player)
    elif availableSlots==42:
            display_winner("tie")
    else:
        xTurn = 'O' if player == 'X' else 'X'

def canvas_click(event):
    global xTurn,gameRunning
    if gameRunning:
        x=event.x
        if 35<x<710:
            col = ((x-35) // (680 // cols))+1
            if canPlace(col):
                check_game_status(col,xTurn)
            if playing_ai:
                ai()

def hover(event):
    global prev_col,xTurn
    if gameRunning:
        x = event.x
        if 35<x<710:
            col = ((x-35) // (680 // cols))+1  # Each column width as canvas width divided by number of cols
            if col != prev_col:
                if prev_col >= 0:
                    canvas.create_rectangle(0,0,800,150, outline='', fill='white', width=0)  # Clear the previous hover
                if xTurn=='X':
                    canvas.create_oval(col*100-65, 45,col*100+15,125, fill="#f7827c")
                else:
                    canvas.create_oval(col*100-65, 45,col*100+15,125, fill="#fff982")
                prev_col = col

def draw_board(canvas):
    canvas.delete("all")
    canvas.create_rectangle(0,0,750,150,fill='white')
    for x in range (1,8):
        for y in range (1,7):
            canvas.create_oval(x*100-65, y*100+60 , x*100+15 , y*100+140 , width=2,fill="white")
    
def restart_game(x):
    global board, current_player,gameRunning,playing_ai,xTurn,firstMove
    gameRunning=True
    firstMove=True
    xTurn='X'
    board = initialize_board()
    current_player = 'X'
    canvas.delete("all")
    draw_board(canvas)
    if(x):
        playing_ai=True
        ai()
    else:
        playing_ai=False
    canvas.bind("<Button-1>", canvas_click)  
    canvas.bind("<Motion>", hover) 


def display_winner(winner):
    global gameRunning
    gameRunning=False
    if winner == "tie":
        text = "It's a tie!"
    else:
        if winner=='X':
            text = "Red Wins!"
        else:
            text= "Yellow Wins!"
    canvas.create_rectangle(0,0,800,150, outline='', fill='white', width=0)
    canvas.create_text(385, 50, text=text, font=('Arial', 40, 'bold'), fill="black",)
    
    twoplayer_button = tk.Button(root, text="2 Players", command=lambda:restart_game(False))
    ai_button = tk.Button(root, text="AI vs Player", command=lambda:restart_game(True))
    canvas.create_window(275, 110, window=twoplayer_button) 
    canvas.create_window(475, 110, window=ai_button) 

def avail_moves(board):
    return [(i+1) for i in range(7) if board[0][i] is None]

def ai():
    global firstMove,xTurn,prev_col
    if firstMove:
        firstMove=False
        canPlace(4)
        xTurn= 'O' 
    else:
        col=minimax(board,xTurn,-1,-1,xTurn,0,availableSlots,-math.inf,math.inf)['position']
        canPlace(col)
        canvas.create_rectangle(0,0,800,150, outline='', fill='white', width=0)  # Clear the previous hover
        canvas.create_oval(prev_col*100-65, 45,prev_col*100+15,125, fill="#fff982")
        check_game_status(col,xTurn)
        # root.after(500,check_game_status,col,xTurn)
        

def hueristic_eval(board,current_player):
    opponent_player='O' if current_player=='X' else 'X'
    current_player=score_position(board,current_player)
    opponent_player=score_position(board,opponent_player)
    return current_player-opponent_player

def score_position(board, player):
    score = 0
    center_array = [i[cols//2] for i in board]
    center_count = center_array.count(player)#Checks center column
    score += center_count * 3  

    # Score horizontal, vertical, and diagonal lines
    for row in range(rows):
        row_array = [board[row][i] for i in range(cols)]
        score += evaluate_line(row_array, player)
    for col in range(cols):
        col_array = [board[row][col] for row in range(rows)]
        score += evaluate_line(col_array, player)
    for row in range(rows - 3):
        for col in range(cols - 3):
            diag1_array = [board[row+i][col+i] for i in range(4)]
            diag2_array = [board[row+3-i][col+i] for i in range(4)]
            score += evaluate_line(diag1_array, player)
            score += evaluate_line(diag2_array, player)
    return score

def evaluate_line(line, player):
    opponent = 'O' if player == 'X' else 'X'
    score = 0
    if line.count(player) == 4:
        score += 100
    elif line.count(player) == 3 and line.count(None) == 1:
        score += 10
    elif line.count(player) == 2 and line.count(None) == 2:
        score += 5
    if line.count(opponent) == 3 and line.count(None) == 1:
        score -= 80
    return score

def minimax(board,current_player,prev_col,prev_row,og_player,availableSlots,depth,alpha,beta,maxdepth=6):
    max_player=og_player
    other_player = 'O' if current_player == 'X' else 'X'
    if winCheck(prev_col, prev_row, other_player):
        return {'position': None, 'score':100 * (41-availableSlots) if other_player == max_player else -100 * (41-availableSlots)}
    elif (42-availableSlots)==0:
        return{'position':None,'score':0}
    if current_player == max_player:
        best = {'position': None, 'score': -math.inf}  # each score should maximize
    else:
        best = {'position': None, 'score': math.inf}  # each score should minimize
    if depth>maxdepth:
        return {'position':None,'score':2*hueristic_eval(board,current_player)*(41-availableSlots)}
    for possible_move in avail_moves(board):
        for y in range(7):
            if(board[5-y][possible_move-1]==None):
                row=5-y
                break
        col=possible_move-1
        board[row][col] = current_player
        sim_score=minimax(board,other_player,col,row,og_player,availableSlots+1,depth+1,alpha,beta)

        board[row][col]=None
        sim_score['position'] = possible_move  # this represents the move optimal next move

        if current_player == max_player:  # X is max player
            if sim_score['score'] > best['score']:
                best = sim_score
            alpha = max(alpha, sim_score['score'])
        else:
            if sim_score['score'] < best['score']:
                best = sim_score
            beta = min(beta, sim_score['score'])
        if beta <= alpha:
            break
    # print(best)
    return best

root.mainloop()