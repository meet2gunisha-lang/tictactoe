import tkinter as tk
import random
from tkinter import messagebox

# Resets all cells on the board to empty and re-enables them for a new game
def clear_btn(buttons):
    not_empty_buttons = [b for row in buttons for b in row]
    for i in not_empty_buttons:
        i.config(text="", state=tk.NORMAL)

# Pure win-check on a 2D text board (no UI side effects)
# Checks all 8 lines: 3 rows, 3 columns, 2 diagonals
# Returns 'X', 'O', 'tie', or None (game still ongoing)
def check_board(board_text):
    """Pure win-check on a 2D text board. Returns 'X', 'O', 'tie', or None."""
    lines = [
        # rows
        [board_text[0][0],board_text[0][1],board_text[0][2]],
        [board_text[1][0],board_text[1][1],board_text[1][2]],
        [board_text[2][0],board_text[2][1],board_text[2][2]],
        # columns
        [board_text[0][0],board_text[1][0],board_text[2][0]],
        [board_text[0][1],board_text[1][1],board_text[2][1]],
        [board_text[0][2],board_text[1][2],board_text[2][2]],
        # diagonals
        [board_text[0][0],board_text[1][1],board_text[2][2]],
        [board_text[0][2],board_text[1][1],board_text[2][0]],
    ]
    for line in lines:
        if line == ["X","X","X"]: return "X"
        if line == ["O","O","O"]: return "O"
    if all(board_text[r][c] != "" for r in range(3) for c in range(3)): return "tie"  # board full, no winner
    return None

# Converts button grid to text, calls check_board, then shows the game-over dialog
# Returns 'X', 'O', 'tie' when game ends; returns 0 if still in progress
def check_winner(board):
    board_text=[[board[r][c].cget("text") for c in range(3)] for r in range(3)]
    status = check_board(board_text)
    if status=="X":
        messagebox.showinfo("Game Over","YOU WON 🎉")
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
    return 0  # game not over yet

# Easy mode: player places X, computer picks a random empty cell for O
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
# Medium mode: player places X, AI follows priority — win > block > strategy
def medium_mode(btn, board):
    if btn.cget("text")=='':
        btn.config(text="X",state=tk.DISABLED)
        # flatten + filter for empty buttons
        board=[[board[r][c] for c in range (3)]for r in range (3)]
        empty_buttons = [b for row in board for b in row if b.cget("text") == ""]
        cnt=len(empty_buttons)  # number of empty cells after X's move
        win=check_winner(board)
        if cnt==0:
            win=check_winner(board)  # board full, check tie
        elif win==0:
            check_medium(cnt, board)  # run AI decision logic
        # first move special case: counter X's opening
        if cnt==8:
            if board[1][1].cget("text")=="X" :  # X took center → O takes a corner
                ai_btn = random.choice([board[0][0], board[0][2],board[2][0], board[2][2]])
                ai_btn.config(text="O", state=tk.DISABLED)
            else:  # X took a non-center cell → O claims center
                board[1][1].config(text="O", state=tk.DISABLED)
        check_winner(board)

