import tkinter as tk
import random
from tkinter import messagebox
from user import add_medium_win

def clear_btn(buttons):
    not_empty_buttons = [b for row in buttons for b in row]
    for i in not_empty_buttons:
        i.config(text="", state=tk.NORMAL)

def check_board(board_text):
    """Pure win-check on a 2D text board. Returns 'X', 'O', 'tie', or None."""
    lines = [
        [board_text[0][0],board_text[0][1],board_text[0][2]],
        [board_text[1][0],board_text[1][1],board_text[1][2]],
        [board_text[2][0],board_text[2][1],board_text[2][2]],
        [board_text[0][0],board_text[1][0],board_text[2][0]],
        [board_text[0][1],board_text[1][1],board_text[2][1]],
        [board_text[0][2],board_text[1][2],board_text[2][2]],
        [board_text[0][0],board_text[1][1],board_text[2][2]],
        [board_text[0][2],board_text[1][1],board_text[2][0]],
    ]
    for line in lines:
        if line == ["X","X","X"]: return "X"
        if line == ["O","O","O"]: return "O"
    if all(board_text[r][c] != "" for r in range(3) for c in range(3)): return "tie"
    return None

def check_winner(board):    
    board_text=[[board[r][c].cget("text") for c in range(3)] for r in range(3)]
    status = check_board(board_text)
    if status=="X": 
        messagebox.showinfo("Game Over","YOU WON 🎉")
        add_medium_win()
        clear_btn(board)
        return "X"
    elif status=="O": 
        messagebox.showinfo("Game Over","Computer Won 😔")
        clear_btn(board)
        return "O"
    elif status=="tie":
        messagebox.showinfo("Game Over","It's a Tie 😐")
        clear_btn(board)
        return "tie"
    return 0

def easy_mode(btn, board):
    if btn.cget("text")=='':
        btn.config(text="X",state=tk.DISABLED)
        # flatten + filter for empty buttons
        empty_buttons = [b for row in board for b in row if b.cget("text") == ""]
        win=check_winner(board)
        if win==0:
            if empty_buttons:     # only if any are left
                ai_btn = random.choice(empty_buttons)
                ai_btn.config(text="O", state=tk.DISABLED)
        check_winner(board)

#Computer logic
def medium_mode(btn, board):
    if btn.cget("text")=='':
        btn.config(text="X",state=tk.DISABLED)
        # flatten + filter for empty buttons
        board=[[board[r][c] for c in range (3)]for r in range (3)]
        empty_buttons = [b for row in board for b in row if b.cget("text") == ""]
        cnt=len(empty_buttons)
        win=check_winner(board)
        if cnt==0:
            win=check_winner(board)
        elif win==0:
            check_medium(cnt, board)
        if cnt==8:
            if board[1][1].cget("text")=="X" :
                ai_btn = random.choice([board[0][0], board[0][2],board[2][0], board[2][2]])
                ai_btn.config(text="O", state=tk.DISABLED)
            else:
                board[1][1].config(text="O", state=tk.DISABLED)
        check_winner(board)

