import tkinter as tk
import random
from tkinter import messagebox
from mysql_user import *

# ── Board reset ───────────────────────────────────────────────────────────────

def clear_btn(buttons):
    """Reset every cell button back to empty and clickable.
    Called after a game ends (win/loss/tie) so the grid is ready for
    the next round.
    """
    not_empty_buttons = [b for row in buttons for b in row]
    for i in not_empty_buttons:
        i.config(text="", state=tk.NORMAL)

# ── Shared win-check logic ────────────────────────────────────────────────────

def check_board(board_text):
    """Pure win-check on a 2D text board. Returns 'X', 'O', 'tie', or None.

    Takes a plain 3x3 list-of-lists of strings ("X"/"O"/"") rather than
    Tkinter buttons, so it can be reused both by check_winner() (UI layer)
    and by minimax() (search layer) without depending on any widgets.
    """
    # All 8 possible winning lines: 3 rows, 3 columns, 2 diagonals
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
    # No winning line found - if every cell is filled, it's a tie
    if all(board_text[r][c] != "" for r in range(3) for c in range(3)): return "tie"
    # Game still in progress
    return None

def check_winner(board, mode):
    """Check the current game state, show a result popup if it's over,
    reset the board, and record the outcome (win/loss/tie) for `mode`.

    board: the 3x3 grid of Tkinter Button widgets
    mode:  'easy' | 'medium' | 'hard' - used to update the right stat columns

    Returns "X" (player won), "O" (computer won), "tie", or 0 (still playing).
    """
    # Convert the button grid to plain text so check_board() can evaluate it
    board_text=[[board[r][c].cget("text") for c in range(3)] for r in range(3)]
    status = check_board(board_text)
    if status=="X":
        messagebox.showinfo("Game Over","YOU WON 🎉")
        clear_btn(board)
        add_status(mode, "wins")
        return "X"
    elif status=="O":
        messagebox.showinfo("Game Over","Computer Won 😔")
        clear_btn(board)
        add_status(mode, "losses")
        return "O"
    elif status=="tie":
        messagebox.showinfo("Game Over","It's a Tie 😐")
        clear_btn(board)
        add_status(mode, "ties")
        return "tie"
    # Nobody has won yet and the board isn't full - game continues
    return 0

# ── Easy mode: random AI ──────────────────────────────────────────────────────

def easy_mode(btn, board):
    """Handle a player click in Easy mode.
    Player's move is placed as "X"; if the game isn't over, the AI
    responds by picking a uniformly random empty cell as "O".
    """
    if btn.cget("text")=='':
        btn.config(text="X",state=tk.DISABLED)
        # flatten + filter for empty buttons
        empty_buttons = [b for row in board for b in row if b.cget("text") == ""]
        win=check_winner(board, "easy")
        if win==0:
            if empty_buttons:     # only if any are left
                ai_btn = random.choice(empty_buttons)
                ai_btn.config(text="O", state=tk.DISABLED)
        check_winner(board, "easy")

#Computer logic
def medium_mode(btn, board):
    """Handle a player click in Medium mode.
    Player's move is placed as "X"; the AI then defers to check_medium()
    for rule-based win/block/positional strategy, except on the AI's very
    first move (cnt == 8, i.e. only the player's first move has been made),
    which is handled directly below as a special case.
    """
    if btn.cget("text")=='':
        btn.config(text="X",state=tk.DISABLED)
        # flatten + filter for empty buttons
        board=[[board[r][c] for c in range (3)]for r in range (3)]
        empty_buttons = [b for row in board for b in row if b.cget("text") == ""]
        cnt=len(empty_buttons)
        win=check_winner(board, "medium")
        if cnt==0:
            win=check_winner(board, "medium")
        elif win==0:
            check_medium(cnt, board)
        # AI's opening reply: if the player took the center, take a random
        # corner; otherwise take the center (the strongest opening reply).
        if cnt==8:
            if board[1][1].cget("text")=="X" :
                ai_btn = random.choice([board[0][0], board[0][2],board[2][0], board[2][2]])
                ai_btn.config(text="O", state=tk.DISABLED)
            else:
                board[1][1].config(text="O", state=tk.DISABLED)
        check_winner(board, "medium")