# Medium AI decision logic: evaluates the board and picks the best cell for O
# Priority order: 1) win immediately  2) block X  3) positional strategy
def check_medium(cnt, board):
    board=[[board[r][c] for c in range (3)]for r in range (3)]
    empty_buttons = [b for row in board for b in row if b.cget("text") == ""]

    # Build all 8 winning lines as (text_values, button_refs) pairs
    lines = [
        # rows
        ([board[0][0].cget("text"), board[0][1].cget("text"), board[0][2].cget("text")], [board[0][0], board[0][1], board[0][2]]),
        ([board[1][0].cget("text"), board[1][1].cget("text"), board[1][2].cget("text")], [board[1][0], board[1][1], board[1][2]]),
        ([board[2][0].cget("text"), board[2][1].cget("text"), board[2][2].cget("text")], [board[2][0], board[2][1], board[2][2]]),
        # columns
        ([board[0][0].cget("text"), board[1][0].cget("text"), board[2][0].cget("text")], [board[0][0], board[1][0], board[2][0]]),
        ([board[0][1].cget("text"), board[1][1].cget("text"), board[2][1].cget("text")], [board[0][1], board[1][1], board[2][1]]),
        ([board[0][2].cget("text"), board[1][2].cget("text"), board[2][2].cget("text")], [board[0][2], board[1][2], board[2][2]]),
        # diagonals
        ([board[0][0].cget("text"), board[1][1].cget("text"), board[2][2].cget("text")], [board[0][0], board[1][1], board[2][2]]),
        ([board[0][2].cget("text"), board[1][1].cget("text"), board[2][0].cget("text")], [board[0][2], board[1][1], board[2][0]]),
    ]

    def fill_line(player):
        """If any line has 2 of `player` and 1 empty, place O in the empty cell. Returns True if placed."""
        for text_line, btn_line in lines:
            if text_line.count(player) == 2 and text_line.count("") == 1:
                btn_line[text_line.index("")].config(text="O", state=tk.DISABLED)
                return True
        return False

    # Priority 1: complete O's two-in-a-row to win
    if fill_line("O"):
        pass
    # Priority 2: block X's two-in-a-row
    elif fill_line("X"):
        pass
    #Other winning conditions — positional heuristics when no immediate threat exists
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
                    # X on opposite corners → play an edge to avoid fork
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
            #if user plays 2 corners — respond with an edge to neutralise fork threat
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
        #if user starts from middle — O counters by taking a corner
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
            # no pattern matched — fall back to a random empty cell
            ai_btn = random.choice(empty_buttons)
            ai_btn.config(text="O", state=tk.DISABLED)

# Hard mode: player places X, computer uses minimax to always play optimally
def hard_mode(btn, board):
    if btn.cget("text")=='':
        btn.config(text="X",state=tk.DISABLED)
        board_text=[[board[r][c].cget("text") for c in range(3)] for r in range(3)]  # convert to text for minimax
        empty_buttons=[b for row in board for b in row if b.cget("text")==""]
        cnt=len(empty_buttons)
        win=check_winner(board)
        if cnt==0:
            win=check_winner(board)  # board full, check tie
        elif win==0:
            pos=best_move(board_text)  # find optimal move via minimax
            if pos:
                r,c=pos
                board[r][c].config(text="O",state=tk.DISABLED)
        check_winner(board)

# Tries every empty cell, scores it with minimax, returns the best (row, col) for O
def best_move(board):
    """Return (row, col) of the best move for O using minimax."""
    best_score, best_pos = -100, None
    for r in range(3):
        for c in range(3):
            if board[r][c]=="":
                board[r][c]="O"           # try placing O
                score = minimax(board, False)  # score the resulting board (X moves next)
                board[r][c]=""            # undo the move
                if score > best_score:
                    best_score, best_pos = score, (r, c)
    return best_pos

# Recursive minimax: O maximises score, X minimises it
# Scores: O wins → +10, X wins → -10, tie → 0
def minimax(board, is_maximizing):
    """Minimax: O is maximiser (+10), X is minimiser (-10), tie is 0."""
    result = check_board(board)
    if result=="O":   return 10   # O wins
    if result=="X":   return -10  # X wins
    if result=="tie": return 0    # draw
    if is_maximizing:
        # O's turn — pick the move with the highest score
        best = -100
        for r in range(3):
            for c in range(3):
                if board[r][c]=="":
                    board[r][c]="O"
                    best = max(best, minimax(board, False))
                    board[r][c]=""  # undo
        return best
    else:
        # X's turn — pick the move with the lowest score (worst for O)
        best = 100
        for r in range(3):
            for c in range(3):
                if board[r][c]=="":
                    board[r][c]="X"
                    best = min(best, minimax(board, True))
                    board[r][c]=""  # undo
        return best