def check_medium(cnt, board):
    board=[[board[r][c] for c in range (3)]for r in range (3)]
    empty_buttons = [b for row in board for b in row if b.cget("text") == ""]
    hori_1=[board[0][0].cget("text"),board[0][1].cget("text"),board[0][2].cget("text")]
    hori_2=[board[1][0].cget("text"),board[1][1].cget("text"),board[1][2].cget("text")]
    hori_3=[board[2][0].cget("text"),board[2][1].cget("text"),board[2][2].cget("text")]
    ver_1=[board[0][0].cget("text"),board[1][0].cget("text"),board[2][0].cget("text")]
    ver_2=[board[0][1].cget("text"),board[1][1].cget("text"),board[2][1].cget("text")]
    ver_3=[board[0][2].cget("text"),board[1][2].cget("text"),board[2][2].cget("text")]
    diag_1=[board[0][0].cget("text"),board[1][1].cget("text"),board[2][2].cget("text")]
    diag_2=[board[0][2].cget("text"),board[1][1].cget("text"),board[2][0].cget("text")]
    # See if AI is winning
    if hori_1==["O","O",""]:
        board[0][2].config(text="O", state=tk.DISABLED)
    elif hori_1==["O","","O"]:
        board[0][1].config(text="O", state=tk.DISABLED)
    elif hori_1==["","O","O"]:
        board[0][0].config(text="O", state=tk.DISABLED)
    elif hori_2==["O","O",""]:
        board[1][2].config(text="O", state=tk.DISABLED)
    elif hori_2==["O","","O"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif hori_2==["","O","O"]:
        board[1][0].config(text="O", state=tk.DISABLED)
    elif hori_3==["O","O",""]:
        board[2][2].config(text="O", state=tk.DISABLED)
    elif hori_3==["O","","O"]:
        board[2][1].config(text="O", state=tk.DISABLED)
    elif hori_3==["","O","O"]:
        board[2][0].config(text="O", state=tk.DISABLED)
    elif ver_1==["O","O",""] :
        board[2][0].config(text="O", state=tk.DISABLED)
    elif ver_1==["O","","O"]:
        board[1][0].config(text="O", state=tk.DISABLED)
    elif ver_1==["","O","O"]:
        board[0][0].config(text="O", state=tk.DISABLED)
    elif ver_2==["O","O",""]:
        board[2][1].config(text="O", state=tk.DISABLED)
    elif ver_2==["O","","O"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif ver_2==["","O","O"]:
        board[0][1].config(text="O", state=tk.DISABLED)
    elif ver_3==["O","O",""]:
        board[2][2].config(text="O", state=tk.DISABLED)
    elif ver_3==["O","","O"]:
        board[1][2].config(text="O", state=tk.DISABLED)
    elif ver_3==["","O","O"]:
        board[0][2].config(text="O", state=tk.DISABLED)
    elif diag_1==["O","O",""]:
        board[2][2].config(text="O", state=tk.DISABLED)
    elif diag_1==["O","","O"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif diag_1==["","O","O"]:
        board[0][0].config(text="O", state=tk.DISABLED)
    elif diag_2==["O","O",""]:
        board[2][0].config(text="O", state=tk.DISABLED)
    elif diag_2==["O","","O"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif diag_2==["","O","O"]:
        board[0][2].config(text="O", state=tk.DISABLED)
    # Check to block user
    elif hori_1==["X","X",""]:
        board[0][2].config(text="O", state=tk.DISABLED)
    elif hori_1==["X","","X"]:
        board[0][1].config(text="O", state=tk.DISABLED)
    elif hori_1==["","X","X"]:
        board[0][0].config(text="O", state=tk.DISABLED)
    elif hori_2==["X","X",""]:
        board[1][2].config(text="O", state=tk.DISABLED)
    elif hori_2==["X","","X"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif hori_2==["","X","X"]:
        board[1][0].config(text="O", state=tk.DISABLED)
    elif hori_3==["X","X",""]:
        board[2][2].config(text="O", state=tk.DISABLED)
    elif hori_3==["X","","X"]:
        board[2][1].config(text="O", state=tk.DISABLED)
    elif hori_3==["","X","X"]:
        board[2][0].config(text="O", state=tk.DISABLED)
    elif ver_1==["X","X",""] :
        board[2][0].config(text="O", state=tk.DISABLED)
    elif ver_1==["X","","X"]:
        board[1][0].config(text="O", state=tk.DISABLED)
    elif ver_1==["","X","X"]:
        board[0][0].config(text="O", state=tk.DISABLED)
    elif ver_2==["X","X",""]:
        board[2][1].config(text="O", state=tk.DISABLED)
    elif ver_2==["X","","X"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif ver_2==["","X","X"]:
        board[0][1].config(text="O", state=tk.DISABLED)
    elif ver_3==["X","X",""]:
        board[2][2].config(text="O", state=tk.DISABLED)
    elif ver_3==["X","","X"]:
        board[1][2].config(text="O", state=tk.DISABLED)
    elif ver_3==["","X","X"]:
        board[0][2].config(text="O", state=tk.DISABLED)
    elif diag_1==["X","X",""]:
        board[2][2].config(text="O", state=tk.DISABLED)
    elif diag_1==["X","","X"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif diag_1==["","X","X"]:
        board[0][0].config(text="O", state=tk.DISABLED)
    elif diag_2==["X","X",""]:
        board[2][0].config(text="O", state=tk.DISABLED)
    elif diag_2==["X","","X"]:
        board[1][1].config(text="O", state=tk.DISABLED)
    elif diag_2==["","X","X"]:
        board[0][2].config(text="O", state=tk.DISABLED)
    #Other winning conditions
    elif cnt!=8:
        #if user starts from corner and plays next on side middle
        if board[1][1].cget("text")=="O" and (board[0][1].cget("text")=="" or board[1][0].cget("text")=="" or board[1][2].cget("text")=="" or board[2][1].cget("text")==""):
            if ((board[2][0].cget("text")=="X" and board[0][1].cget("text")=="X") or (board[0][0].cget("text")=="X" and board[2][1].cget("text")=="X")) and (board[1][2].cget("text")==""):
                board[1][2].config(text="O", state=tk.DISABLED)
            elif ((board[2][2].cget("text")=="X" and board[0][1].cget("text")=="X") or (board[0][2].cget("text")=="X" and board[2][1].cget("text")=="X")) and (board[1][0].cget("text")==""):
                board[1][0].config(text="O", state=tk.DISABLED)
            elif board[1][1].cget("text")=="O" and (board[0][0].cget("text")=="" or board[0][2].cget("text")=="" or board[2][0].cget("text")=="" or board[2][2].cget("text")==""):
                if ((board[2][1].cget("text")=="X" and board[1][2].cget("text")=="X")) and (board[2][2].cget("text")==""):
                    board[2][2].config(text="O", state=tk.DISABLED)
                elif ((board[1][0].cget("text")=="X" and board[2][1].cget("text")=="X"))and (board[2][0].cget("text")==""):
                    board[2][0].config(text="O", state=tk.DISABLED)
                elif ((board[0][1].cget("text")=="X" and board[1][0].cget("text")=="X")) and (board[0][0].cget("text")==""):
                    board[0][0].config(text="O", state=tk.DISABLED)
                elif ((board[0][1].cget("text")=="X" and board[1][2].cget("text")=="X")) and (board[0][2].cget("text")==""):
                    board[0][2].config(text="O", state=tk.DISABLED)
                elif ((board[1][2].cget("text")=="X" and (board[0][0].cget("text")=="X" or board[2][0].cget("text")=="X"))) and (board[2][1].cget("text")==""):
                    board[2][1].config(text="O", state=tk.DISABLED)
                elif ((board[2][1].cget("text")=="X" and (board[0][0].cget("text")=="X" or board[0][2].cget("text")=="X"))) and (board[1][0].cget("text")==""):
                    board[1][0].config(text="O", state=tk.DISABLED)
                elif ((board[1][0].cget("text")=="X" and (board[0][2].cget("text")=="X" or board[2][2].cget("text")=="X"))) and (board[2][1].cget("text")==""):
                    board[2][1].config(text="O", state=tk.DISABLED)
                elif ((board[0][1].cget("text")=="X" and (board[2][0].cget("text")=="X" or board[2][2].cget("text")=="X"))) and (board[1][0].cget("text")==""):
                    board[1][0].config(text="O", state=tk.DISABLED)
                else:
                    if ((board[2][0].cget("text")=="X" and board[0][2].cget("text")=="X") or (board[0][0].cget("text")=="X" and board[2][2].cget("text")=="X")):
                        blank_list1=[]
                        if board[0][1].cget("text")=="":
                            blank_list1.append(board[0][1])
                        if board[1][0].cget("text")=="":
                            blank_list1.append(board[1][0])
                        if board[1][2].cget("text")=="":
                            blank_list1.append(board[1][2])
                        if board[2][1].cget("text")=="":
                            blank_list1.append(board[2][1])
                        ai_btn = random.choice(blank_list1)
                        ai_btn.config(text="O", state=tk.DISABLED)
                    else:
                        ai_btn = random.choice(empty_buttons)
                        ai_btn.config(text="O", state=tk.DISABLED)
            #if user plays 2 corners
            else:
                blank_list1=[]
                if board[0][1].cget("text")=="":
                    blank_list1.append(board[0][1])
                if board[1][0].cget("text")=="":
                    blank_list1.append(board[1][0])
                if board[1][2].cget("text")=="":
                    blank_list1.append(board[1][2])
                if board[2][1].cget("text")=="":
                    blank_list1.append(board[2][1])
                ai_btn = random.choice(blank_list1)
                ai_btn.config(text="O", state=tk.DISABLED)
        #if user starts from middle
        elif board[1][1].cget("text")=="X" and (board[0][0].cget("text")=="" or board[0][2].cget("text")=="" or board[2][0].cget("text")=="" or board[2][2].cget("text")==""):
            blank_list2=[]
            if board[0][0].cget("text")=="":
                blank_list2.append(board[0][0])
            if board[0][2].cget("text")=="":
                blank_list2.append(board[0][2])
            if board[2][0].cget("text")=="":
                blank_list2.append(board[2][0])
            if board[2][2].cget("text")=="":
                blank_list2.append(board[2][2])
            ai_btn = random.choice(blank_list2)
            ai_btn.config(text="O", state=tk.DISABLED)
        else:
            ai_btn = random.choice(empty_buttons)
            ai_btn.config(text="O", state=tk.DISABLED)

def hard_mode(btn, board):
    if btn.cget("text")=='':
        btn.config(text="X",state=tk.DISABLED)
        board_text=[[board[r][c].cget("text") for c in range(3)] for r in range(3)]
        empty_buttons=[b for row in board for b in row if b.cget("text")==""]
        cnt=len(empty_buttons)
        win=check_winner(board)
        if cnt==0:
            win=check_winner(board)
        elif win==0:
            pos=best_move(board_text)
            if pos:
                r,c=pos
                board[r][c].config(text="O",state=tk.DISABLED)
        check_winner(board)

def best_move(board):
    """Return (row, col) of the best move for O using minimax."""
    best_score, best_pos = -100, None
    for r in range(3):
        for c in range(3):
            if board[r][c]=="":
                board[r][c]="O"
                score = minimax(board, False)
                board[r][c]=""
                if score > best_score:
                    best_score, best_pos = score, (r, c)
    return best_pos

def minimax(board, is_maximizing):
    """Minimax: O is maximiser (+10), X is minimiser (-10), tie is 0."""
    result = check_board(board)
    if result=="O":   return 10
    if result=="X":   return -10
    if result=="tie": return 0
    if is_maximizing:
        best = -100
        for r in range(3):
            for c in range(3):
                if board[r][c]=="":
                    board[r][c]="O"
                    best = max(best, minimax(board, False))
                    board[r][c]=""
        return best
    else:
        best = 100
        for r in range(3):
            for c in range(3):
                if board[r][c]=="":
                    board[r][c]="X"
                    best = min(best, minimax(board, True))
                    board[r][c]=""
        return best