def check_medium(cnt, board):
    """Rule-based AI move for Medium mode (checked in priority order):

      1. Take a winning move for "O" if one exists (any row/col/diagonal
         with two O's and one empty cell).
      2. Otherwise, block the player's winning move for "X" the same way.
      3. Otherwise, fall back to positional heuristics based on where the
         player has already played (corner/middle openings), picking a
         random cell from the resulting candidate list.

    `cnt` (remaining empty cells) is used only to route around the special
    AI-opening-move case handled in medium_mode() (see cnt == 8 above).
    """
    board=[[board[r][c] for c in range (3)]for r in range (3)]
    empty_buttons = [b for row in board for b in row if b.cget("text") == ""]
    # Snapshot the text of every row, column, and diagonal so each can be
    # pattern-matched below (e.g. ["O","O",""] means "O is one move from
    # winning this line, and the empty slot is the winning cell").
    hori_1=[board[0][0].cget("text"),board[0][1].cget("text"),board[0][2].cget("text")]
    hori_2=[board[1][0].cget("text"),board[1][1].cget("text"),board[1][2].cget("text")]
    hori_3=[board[2][0].cget("text"),board[2][1].cget("text"),board[2][2].cget("text")]
    ver_1=[board[0][0].cget("text"),board[1][0].cget("text"),board[2][0].cget("text")]
    ver_2=[board[0][1].cget("text"),board[1][1].cget("text"),board[2][1].cget("text")]
    ver_3=[board[0][2].cget("text"),board[1][2].cget("text"),board[2][2].cget("text")]
    diag_1=[board[0][0].cget("text"),board[1][1].cget("text"),board[2][2].cget("text")]
    diag_2=[board[0][2].cget("text"),board[1][1].cget("text"),board[2][0].cget("text")]
    # ── Priority 1: see if AI ("O") can win right now ──
    # Each branch below checks one line for the pattern "two O's + one gap"
    # and immediately fills that gap with "O" to complete the win.
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
    # ── Priority 2: block the player ("X") from winning ──
    # Same pattern as above, but for "two X's + one gap": fill the gap
    # with "O" to stop the player completing that line.
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
    # ── Priority 3: no immediate win/block available - positional play ──
    # Neither the AI nor the player has a one-move win right now, so fall
    # back to opening-strategy heuristics keyed off where the player has
    # played relative to the AI's center move.
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

# ── Hard mode: unbeatable minimax AI ──────────────────────────────────────────

def hard_mode(btn, board):
    """Handle a player click in Hard mode.
    Player's move is placed as "X"; the AI then uses best_move() (backed
    by a full minimax search) to always pick the objectively best reply -
    guaranteeing the AI can never lose, only win or draw.
    """
    if btn.cget("text")=='':
        btn.config(text="X",state=tk.DISABLED)
        # Convert the button grid to plain text for the minimax search
        board_text=[[board[r][c].cget("text") for c in range(3)] for r in range(3)]
        empty_buttons=[b for row in board for b in row if b.cget("text")==""]
        cnt=len(empty_buttons)
        win=check_winner(board, "hard")
        if cnt==0:
            win=check_winner(board, "hard")
        elif win==0:
            pos=best_move(board_text)
            if pos:
                r,c=pos
                board[r][c].config(text="O",state=tk.DISABLED)
        check_winner(board, "hard")

def best_move(board):
    """Return (row, col) of the best move for O using minimax.

    Tries every empty cell as a candidate "O" move, scores each resulting
    position via minimax() (from X's upcoming turn, is_maximizing=False),
    and keeps whichever candidate yields the highest score for O.
    """
    best_score, best_pos = -100, None
    for r in range(3):
        for c in range(3):
            if board[r][c]=="":
                # Try this move, score it, then undo it (backtracking)
                board[r][c]="O"
                score = minimax(board, False)
                board[r][c]=""
                if score > best_score:
                    best_score, best_pos = score, (r, c)
    return best_pos

def minimax(board, is_maximizing):
    """Minimax: O is maximiser (+10), X is minimiser (-10), tie is 0.

    Recursively explores every remaining move: on O's turn it picks the
    move that maximizes the score (best for the AI), on X's turn it
    picks the move that minimizes the score (worst-case for the AI,
    i.e. assumes the player plays optimally). Terminal positions are
    scored via check_board(); the recursion bottoms out once no empty
    cells remain (this is small enough - max 9 cells - to search fully).
    """
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